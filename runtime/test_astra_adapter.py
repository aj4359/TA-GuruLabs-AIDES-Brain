import os,unittest
from unittest.mock import patch
from astra_adapter import create_edit_plan

class AstraTests(unittest.TestCase):
    def test_disabled_by_default(self):
        with patch.dict(os.environ,{"AI_ENABLED":"false","OPENAI_API_KEY":"fake"}):
            with self.assertRaises(RuntimeError): create_edit_plan({"clips":[]},allow_paid=True)
    def test_requires_spend_authorisation(self):
        with patch.dict(os.environ,{"AI_ENABLED":"true","AI_MAX_COST_GBP_PER_JOB":"0","OPENAI_API_KEY":"fake"}):
            with self.assertRaises(RuntimeError): create_edit_plan({"clips":[]},allow_paid=True)

if __name__=="__main__": unittest.main()
