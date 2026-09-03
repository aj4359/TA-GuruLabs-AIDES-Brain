import unittest

from session_policy import ParticipantConsent, SessionPolicy, enforce_session_start, retention_decision


class SessionPolicyTests(unittest.TestCase):
    def test_capture_denied_without_unanimous_consent(self):
        policy = SessionPolicy(participants=(
            ParticipantConsent("a", True),
            ParticipantConsent("b", False),
        ))
        self.assertEqual(enforce_session_start(policy)["decision"], "deny")

    def test_capture_allowed_with_unanimous_consent(self):
        policy = SessionPolicy(participants=(
            ParticipantConsent("a", True),
            ParticipantConsent("b", True),
        ))
        result = enforce_session_start(policy)
        self.assertEqual(result["decision"], "allow")
        self.assertEqual(result["memory_scope"], "aegis_isolated")

    def test_raw_audio_and_transcript_are_ephemeral(self):
        policy = SessionPolicy(participants=(ParticipantConsent("a", True, True),))
        decision = retention_decision(policy)
        self.assertEqual(decision["raw_audio"], "delete_after_session")
        self.assertEqual(decision["transcript"], "delete_after_session")

    def test_summary_retention_requires_all_participants_to_opt_in(self):
        policy = SessionPolicy(participants=(
            ParticipantConsent("a", True, True),
            ParticipantConsent("b", True, False),
        ))
        self.assertEqual(retention_decision(policy)["derived_summary"], "delete_after_session")

    def test_summary_can_be_retained_after_unanimous_opt_in(self):
        policy = SessionPolicy(participants=(
            ParticipantConsent("a", True, True),
            ParticipantConsent("b", True, True),
        ))
        self.assertEqual(retention_decision(policy)["derived_summary"], "retain")


if __name__ == "__main__":
    unittest.main()
