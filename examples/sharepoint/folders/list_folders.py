from office365.sharepoint.client_context import ClientContext
from tests import test_client_credentials, test_team_site_url

ctx = ClientContext(test_team_site_url).with_credentials(test_client_credentials)


def enum_folder(parent_folder, action):
    """
    :type parent_folder: Folder
    :type action: (Folder)-> None
    """
    parent_folder.expand(["Folders"]).get().execute_query()
    action(parent_folder)
    for folder in parent_folder.folders:
        enum_folder(folder, action)


def print_folder_stat(folder):
    # type: (Folder) -> None
    print(folder.serverRelativeUrl)
    print(folder.time_created)


root_folder = ctx.web.default_document_library().root_folder
enum_folder(root_folder, print_folder_stat)
