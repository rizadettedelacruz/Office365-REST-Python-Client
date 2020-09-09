from unittest import TestCase

from settings import settings

from office365.runtime.auth.user_credential import UserCredential
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.directory.directorySession import DirectorySession


class TestDirectorySession(TestCase):
    session = None  # type: DirectorySession

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        user_credentials = UserCredential(settings['user_credentials']['username'],
                                          settings['user_credentials']['password'])
        cls.client = ClientContext(settings['url']).with_credentials(user_credentials)
        cls.session = DirectorySession(cls.client)

    def test_1_init_session(self):
        session = self.__class__.session.get().execute_query()
        self.assertIsInstance(session, DirectorySession)

    def test_2_get_me(self):
        me = self.__class__.session.me().get().execute_query()
        self.assertIsNotNone(me.resource_path)
