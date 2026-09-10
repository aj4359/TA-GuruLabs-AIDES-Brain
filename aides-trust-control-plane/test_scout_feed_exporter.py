import json
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path

from moat import OutcomeStatus
from scout_feed_exporter import export_public_feed
from scout_mission_feed import sanitised_scout_example


class ScoutFeedExporterTests(unittest.TestCase):
    def test_exports_versioned_sanitised_payload(self):
        feed = sanitised_scout_example()
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "feed.json"
            payload = export_public_feed(feed, path, feed_mode="SANITISED_DEMO", stage_details={"VERIFY": "Fresh-context verification"})
            written = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(payload, written)
        self.assertEqual(written["schema_version"], "1.0")
        self.assertEqual(written["feed_mode"], "SANITISED_DEMO")
        self.assertEqual(written["stages"][4]["detail"], "Fresh-context verification")
        self.assertIsNone(written["verified_value_gbp"])

    def test_operational_mode_is_explicitly_supported(self):
        feed = sanitised_scout_example()
        with tempfile.TemporaryDirectory() as directory:
            payload = export_public_feed(feed, Path(directory) / "feed.json", feed_mode="RECORDED_OPERATIONAL")
        self.assertEqual(payload["feed_mode"], "RECORDED_OPERATIONAL")

    def test_unrecognised_mode_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(ValueError, "unsupported public feed mode"):
                export_public_feed(sanitised_scout_example(), Path(directory) / "feed.json", feed_mode="LIVE")

    def test_invalid_feed_fails_before_write(self):
        bad = replace(sanitised_scout_example(), outcome_status=OutcomeStatus.UNKNOWN, verified_value_gbp=__import__('decimal').Decimal("100"))
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "feed.json"
            with self.assertRaisesRegex(ValueError, "unknown outcome"):
                export_public_feed(bad, path, feed_mode="RECORDED_OPERATIONAL")
            self.assertFalse(path.exists())


if __name__ == "__main__":
    unittest.main()
