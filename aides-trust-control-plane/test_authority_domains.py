import unittest

from authority_domains import AuthorityDomains, evaluate_deployment_authority


class AuthorityDomainTests(unittest.TestCase):
    def setUp(self):
        self.domains = AuthorityDomains(
            developer_id="ta-gurulabs",
            developer_controls_ref="build-proof-001",
            deployer_id="customer-operator",
            deployment_context="procurement-research",
            permitted_actions=frozenset({"research_public_information", "create_internal_recommendation"}),
        )

    def test_authorised_deployment_action_is_allowed(self):
        result = evaluate_deployment_authority(self.domains, "research_public_information")
        self.assertEqual(result["decision"], "allow")

    def test_technical_capability_does_not_imply_deployment_authority(self):
        result = evaluate_deployment_authority(self.domains, "contact_external_party")
        self.assertEqual(result["decision"], "deny")
        self.assertIn("does not confer", result["reason"])


if __name__ == "__main__":
    unittest.main()
