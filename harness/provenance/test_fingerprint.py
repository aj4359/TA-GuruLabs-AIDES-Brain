"""Smoke and tamper tests for provenance CLI. Run python3 -m unittest discover -s harness/provenance."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("fingerprint.py")

class FingerprintTests(unittest.TestCase):
    def test_create_verify_and_tamper(self):
        with tempfile.TemporaryDirectory() as td:
            base = Path(td)
            source = base / "source.bin"
            manifest = base / "evidence.json"
            source.write_bytes(b"original JingWu artifact")
            create = subprocess.run(
                [sys.executable, str(SCRIPT), "create", "--file", str(source),
                 "--project", "JWM-TEST", "--asset-id", "test-1", "--out", str(manifest),
                 "--contributor", "Anthony Johnson", "--tool", "Maestro AIDE"],
                capture_output=True, text=True
            )
            self.assertEqual(create.returncode, 0, create.stderr)
            self.assertEqual(json.loads(manifest.read_text())["rights_status"], "unverified")
            good = subprocess.run(
                [sys.executable, str(SCRIPT), "verify", "--file", str(source),
                 "--manifest", str(manifest)], capture_output=True, text=True
            )
            self.assertEqual(good.returncode, 0, good.stderr)
            self.assertTrue(json.loads(good.stdout)["verified"])
            source.write_bytes(b"tampered JingWu artifact")
            bad = subprocess.run(
                [sys.executable, str(SCRIPT), "verify", "--file", str(source),
                 "--manifest", str(manifest)], capture_output=True, text=True
            )
            self.assertEqual(bad.returncode, 1)
            self.assertFalse(json.loads(bad.stdout)["verified"])
    def test_refuses_overwrite(self):
        with tempfile.TemporaryDirectory() as td:
            base=Path(td)
            source=base/"x.bin"; source.write_bytes(b"demo")
            manifest=base/"x.json"
            args=[sys.executable,str(SCRIPT),"create","--file",str(source),"--project","P",
                  "--asset-id","A","--out",str(manifest)]
            self.assertEqual(subprocess.run(args,capture_output=True).returncode,0)
            self.assertEqual(subprocess.run(args,capture_output=True).returncode,2)

if __name__=="__main__":
    unittest.main()
