import datetime

from office365.runtime.paths.resource_path import ResourcePath
from office365.sharepoint.entity import Entity


class ListItemVersion(Entity):
    """Represents a version of a list item."""

    @property
    def version_id(self):
        """Gets the ID of the version."""
        return int(self.properties.get("VersionId", -1))

    @property
    def version_label(self):
        """Gets the version number of the item version.
        :rtype: str or None
        """
        return self.properties.get("VersionLabel", None)

    @property
    def is_current_version(self):
        """Gets a value that specifies whether the file version is the current version.
        :rtype: bool
        """
        return self.properties.get("IsCurrentVersion", None)

    @property
    def created(self):
        """Gets the creation date and time for the item version."""
        return self.properties.get("Created", datetime.datetime.min)

    @property
    def created_by(self):
        """Gets the user that created the item version."""
        from office365.sharepoint.principal.users.user import User

        return self.properties.get(
            "CreatedBy",
            User(self.context, ResourcePath("CreatedBy", self.resource_path)),
        )

    @property
    def fields(self):
        """Gets the collection of fields that are used in the list that contains the item version."""
        from office365.sharepoint.fields.collection import FieldCollection

        return self.properties.get(
            "Fields",
            FieldCollection(self.context, ResourcePath("Fields", self.resource_path)),
        )

    @property
    def file_version(self):
        """"""
        from office365.sharepoint.files.versions.version import FileVersion

        return self.properties.get(
            "FileVersion",
            FileVersion(self.context, ResourcePath("FileVersion", self.resource_path)),
        )

    @property
    def property_ref_name(self):
        return "VersionId"

    @property
    def parent_collection(self):
        """
        :rtype: office365.sharepoint.listitems.versions.collection.ListItemVersionCollection
        """
        return self._parent_collection

    def get_property(self, name, default_value=None):
        if default_value is None:
            property_mapping = {
                "CreatedBy": self.created_by,
                "FileVersion": self.file_version,
            }
            default_value = property_mapping.get(name, None)
        return super(ListItemVersion, self).get_property(name, default_value)

    def set_property(self, name, value, persist_changes=True):
        if self._resource_path is None:
            if name == "VersionId":
                self._resource_path = self.parent_collection.get_by_id(
                    value
                ).resource_path
        return super(ListItemVersion, self).set_property(name, value, persist_changes)
