from office365.runtime.client_object import ClientObject
from office365.runtime.odata.odata_query_options import QueryOptions
from office365.runtime.queries.client_query import ClientQuery


class ReadEntityQuery(ClientQuery):
    def __init__(self, entity_to_read, properties_to_include=None):
        """
        Read entity query

        :type properties_to_include: list[str] or None
        :type entity_to_read: office365.runtime.client_object.ClientObject
        """
        super().__init__(entity_to_read.context, entity_to_read, None, None, entity_to_read)
        self._properties_to_include = properties_to_include

    def build_url(self):
        url = super().build_url()
        if self._properties_to_include:
            url += "?" + self._build_query_url()
        return url

    def _build_query_url(self):
        query = QueryOptions()
        for n in self._properties_to_include:
            prop_val = self._binding_type.get_property(n)
            if isinstance(prop_val, ClientObject):
                query.expand.append(n)
            query.select.append(n)
        return query.to_url()
