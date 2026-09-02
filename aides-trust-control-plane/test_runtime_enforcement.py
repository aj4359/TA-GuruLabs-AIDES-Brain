import unittest

from runtime_enforcement import RuntimeContext, RuntimeEnforcer, RuntimeState


class RuntimeEnforcementTests(unittest.TestCase):
    def setUp(self):
        self.enforcer = RuntimeEnforcer()
        self.ctx = RuntimeContext(transaction_id="tx-1", actor_id="aide.scout.v1")

    def test_deny_blocks_only_requested_action(self):
        self.enforcer.deny(self.ctx, "contact_external_party", "policy breach")
        self.assertFalse(self.enforcer.can_execute(self.ctx, "contact_external_party"))
        self.assertTrue(self.enforcer.can_execute(self.ctx, "research_public_information"))

    def test_pause_blocks_execution(self):
        self.enforcer.pause(self.ctx, "human intervention")
        self.assertEqual(self.ctx.state, RuntimeState.PAUSED)
        self.assertFalse(self.enforcer.can_execute(self.ctx, "research_public_information"))

    def test_revoke_credentials_blocks_execution(self):
        self.enforcer.revoke_credentials(self.ctx, "credential risk")
        self.assertFalse(self.ctx.credentials_active)
        self.assertFalse(self.enforcer.can_execute(self.ctx, "research_public_information"))

    def test_quarantine_revokes_credentials(self):
        self.enforcer.quarantine(self.ctx, "anomalous behaviour")
        self.assertEqual(self.ctx.state, RuntimeState.QUARANTINED)
        self.assertFalse(self.ctx.credentials_active)
        self.assertFalse(self.enforcer.can_execute(self.ctx, "research_public_information"))

    def test_terminate_is_terminal(self):
        self.enforcer.terminate(self.ctx, "kill switch")
        self.enforcer.pause(self.ctx, "should not revive")
        self.assertEqual(self.ctx.state, RuntimeState.TERMINATED)
        self.assertFalse(self.enforcer.can_execute(self.ctx, "anything"))


if __name__ == "__main__":
    unittest.main()
