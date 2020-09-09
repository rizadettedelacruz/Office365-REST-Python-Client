from urllib.parse import quote

from office365.entity import Entity
from office365.runtime.queries.delete_entity_query import DeleteEntityQuery
from office365.runtime.resource_path import ResourcePath
from office365.teams.chatMessageCollection import ChatMessageCollection
from office365.teams.teamsTabCollection import TeamsTabCollection


class Channel(Entity):
    """Teams are made up of channels, which are the conversations you have with your teammates"""

    def delete_object(self):
        """Deletes the channel."""
        qry = DeleteEntityQuery(self)
        self.context.add_query(qry)
        self.remove_from_parent_collection()
        return self

    @property
    def tabs(self):
        """A collection of all the tabs in the channel. A navigation property."""
        return self.properties.get('tabs',
                                   TeamsTabCollection(self.context, ResourcePath("tabs", self.resource_path)))

    @property
    def messages(self):
        """A collection of all the messages in the channel. A navigation property. Nullable."""
        return self.properties.get('messages',
                                   ChatMessageCollection(self.context, ResourcePath("messages", self.resource_path)))

    @property
    def web_url(self):
        """A hyperlink that will navigate to the channel in Microsoft Teams. This is the URL that you get when you
        right-click a channel in Microsoft Teams and select Get link to channel. This URL should be treated as an
        opaque blob, and not parsed. Read-only.

        :rtype: str or None """
        return self.properties.get('webUrl', None)

    def set_property(self, name, value, persist_changes=True):
        super().set_property(name, value, persist_changes)
        # fallback: fix resource path
        if name == "id":
            channel_id = quote(value)
            self._resource_path = ResourcePath(channel_id, self.resource_path.parent)
