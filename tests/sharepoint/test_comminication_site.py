import uuid
from unittest import TestCase

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.sites.site import Site
from office365.sharepoint.tenant.administration.tenant import Tenant
from tests import test_admin_site_url, test_root_site_url, test_user_credentials


class TestCommunicationSite(TestCase):
    target_site = None  # type: Site

    @classmethod
    def setUpClass(cls):
        super(TestCommunicationSite, cls).setUpClass()
        ctx = ClientContext(test_root_site_url).with_credentials(test_user_credentials)
        cls.client = ctx

    def test1_create_site(self):
        site_alias = "site{0}".format(uuid.uuid4().hex)
        comm_site = self.client.create_communication_site(
            site_alias, site_alias
        ).execute_query()
        self.assertIsNotNone(comm_site.resource_path)
        self.__class__.target_site = comm_site

    def test2_is_comm_site(self):
        result = self.__class__.target_site.is_comm_site().execute_query()
        self.assertIsNotNone(result.value)

    def test3_set_as_home_site(self):
        result = self.__class__.target_site.set_as_home_site().execute_query()
        self.assertIsNotNone(result.value)

    def test4_is_valid_home_site(self):
        result = self.__class__.target_site.is_valid_home_site().execute_query()
        self.assertIsNotNone(result.value)

    # def test5_get_home_details(self):
    #    result = self.client.home_site.details().execute_query()
    #    self.assertIsNotNone(result.value)

    def test7_register_hub_site(self):
        tenant = Tenant.from_url(test_admin_site_url).with_credentials(
            test_user_credentials
        )
        props = tenant.register_hub_site(self.__class__.target_site.url).execute_query()
        self.assertIsNotNone(props.site_id)
        site = self.__class__.target_site.get().execute_query()
        self.assertTrue(site.is_hub_site)

    def test8_unregister_hub_site(self):
        client_admin = ClientContext(test_admin_site_url).with_credentials(
            test_user_credentials
        )
        tenant = Tenant(client_admin)
        tenant.unregister_hub_site(self.__class__.target_site.url).execute_query()

    def test9_delete_site(self):
        self.__class__.target_site.delete_object().execute_query()
