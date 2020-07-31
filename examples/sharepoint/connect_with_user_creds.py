from office365.runtime.auth.user_credential import UserCredential
from office365.sharepoint.client_context import ClientContext
from settings import settings

ctx = ClientContext.connect_with_credentials(settings["url"],
                                             UserCredential(settings['user_credentials']['username'],
                                                            settings['user_credentials']['password']))

web = ctx.web
ctx.load(web)
ctx.execute_query()
print(web.properties["Url"])
