"""Offline tests for Astra Responses adapter, using mocked network responses."""
import json
import os
import unittest
from io import BytesIO
from unittest.mock import patch
from astra_adapter import create_edit_plan

MANIFEST={"brief":"cut to music", "clips":[{"id":"one","duration":60}]}

class FakeResponse:
    def __init__(self,text):
        self.data=BytesIO(json.dumps({
            "output":[{"type":"message","content":[{"type":"output_text","text":text}]}]
        }).encode())
    def __enter__(self): return self
    def __exit__(self,*args): self.data.close()
    def read(self,*args): return self.data.read(*args)

class AstraAdapterTests(unittest.TestCase):
    def test_disabled_by_default(self):
        with patch.dict(os.environ,{"AI_ENABLED":"false","OPENAI_API_KEY":"fake",
                                    "AI_MAX_COST_GBP_PER_JOB":"2"}):
            with patch("urllib.request.urlopen") as network:
                with self.assertRaisesRegex(RuntimeError,"AI disabled"):
                    create_edit_plan(MANIFEST,allow_paid=True)
                network.assert_not_called()

    def test_budget_is_required(self):
        with patch.dict(os.environ,{"AI_ENABLED":"true","OPENAI_API_KEY":"fake",
                                    "AI_MAX_COST_GBP_PER_JOB":"0"}):
            with patch("urllib.request.urlopen") as network:
                with self.assertRaisesRegex(RuntimeError,"budget"):
                    create_edit_plan(MANIFEST,allow_paid=True)
                network.assert_not_called()

    def test_valid_mocked_response(self):
        plan='{"shots":[{"clip_id":"one","start":0,"end":60}]}'
        with patch.dict(os.environ,{"AI_ENABLED":"true","OPENAI_API_KEY":"fake",
                                    "AI_MAX_COST_GBP_PER_JOB":"2"}):
            with patch("urllib.request.urlopen",return_value=FakeResponse(plan)):
                result=create_edit_plan(MANIFEST,allow_paid=True)
        self.assertEqual(result["shots"][0]["end"],60)
        self.assertEqual(result["model"],"gpt-6.2-astra")

    def test_reject_unknown_clip_from_model(self):
        plan='{"shots":[{"clip_id":"fabricated","start":0,"end":60}]}'
        with patch.dict(os.environ,{"AI_ENABLED":"true","OPENAI_API_KEY":"fake",
                                    "AI_MAX_COST_GBP_PER_JOB":"2"}):
            with patch("urllib.request.urlopen",return_value=FakeResponse(plan)):
                with self.assertRaisesRegex(ValueError,"Unknown clip"):
                    create_edit_plan(MANIFEST,allow_paid=True)

    def test_reject_short_edit(self):
        plan='{"shots":[{"clip_id":"one","start":0,"end":10}]}'
        with patch.dict(os.environ,{"AI_ENABLED":"true","OPENAI_API_KEY":"fake",
                                    "AI_MAX_COST_GBP_PER_JOB":"2"}):
            with patch("urllib.request.urlopen",return_value=FakeResponse(plan)):
                with self.assertRaisesRegex(ValueError,"close to 60"):
                    create_edit_plan(MANIFEST,allow_paid=True)

if __name__=="__main__": unittest.main()
