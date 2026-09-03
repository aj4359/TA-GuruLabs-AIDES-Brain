import unittest

from session_policy import ParticipantConsent, SessionPolicy
from speech_adapter import ConsentRequiredError, SpeechSegment, transcribe_with_policy


class FakeProvider:
    provider_name = "fake"

    def __init__(self):
        self.called = False

    def transcribe(self, audio_chunks):
        self.called = True
        list(audio_chunks)
        return [
            SpeechSegment("speaker-a", "hello", 0, 500),
            SpeechSegment("speaker-b", "hi", 600, 900),
        ]


class SpeechAdapterTests(unittest.TestCase):
    def test_provider_is_not_called_without_unanimous_consent(self):
        policy = SessionPolicy(participants=(
            ParticipantConsent("a", True),
            ParticipantConsent("b", False),
        ))
        provider = FakeProvider()

        with self.assertRaises(ConsentRequiredError):
            transcribe_with_policy(policy, provider, [b"ephemeral-audio"])

        self.assertFalse(provider.called)

    def test_provider_runs_after_unanimous_consent(self):
        policy = SessionPolicy(participants=(
            ParticipantConsent("a", True),
            ParticipantConsent("b", True),
        ))
        provider = FakeProvider()

        segments = transcribe_with_policy(policy, provider, [b"ephemeral-audio"])

        self.assertTrue(provider.called)
        self.assertEqual(len(segments), 2)
        self.assertEqual(segments[0].speaker_id, "speaker-a")


if __name__ == "__main__":
    unittest.main()
