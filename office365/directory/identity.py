from office365.runtime.client_value import ClientValue


class Identity(ClientValue):
    """The Identity resource represents an identity of an actor. For example, an actor can be a user, device,
    or application. """

    def __init__(self):
        super().__init__()
        self.displayName = None
        self.id = None
