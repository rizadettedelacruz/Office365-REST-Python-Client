import os
import tempfile

from office365.runtime.auth.clientCredential import ClientCredential
from office365.sharepoint.client_context import ClientContext
from settings import settings

ctx = ClientContext(settings['url']).with_credentials(
    ClientCredential(settings['client_credentials']['client_id'],
                     settings['client_credentials']['client_secret']))

# retrieve files from library
source_folder = ctx.web.lists.get_by_title("Documents").rootFolder
files = source_folder.files
ctx.load(files)
ctx.execute_query()
download_path = tempfile.mkdtemp()
for file in files:
    print("Downloading file: {} ...".format(file.properties["ServerRelativeUrl"]))
    download_file_name = os.path.join(download_path, os.path.basename(file.properties["Name"]))
    with open(download_file_name, "wb") as local_file:
        file.download(local_file)
        ctx.execute_query()
    print(f"[Ok] file has been downloaded: {download_file_name}")
