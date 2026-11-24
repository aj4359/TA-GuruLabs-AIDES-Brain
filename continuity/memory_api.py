"""TA GuruLabs private per-AIDE memory HTTP service, standard library only.

Binds to 127.0.0.1. Every request must carry a bearer token mapped to a
server-controlled identity and project scope. For remote use, add a reviewed
TLS-authenticated private gateway; do NOT expose this directly on the internet.
Start: TA_MEMORY_IDENTITIES_JSON='[{"name":"...","token_sha256":"...",
 "role":"founder","projects":["SICARIO"]}]' python -m continuity.memory_api
"""
from __future__ import annotations
import hashlib
import hmac
import json
import os
import sqlite3
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlsplit
from continuity.aide_memory_store import connect, add_memory, approve_memory
from continuity.context_packet import context_packet

MAX_JSON_BYTES = 32768
MAX_TOKEN_BYTES = 256
MAX_TEXT_CHARS = 3000


def load_identities(raw: str) -> list[dict]:
    values = json.loads(raw)
    if not isinstance(values, list) or not values:
        raise ValueError("Nonempty identity configuration required")
    seen=set()
    for v in values:
        if not isinstance(v,dict) or v.get("role") not in ("founder","aide"):
            raise ValueError("Unknown identity role")
        if not isinstance(v.get("name"),str) or not v["name"].strip():
            raise ValueError("Identity name required")
        digest=v.get("token_sha256")
        if not isinstance(digest,str) or len(digest)!=64 or any(c not in "0123456789abcdef" for c in digest):
            raise ValueError("Invalid token digest")
        if digest in seen: raise ValueError("Duplicate token digest")
        seen.add(digest)
        if not isinstance(v.get("projects"),list) or not v["projects"] or any(not isinstance(s,str) or not s.strip() for s in v["projects"]):
            raise ValueError("Each identity requires project scopes")
    return values


def resolve_identity(identities: list[dict], bearer: str | None):
    if not bearer or len(bearer) > MAX_TOKEN_BYTES:
        return None
    supplied = hashlib.sha256(bearer.encode("utf-8")).hexdigest()
    matched = None
    for person in identities:
        if hmac.compare_digest(supplied,person["token_sha256"]):
            matched=person
    return matched


def make_handler(db_path: str, identities: list[dict]):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *_args):
            # Suppress headers and tokens in standard logs. Delegate controlled
            # request metadata logging to trusted hosting infrastructure.
            return
        def send(self, status, payload):
            blob=json.dumps(payload,sort_keys=True).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type","application/json")
            self.send_header("Content-Length",str(len(blob)))
            self.send_header("Cache-Control","no-store")
            self.send_header("X-Content-Type-Options","nosniff")
            self.end_headers()
            self.wfile.write(blob)
        def who(self):
            header=self.headers.get("Authorization","")
            if not header.startswith("Bearer "):
                return None
            return resolve_identity(identities,header[7:])
        def body(self):
            raw_len=self.headers.get("Content-Length","")
            try: length=int(raw_len)
            except ValueError: raise ValueError("Invalid content length")
            if length<=0 or length>MAX_JSON_BYTES:raise ValueError("JSON payload too large or empty")
            body=json.loads(self.rfile.read(length))
            if not isinstance(body,dict):raise ValueError("JSON object required")
            return body
        def in_scope(self,identity,project):
            return isinstance(project,str) and project in identity["projects"]
        def do_GET(self):
            identity=self.who()
            if not identity:return self.send(401,{"error":"unauthorized"})
            u=urlsplit(self.path)
            if u.path=="/v1/health":
                return self.send(200,{"status":"serving","scope":"private-local-memory-service"})
            if u.path!="/v1/context":return self.send(404,{"error":"not_found"})
            qs=parse_qs(u.query)
            project=qs.get("project",[""])[0]
            if not self.in_scope(identity,project):
                return self.send(403,{"error":"out_of_scope"})
            if identity["role"]=="founder":
                # Founder may request an AIDE's context for an authorized project.
                aide=qs.get("aide",[""])[0]
                if not aide:return self.send(400,{"error":"aide_required"})
            else:
                aide=identity["name"]
                if "aide" in qs and qs["aide"][0]!=aide:
                    return self.send(403,{"error":"identity_mismatch"})
            con=connect(db_path)
            try:packet=context_packet(con,aide=aide,project=project)
            finally:con.close()
            # API layer has authenticated the caller. Preserve the library's
            # explicit status flag separately from host verification.
            packet["authenticated_subject"]=identity["name"]
            packet["scope_verified"]=True
            return self.send(200,packet)
        def do_POST(self):
            identity=self.who()
            if not identity:return self.send(401,{"error":"unauthorized"})
            u=urlsplit(self.path)
            if u.path not in ("/v1/memories/draft","/v1/memories/approve"):
                return self.send(404,{"error":"not_found"})
            try:obj=self.body()
            except (ValueError,json.JSONDecodeError):
                return self.send(400,{"error":"invalid_json_or_size"})
            project=obj.get("project","")
            if not self.in_scope(identity,project):
                return self.send(403,{"error":"out_of_scope"})
            con=connect(db_path)
            try:
                if u.path=="/v1/memories/draft":
                    owner=identity["name"] if identity["role"]=="aide" else obj.get("aide","")
                    if not owner or (identity["role"]=="aide" and "aide" in obj and obj["aide"]!=owner):
                        return self.send(403,{"error":"identity_mismatch"})
                    content=obj.get("content","")
                    source=obj.get("source_ref","")
                    if not isinstance(content,str) or not 1<=len(content)<=MAX_TEXT_CHARS or not isinstance(source,str) or not 1<=len(source)<=400:
                        return self.send(400,{"error":"invalid_content_or_source"})
                    if obj.get("visibility","private") not in ("private","team"):
                        return self.send(400,{"error":"invalid_visibility"})
                    if obj.get("type","") not in ("fact","decision","lesson","blocker","preference"):
                        return self.send(400,{"error":"invalid_type"})
                    mid=add_memory(con,actor=identity["name"],owner_aide=owner,project=project,
                        memory_type=obj["type"],content=content,source_ref=source,
                        visibility=obj.get("visibility","private"))
                    return self.send(201,{"id":mid,"approval":"draft"})
                if identity["role"]!="founder":
                    return self.send(403,{"error":"founder_approval_required"})
                mid=obj.get("id","")
                if not isinstance(mid,str) or len(mid)>100:
                    return self.send(400,{"error":"invalid_memory_id"})
                # Critical: approval must match project authorisation.
                actual=con.execute("SELECT project FROM memories WHERE id=?",(mid,)).fetchone()
                if not actual:return self.send(404,{"error":"unknown_memory"})
                if actual["project"]!=project:
                    return self.send(403,{"error":"cross_project_approval_denied"})
                approve_memory(con,actor=identity["name"],memory_id=mid)
                return self.send(200,{"id":mid,"approval":"approved"})
            except (sqlite3.Error,ValueError,KeyError):
                return self.send(400,{"error":"invalid_request"})
            finally:con.close()
    return Handler


def serve(db_path: str, identities: list[dict], port: int = 8767):
    if port<0 or port>65535:raise ValueError("Invalid port")
    # Bound only to loopback, never 0.0.0.0; private reverse proxy required.
    srv=ThreadingHTTPServer(("127.0.0.1",port),make_handler(db_path,identities))
    return srv


def main():
    raw=os.environ.get("TA_MEMORY_IDENTITIES_JSON","")
    if not raw:raise SystemExit("TA_MEMORY_IDENTITIES_JSON is required")
    ids=load_identities(raw)
    db=os.environ.get("TA_MEMORY_DB",".private/tagurulabs_memory.sqlite3")
    port=int(os.environ.get("TA_MEMORY_PORT","8767"))
    Path(db).parent.mkdir(parents=True,exist_ok=True)
    serve(db,ids,port).serve_forever()


if __name__=="__main__":main()
