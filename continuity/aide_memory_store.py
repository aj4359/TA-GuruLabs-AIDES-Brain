#!/usr/bin/env python3
"""JingWu/TA GuruLabs portable asset index + AIDE memory store.
Standard-library-only SQLite. Run locally or in a trusted private worker.
NOT a hosted API, not an authenticated network service, not a cloud backup.
"""
import argparse, hashlib, json, sqlite3, uuid
from datetime import datetime, timezone
from pathlib import Path

SCHEMA = """
PRAGMA foreign_keys=ON;
CREATE TABLE IF NOT EXISTS assets (
 id TEXT PRIMARY KEY, project TEXT NOT NULL, title TEXT NOT NULL,
 kind TEXT NOT NULL, version TEXT NOT NULL,
 uri TEXT, sha256 TEXT, bytes INTEGER, rights TEXT NOT NULL,
 confidentiality TEXT NOT NULL CHECK(confidentiality IN ('public','internal','confidential')),
 status TEXT NOT NULL CHECK(status IN ('registered','copied','restore_verified')),
 source_id TEXT, created_at TEXT NOT NULL,
 UNIQUE(project,title,version)
);
CREATE INDEX IF NOT EXISTS ix_asset_project ON assets(project,kind);
CREATE TABLE IF NOT EXISTS memories (
 id TEXT PRIMARY KEY, owner_aide TEXT NOT NULL, project TEXT NOT NULL,
 memory_type TEXT NOT NULL CHECK(memory_type IN ('fact','decision','lesson','blocker','preference')),
 content TEXT NOT NULL, source_ref TEXT NOT NULL,
 visibility TEXT NOT NULL CHECK(visibility IN ('private','team')),
 approval TEXT NOT NULL CHECK(approval IN ('draft','approved','rejected')),
 created_at TEXT NOT NULL,
 supersedes_id TEXT REFERENCES memories(id)
);
CREATE INDEX IF NOT EXISTS ix_memory_access ON memories(project,owner_aide,visibility,approval);
CREATE TABLE IF NOT EXISTS audit (
 id INTEGER PRIMARY KEY AUTOINCREMENT, at TEXT NOT NULL, actor TEXT NOT NULL,
 action TEXT NOT NULL, target TEXT NOT NULL
);
"""
def now(): return datetime.now(timezone.utc).isoformat()
def uid(): return str(uuid.uuid4())
def connect(db):
    p=Path(db); p.parent.mkdir(parents=True,exist_ok=True)
    c=sqlite3.connect(p);c.row_factory=sqlite3.Row;c.executescript(SCHEMA)
    return c
def audit(c,actor,action,target):
    c.execute("INSERT INTO audit(at,actor,action,target) VALUES(?,?,?,?)",(now(),actor,action,target))
def add_asset(c, *, actor, project,title,kind,version,rights,confidentiality='confidential',uri=None,file=None,source_id=None):
    if not actor or not project or not title or not rights: raise ValueError("Required asset metadata missing")
    sha=None; size=None
    if file:
        p=Path(file).resolve()
        if not p.is_file(): raise FileNotFoundError(file)
        h=hashlib.sha256()
        with p.open("rb") as fp:
            for chunk in iter(lambda:fp.read(1024*1024),b''):h.update(chunk)
        sha,size=h.hexdigest(),p.stat().st_size
    aid=uid()
    c.execute("INSERT INTO assets VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)",
              (aid,project,title,kind,version,uri,sha,size,rights,confidentiality,
               'registered',source_id,now()))
    audit(c,actor,'asset_register',aid);c.commit()
    return dict(c.execute("SELECT * FROM assets WHERE id=?",(aid,)).fetchone())
def add_memory(c, *, actor, owner_aide,project,memory_type,content,source_ref,visibility='private',supersedes_id=None):
    # No unsourced memories; always draft until a separate approval operation.
    if not all((actor,owner_aide,project,memory_type,content,source_ref)):
        raise ValueError("Memory provenance mandatory")
    mid=uid()
    c.execute("INSERT INTO memories VALUES(?,?,?,?,?,?,?,?,?,?)",
              (mid,owner_aide,project,memory_type,content,source_ref,
               visibility,'draft',now(),supersedes_id))
    audit(c,actor,'memory_drafted',mid);c.commit()
    return mid
def approve_memory(c,*,actor,memory_id):
    # Caller authentication/roles MUST be enforced by host application.
    row=c.execute("SELECT id FROM memories WHERE id=?",(memory_id,)).fetchone()
    if not row: raise KeyError(memory_id)
    c.execute("UPDATE memories SET approval='approved' WHERE id=?",(memory_id,))
    audit(c,actor,'memory_approved',memory_id);c.commit()
def recall(c,*,aide,project,query=''):
    # Private memory is visible ONLY to owning aide; team memory visible
    # only once explicitly approved. Project scope is always enforced.
    rows=c.execute("""SELECT id,owner_aide,memory_type,content,source_ref,visibility,created_at
    FROM memories WHERE project=? AND approval='approved'
      AND ((owner_aide=? AND visibility='private') OR visibility='team')
      AND content LIKE ? ORDER BY created_at DESC LIMIT 100""",
      (project,aide,'%'+query.replace('%','\\%').replace('_','\\_')+'%')).fetchall()
    return [dict(r) for r in rows]
def main():
    p=argparse.ArgumentParser()
    p.add_argument('--db',default='.private/jingwu_memory.sqlite3')
    sub=p.add_subparsers(dest='op',required=True)
    a=sub.add_parser('asset');a.add_argument('--actor',required=True);a.add_argument('--project',required=True)
    a.add_argument('--title',required=True);a.add_argument('--kind',required=True)
    a.add_argument('--version',required=True);a.add_argument('--rights',required=True)
    a.add_argument('--file');a.add_argument('--uri')
    m=sub.add_parser('remember');m.add_argument('--actor',required=True)
    m.add_argument('--aide',required=True);m.add_argument('--project',required=True)
    m.add_argument('--type',required=True);m.add_argument('--content',required=True)
    m.add_argument('--source',required=True);m.add_argument('--visibility',choices=['private','team'],default='private')
    r=sub.add_parser('recall');r.add_argument('--aide',required=True);r.add_argument('--project',required=True);r.add_argument('--query',default='')
    v=sub.add_parser('approve');v.add_argument('--actor',required=True);v.add_argument('--id',required=True)
    args=p.parse_args();c=connect(args.db)
    if args.op=='asset': out=add_asset(c,actor=args.actor,project=args.project,title=args.title,
       kind=args.kind,version=args.version,rights=args.rights,file=args.file,uri=args.uri)
    elif args.op=='remember':out={'id':add_memory(c,actor=args.actor,owner_aide=args.aide,project=args.project,
       memory_type=args.type,content=args.content,source_ref=args.source,visibility=args.visibility)}
    elif args.op=='recall':out=recall(c,aide=args.aide,project=args.project,query=args.query)
    else:approve_memory(c,actor=args.actor,memory_id=args.id);out={'approved':args.id}
    print(json.dumps(out,indent=2))
if __name__=='__main__':main()
