from unittest import TestCase

from office365.directory.domains.domain import Domain
from office365.graph_client import GraphClient
from tests.graph_case import acquire_token_by_client_credentials


class TestDomain(TestCase):
    """Tests for Azure Active Directory (Azure AD) domains"""

    target_domain = None  # type: Domain

    @classmethod
    def setUpClass(cls):
        cls.client = GraphClient(acquire_token_by_client_credentials)

    def test1_list_domains(self):
        domains = self.client.domains.top(1).get().execute_query()
        self.assertIsNotNone(domains.resource_path)
        self.assertEqual(len(domains), 1)
        self.__class__.target_domain = domains[0]

    # def test2_verify_domain(self):
    #    domain = self.__class__.target_domain.verify().execute_query()
    #    self.assertIsNotNone(domain.resource_path)
