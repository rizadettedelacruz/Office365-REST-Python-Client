from settings import settings
from tests.sharepoint.sharepoint_case import SPTestCase

from office365.sharepoint.changes.change_query import ChangeQuery
from office365.sharepoint.permissions.basePermissions import BasePermissions
from office365.sharepoint.principal.user import User


class TestSharePointUser(SPTestCase):
    target_user = None  # type: User

    def test1_get_current_user(self):
        user = self.client.web.currentUser.get().execute_query()
        self.assertIsNotNone(user.login_name, "Current user was not requested")
        self.assertIsInstance(user.id, int)
        self.__class__.target_user = user

    def test2_ensure_user(self):
        result_user = self.client.web.ensure_user(self.__class__.target_user.login_name).execute_query()
        self.assertIsNotNone(result_user.user_id)

    def test3_get_user(self):
        target_user = self.client.web.siteUsers.get_by_login_name(self.__class__.target_user.login_name)\
            .get().execute_query()
        self.assertIsNotNone(target_user.id)

    def test4_update_user(self):
        user_to_update = self.__class__.target_user
        user_to_update.set_property("Email", "support@{0}".format(settings["tenant"])).update().execute_query()

    def test5_get_user_permissions(self):
        perms_result = self.client.web.get_user_effective_permissions(self.__class__.target_user.login_name)
        self.client.execute_query()
        self.assertIsInstance(perms_result.value, BasePermissions)

    def test6_get_user_changes(self):
        changes = self.client.site.get_changes(ChangeQuery(user=True)).execute_query()
        self.assertGreater(len(changes), 0)
