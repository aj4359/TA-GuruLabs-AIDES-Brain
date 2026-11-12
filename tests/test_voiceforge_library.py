"""Zero-network unit tests for VoiceForge asset permissions and path isolation."""
import importlib
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


class LibraryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.env = patch.dict(os.environ, {"VOICEFORGE_DATA_DIR": self.temp.name})
        self.env.start()
        self.addCleanup(self.env.stop)
        import voiceforge_lite.library as library
        self.lib = importlib.reload(library)
        (Path(self.temp.name) / "effects").mkdir()
        (Path(self.temp.name) / "effects" / "original.wav").write_bytes(b"placeholder")

    def test_path_traversal_blocked(self):
        with self.assertRaises(ValueError):
            self.lib.resolve_asset("../secret.wav")

    def test_absolute_path_blocked(self):
        with self.assertRaises(ValueError):
            self.lib.resolve_asset("/etc/passwd")

    def test_requires_rights_note(self):
        with self.assertRaises(ValueError):
            self.lib.register_asset("fight01", "effects/original.wav", "effect", "")

    def test_unapproved_hidden_by_default(self):
        self.lib.register_asset("fight01", "effects/original.wav", "effect", "Original recording")
        self.assertEqual(self.lib.list_assets(), {})
        self.assertIn("fight01", self.lib.list_assets(approved_only=False))

    def test_approved_asset_visible(self):
        self.lib.register_asset("fight01", "effects/original.wav", "effect",
                                "Original recording cleared for publication", True)
        self.assertIn("fight01", self.lib.list_assets())
        with self.assertRaises(ValueError):
            self.lib.register_asset("fight01", "effects/original.wav", "effect",
                                    "Original recording", True)

    def test_no_external_file_registration(self):
        with self.assertRaises(ValueError):
            self.lib.register_asset("fight01", "../other.wav", "effect", "Permission granted", True)


if __name__ == "__main__":
    unittest.main()
