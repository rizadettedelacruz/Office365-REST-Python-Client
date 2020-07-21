from office365.runtime.clientValue import ClientValue


class WebCreationInformation(ClientValue):
    """Represents metadata about site creation."""

    def __init__(self):
        super().__init__()
        self.Title = None
        self.Url = None

    @property
    def entity_type_name(self):
        return "SP.WebCreationInformation"
