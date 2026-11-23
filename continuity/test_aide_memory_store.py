"""Offline security/continuity semantics for private AIDE memory, no real user content."""
import tempfile,unittest
from pathlib import Path
from aide_memory_store import connect,add_asset,add_memory,approve_memory,recall
class MemoryTests(unittest.TestCase):
    def setUp(self):
        self.t=tempfile.TemporaryDirectory()
        self.db=connect(str(Path(self.t.name)/'private.sqlite3'))
    def tearDown(self):
        self.db.close();self.t.cleanup()
    def test_individual_memory_isolation_and_project_partition(self):
        a=add_memory(self.db,actor='test',owner_aide='CUTLASS',project='BYL',
             memory_type='lesson',content='Use measured downbeat',source_ref='test:1')
        approve_memory(self.db,actor='test',memory_id=a)
        self.assertEqual(len(recall(self.db,aide='CUTLASS',project='BYL')),1)
        self.assertEqual(recall(self.db,aide='MAESTRO',project='BYL'),[])
        self.assertEqual(recall(self.db,aide='CUTLASS',project='SICARIO'),[])
    def test_team_memory_requires_approval(self):
        a=add_memory(self.db,actor='test',owner_aide='CUTLASS',project='BYL',
             memory_type='decision',content='Approved fictional scene cue',
             source_ref='test:2',visibility='team')
        self.assertEqual(recall(self.db,aide='MAESTRO',project='BYL'),[])
        approve_memory(self.db,actor='test',memory_id=a)
        self.assertEqual(len(recall(self.db,aide='MAESTRO',project='BYL')),1)
    def test_asset_registration_does_not_mean_backup(self):
        p=Path(self.t.name)/'audio.bin';p.write_bytes(b'FAKE-TEST-DATA')
        a=add_asset(self.db,actor='test',project='BYL',title='synthetic sample',
                    kind='audio',version='v1',rights='test fixture',file=p)
        self.assertEqual(a['status'],'registered')
        self.assertEqual(a['bytes'],len(b'FAKE-TEST-DATA'))
        self.assertEqual(len(a['sha256']),64)
if __name__=='__main__':unittest.main()
