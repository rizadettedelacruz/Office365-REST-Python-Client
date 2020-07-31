from unittest import TestCase
from office365.runtime.auth.clientCredential import ClientCredential
from settings import settings
from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.webs.web import Web
from office365.sharepoint.lists.list_creation_information import ListCreationInformation


class SPTestCase(TestCase):
    """SharePoint specific test case base class"""

    client = None
    client_id = settings.get('client_credentials').get('client_id')
    client_secret = settings.get('client_credentials').get('client_secret')
    site_url = settings.get('url')

    @classmethod
    def setUpClass(cls):
        ctx_auth = AuthenticationContext(url=cls.site_url)
        ctx_auth.acquire_token_for_app(client_id=cls.client_id,
                                       client_secret=cls.client_secret)
        cls.client = ClientContext(settings['url'], ctx_auth)

    @property
    def credentials(self):
        return ClientCredential(self.client_id, self.client_secret)

    @staticmethod
    def create_list(web, list_properties):
        """

        :param Web web:
        :param ListCreationInformation list_properties:
        :return: List
        """
        ctx = web.context
        list_obj = web.lists.add(list_properties)
        ctx.execute_query()
        return list_obj

    @staticmethod
    def ensure_list(web, list_properties):
        """

        :param Web web:
        :param ListCreationInformation list_properties:
        :return: List
        """
        ctx = web.context
        lists = web.lists.filter(f"Title eq '{list_properties.Title}'")
        ctx.load(lists)
        ctx.execute_query()
        if len(lists) == 1:
            return lists[0]
        return SPTestCase.create_list(web, list_properties)

    @staticmethod
    def read_file_as_text(path):
        with open(path) as content_file:
            file_content = content_file.read()
        return file_content

    @staticmethod
    def read_file_as_binary(path):
        with open(path, 'rb') as content_file:
            file_content = content_file.read()
        return file_content
