from office365.sharepoint.webs.web import Web
from tests.sharepoint.sharepoint_case import SPTestCase


class TestClientSideComponent(SPTestCase):
    target_web = None  # type: Web

    @classmethod
    def setUpClass(cls):
        super(TestClientSideComponent, cls).setUpClass()

    def test1_get_all_client_side_components(self):
        result = self.client.web.get_all_client_side_components().execute_query()
        self.assertIsNotNone(result.value)

    def test2_get_client_side_web_parts(self):
        result = self.client.web.get_client_side_web_parts().execute_query()
        self.assertIsNotNone(result.value)
