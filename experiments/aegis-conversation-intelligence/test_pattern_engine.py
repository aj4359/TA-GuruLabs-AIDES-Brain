import unittest

from pattern_engine import Segment, extract_patterns, render_neutral_observations


class PatternEngineTests(unittest.TestCase):
    def test_structural_metrics_are_deterministic(self):
        segments = [
            Segment("a", 0.0, 4.0, "How was your day?"),
            Segment("b", 3.5, 6.0, "Busy, but good."),
            Segment("a", 10.0, 12.0, "What made it good?"),
        ]
        result = extract_patterns(segments, long_silence_seconds=3.0)
        self.assertEqual(result["turn_counts"], {"a": 2, "b": 1})
        self.assertEqual(result["question_counts"], {"a": 2, "b": 0})
        self.assertEqual(result["overlap_count"], 1)
        self.assertEqual(result["long_silence_count"], 1)
        self.assertEqual(result["speaker_switch_count"], 2)

    def test_invalid_segment_is_rejected(self):
        with self.assertRaises(ValueError):
            extract_patterns([Segment("a", 5.0, 4.0, "bad timing")])

    def test_empty_conversation_returns_neutral_zero_state(self):
        result = extract_patterns([])
        self.assertEqual(result["total_segments"], 0)
        self.assertEqual(result["talk_time_share"], {})

    def test_observations_are_descriptive_not_diagnostic(self):
        result = extract_patterns([
            Segment("a", 0.0, 2.0, "Hello?"),
            Segment("b", 2.5, 5.5, "Hi there."),
        ])
        text = " ".join(render_neutral_observations(result)).lower()
        prohibited = ["toxic", "dishonest", "compatible", "depressed", "anxious", "healthy relationship"]
        for term in prohibited:
            self.assertNotIn(term, text)


if __name__ == "__main__":
    unittest.main()
