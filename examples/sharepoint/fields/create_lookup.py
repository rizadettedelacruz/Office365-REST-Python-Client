"""
Demonstrates how to create lookup field
"""
from office365.sharepoint.client_context import ClientContext
from tests import create_unique_name, test_client_credentials, test_team_site_url

field_name = create_unique_name("MultilookupField")
client = ClientContext(test_team_site_url).with_credentials(test_client_credentials)
lookup_list = client.web.default_document_library()

field = client.web.fields.add_lookup_field(
    title=field_name,
    lookup_list=lookup_list,
    lookup_field_name="Title",
    allow_multiple_values=True,
).execute_query()
print("Field  {0} has been created", field.internal_name)
field.delete_object().execute_query()  # clean up
