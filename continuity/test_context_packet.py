"""Guardrails for TA GuruLabs project-bound context packets."""
import tempfile,unittest
from pathlib import Path
from aide_memory_store import connect, add_memory, approve_memory, add_asset
from context_packet import context_packet

class ContextPacketTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.c=connect(str(Path(self.tmp.name)/"memory.sqlite3"))
    def tearDown(self):
        self.c.close();self.tmp.cleanup()
    def test_no_cross_aide_or_cross_project_private_memory(self):
        secret=add_memory(self.c,actor="test",owner_aide="CUTLASS",project="SICARIO",
          memory_type="decision",content="Private creative work",source_ref="issue:test")
        approve_memory(self.c,actor="test",memory_id=secret)
        self.assertEqual(len(context_packet(self.c,aide="CUTLASS",project="SICARIO")["approved_memories"]),1)
        self.assertEqual(context_packet(self.c,aide="MAESTRO",project="SICARIO")["approved_memories"],[])
        self.assertEqual(context_packet(self.c,aide="CUTLASS",project="PAYE")["approved_memories"],[])
    def test_draft_team_hidden_until_approved(self):
        item=add_memory(self.c,actor="test",owner_aide="CUTLASS",project="SICARIO",
          memory_type="fact",content="Canon v3",source_ref="manifest:v3",visibility="team")
        self.assertEqual(context_packet(self.c,aide="MAESTRO",project="SICARIO")["approved_memories"],[])
        approve_memory(self.c,actor="test",memory_id=item)
        self.assertEqual(len(context_packet(self.c,aide="MAESTRO",project="SICARIO")["approved_memories"]),1)
    def test_confidential_asset_not_returned(self):
        add_asset(self.c,actor="test",project="SICARIO",title="unreleased master",
          kind="video",version="v1",rights="owned",confidentiality="confidential",
          uri="private://unpublished.mp4")
        add_asset(self.c,actor="test",project="SICARIO",title="public trailer",
          kind="video",version="v1",rights="owned",confidentiality="public",
          uri="https://example.invalid/trailer.mp4")
        packet=context_packet(self.c,aide="CUTLASS",project="SICARIO")
        self.assertEqual(len(packet["nonconfidential_asset_index"]),1)
        self.assertNotIn("private://",repr(packet))
        self.assertNotIn("https://example.invalid",repr(packet))
    def test_invalid_limits_fail(self):
        with self.assertRaises(ValueError):
            context_packet(self.c,aide="CUTLASS",project="SICARIO",max_memories=0)
if __name__=="__main__":unittest.main()
