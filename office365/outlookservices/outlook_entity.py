from office365.runtime.client_object import ClientObject
from office365.runtime.queries.delete_entity_query import DeleteEntityQuery
from office365.runtime.queries.update_entity_query import UpdateEntityQuery
from office365.runtime.resource_path import ResourcePath


class OutlookEntity(ClientObject):
    """Base Outlook entity."""

    def update(self):
        qry = UpdateEntityQuery(self)
        self.context.add_query(qry)
        return self

    def delete_object(self):
        """Deletes the outlook entity."""
        qry = DeleteEntityQuery(self)
        self.context.add_query(qry)
        return self

    def set_property(self, name, value, persist_changes=True):
        super().set_property(name, value, persist_changes)
        # fallback: create a new resource path
        if name.lower() == "id":
            self._resource_path = ResourcePath(
                value,
                self._parent_collection.resource_path)
        return self
