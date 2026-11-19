"""x402-inspired LOCAL DEMO ONLY: no wallet, settlement, or real authentication."""
import json, re
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

def inspect_document(text):
    fields = {"date": r"\b(?:date|dated)\s*:", "reference": r"\b(?:reference|ref)\s*:", "signature": r"\b(?:signature|signed)\s*:"}
    checks = {k: bool(re.search(p, text, re.I)) for k,p in fields.items()}
    return {"demo_only": True, "checks": checks, "complete": all(checks.values()), "notice":"Field presence only; not a security, identity, tax or legal validation"}

class Handler(BaseHTTPRequestHandler):
    def reply(self, status, data):
        b=json.dumps(data).encode()
        self.send_response(status); self.send_header("Content-Type","application/json")
        self.send_header("Cache-Control","no-store"); self.send_header("Content-Length",str(len(b)))
        self.end_headers(); self.wfile.write(b)
    def do_GET(self):
        if self.path=="/health": return self.reply(200,{"status":"ok","mode":"local-demo","payments":"disabled"})
        self.reply(404,{"error":"not found"})
    def do_POST(self):
        if self.path!="/v1/docuguard/check": return self.reply(404,{"error":"not found"})
        try: n=int(self.headers.get("Content-Length","-1"))
        except ValueError: return self.reply(400,{"error":"invalid content length"})
        if n<0 or n>8192: return self.reply(413,{"error":"request size out of demo bounds"})
        if self.headers.get("X-Demo-Payment")!="demo-paid":
            return self.reply(402,{"error":"simulated payment required","mode":"x402-inspired-NOT-compliant","price_example":{"amount":"0.10","currency":"GBP"},"demo_header":{"X-Demo-Payment":"demo-paid"},"real_payments_enabled":False})
        try:
            obj=json.loads(self.rfile.read(n))
            if not isinstance(obj,dict) or not isinstance(obj.get("text"),str): return self.reply(400,{"error":"JSON text string required"})
            if len(obj["text"])>4000: return self.reply(413,{"error":"text too long"})
            return self.reply(200,inspect_document(obj["text"]))
        except (UnicodeDecodeError,json.JSONDecodeError): return self.reply(400,{"error":"invalid JSON"})

if __name__=="__main__":
    print("Local mock only: http://127.0.0.1:8765 (no real payments)")
    ThreadingHTTPServer(("127.0.0.1",8765),Handler).serve_forever()
