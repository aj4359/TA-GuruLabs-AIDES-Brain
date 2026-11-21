import json, threading, unittest
from http.server import ThreadingHTTPServer
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from server import Handler, inspect_document

class DemoTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.s=ThreadingHTTPServer(("127.0.0.1",0),Handler)
        cls.t=threading.Thread(target=cls.s.serve_forever,daemon=True); cls.t.start()
        cls.url="http://127.0.0.1:%d/v1/docuguard/check"%cls.s.server_port
    @classmethod
    def tearDownClass(cls):
        cls.s.shutdown(); cls.s.server_close()
    def post(self,obj,token=None):
        headers={"Content-Type":"application/json"}
        if token: headers["X-Demo-Payment"]=token
        req=Request(self.url,json.dumps(obj).encode(),headers,method="POST")
        try:
            with urlopen(req) as r: return r.status,json.load(r)
        except HTTPError as e: return e.code,json.load(e)
    def test_unpaid(self):
        status,body=self.post({"text":"Date: today"})
        self.assertEqual(status,402);self.assertFalse(body["real_payments_enabled"])
    def test_paid_simulation(self):
        status,body=self.post({"text":"Date: A\nRef: B\nSigned: C"},"demo-paid")
        self.assertEqual(status,200);self.assertTrue(body["complete"])
    def test_incomplete(self):
        status,body=self.post({"text":"Date: A"},"demo-paid")
        self.assertEqual(status,200);self.assertFalse(body["complete"])
    def test_invalid(self):
        self.assertEqual(self.post({"wrong":"A"},"demo-paid")[0],400)
    def test_demo_only(self):
        self.assertTrue(inspect_document("signed: A")["demo_only"])

if __name__=="__main__":unittest.main()
