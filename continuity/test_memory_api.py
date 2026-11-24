"""Real HTTP integration tests of the private AIDE memory service."""
import hashlib,json,tempfile,threading,unittest,urllib.request,urllib.error
from pathlib import Path
from continuity.memory_api import load_identities,serve

def person(name,role,secret,projects):
    return {"name":name,"role":role,"token_sha256":hashlib.sha256(secret.encode()).hexdigest(),"projects":projects}

class LiveMemoryAPITests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp=tempfile.TemporaryDirectory()
        config=[person("founder","founder","founder-test-secret-2026",["SICARIO","BARD"]),
                person("CUTLASS","aide","cutlass-test-secret-2026",["SICARIO"]),
                person("MAESTRO","aide","maestro-test-secret-2026",["SICARIO"])]
        cls.server=serve(str(Path(cls.tmp.name)/"memory.sqlite3"),load_identities(json.dumps(config)),0)
        cls.url="http://127.0.0.1:"+str(cls.server.server_address[1])
        cls.thread=threading.Thread(target=cls.server.serve_forever,daemon=True)
        cls.thread.start()
    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown();cls.server.server_close();cls.thread.join(timeout=2);cls.tmp.cleanup()
    def api(self,method,path,secret=None,obj=None):
        body=None if obj is None else json.dumps(obj).encode()
        headers={"Content-Type":"application/json"}
        if secret:headers["Authorization"]="Bearer "+secret
        req=urllib.request.Request(self.url+path,body,headers=headers,method=method)
        try:
            with urllib.request.urlopen(req,timeout=5) as res:return res.status,json.load(res)
        except urllib.error.HTTPError as e:return e.code,json.load(e)
    def test_private_memory_safeguards_and_restart(self):
        actor="cutlass-test-secret-2026"; boss="founder-test-secret-2026"
        status,out=self.api("POST","/v1/memories/draft",actor,{"project":"SICARIO","type":"decision",
            "content":"Don Azrael canon detail (synthetic test)","source_ref":"test:approved-document",
            "visibility":"private"})
        self.assertEqual(status,201)
        mid=out["id"]
        self.assertEqual(self.api("GET","/v1/context?project=SICARIO",actor)[1]["approved_memories"],[])
        self.assertEqual(self.api("POST","/v1/memories/approve",actor,{"project":"SICARIO","id":mid})[0],403)
        self.assertEqual(self.api("POST","/v1/memories/approve",boss,{"project":"BARD","id":mid})[0],403)
        self.assertEqual(self.api("POST","/v1/memories/approve",boss,{"project":"SICARIO","id":mid})[0],200)
        self.assertEqual(len(self.api("GET","/v1/context?project=SICARIO",actor)[1]["approved_memories"]),1)
        self.assertEqual(self.api("GET","/v1/context?project=SICARIO","maestro-test-secret-2026")[1]["approved_memories"],[])
        self.assertEqual(self.api("GET","/v1/context?project=BARD",actor)[0],403)
        self.assertEqual(self.api("GET","/v1/context?project=SICARIO&aide=MAESTRO",actor)[0],403)
        self.assertEqual(self.api("GET","/v1/context?project=SICARIO")[0],401)
        # simulate independent new client session; API reopens SQLite for each request
        self.assertEqual(len(self.api("GET","/v1/context?project=SICARIO",actor)[1]["approved_memories"]),1)
    def test_shared_memory_requires_approval(self):
        actor="cutlass-test-secret-2026"
        _,out=self.api("POST","/v1/memories/draft",actor,{"project":"SICARIO","type":"fact",
           "content":"Synthetic shared canon","source_ref":"test:shared","visibility":"team"})
        before=self.api("GET","/v1/context?project=SICARIO","maestro-test-secret-2026")[1]["approved_memories"]
        self.assertFalse(any(m["id"]==out["id"] for m in before))
        self.assertEqual(self.api("POST","/v1/memories/approve","founder-test-secret-2026",{"project":"SICARIO","id":out["id"]})[0],200)
        after=self.api("GET","/v1/context?project=SICARIO","maestro-test-secret-2026")[1]["approved_memories"]
        self.assertTrue(any(m["id"]==out["id"] for m in after))
    def test_actual_server_restart_retains_approved_memory(self):
        # Start a separate instance, shut it down, then start another server
        # pointing at the same durable SQLite file. Use an entirely new client.
        from continuity.memory_api import load_identities, serve
        import urllib.request
        db=str(Path(self.tmp.name)/"restart-memory.sqlite3")
        ids=load_identities(json.dumps([
            person("founder","founder","restart-founder-token",["BARD"]),
            person("CUTLASS","aide","restart-cutlass-token",["BARD"]),
        ]))
        def request(server,method,path,token,obj=None):
            body=json.dumps(obj).encode() if obj is not None else None
            req=urllib.request.Request(
                "http://127.0.0.1:"+str(server.server_address[1])+path,
                data=body,method=method,
                headers={"Authorization":"Bearer "+token,"Content-Type":"application/json"})
            with urllib.request.urlopen(req,timeout=5) as resp:return json.load(resp)
        first=serve(db,ids,0)
        t=threading.Thread(target=first.serve_forever,daemon=True);t.start()
        try:
            created=request(first,"POST","/v1/memories/draft","restart-cutlass-token",{
                "project":"BARD","type":"lesson","content":"Approved timing cue survives process restart",
                "source_ref":"test:independent-worker-restart","visibility":"team"})
            request(first,"POST","/v1/memories/approve","restart-founder-token",
                    {"project":"BARD","id":created["id"]})
        finally:
            first.shutdown();first.server_close();t.join(timeout=3)
        second=serve(db,ids,0)
        t2=threading.Thread(target=second.serve_forever,daemon=True);t2.start()
        try:
            pkt=request(second,"GET","/v1/context?project=BARD","restart-cutlass-token")
            self.assertEqual(len(pkt["approved_memories"]),1)
            self.assertEqual(pkt["approved_memories"][0]["id"],created["id"])
        finally:
            second.shutdown();second.server_close();t2.join(timeout=3)

    def test_reject_bad_identity_configuration(self):
        with self.assertRaises(ValueError):
            load_identities("[]")
        with self.assertRaises(ValueError):
            load_identities(json.dumps([person("x","admin","x",["SICARIO"])]))
    def test_body_limits_and_no_auth(self):
        self.assertEqual(self.api("POST","/v1/memories/draft",None,{"project":"SICARIO"})[0],401)
        too_long="Q"*40000
        self.assertEqual(self.api("POST","/v1/memories/draft","cutlass-test-secret-2026",
            {"project":"SICARIO","type":"fact","content":too_long,"source_ref":"test"})[0],400)

if __name__=="__main__":unittest.main()
