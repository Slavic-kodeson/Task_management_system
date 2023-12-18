class MakeItDict:
    def __init__(self, **kwargs):
        self.arguments = kwargs

    def __getattr__(self, item):
        raise NotImplementedError(item)

    def __getitem__(self, item):
        return self.arguments[item]


class CreateRegistrationCode(MakeItDict):
    """ Signature for SingleDispatch:
        Route: Create Registration Code """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class CheckRegistrationCode(MakeItDict):
    """ Signature for SingleDispatch:
        Route: Check Registration Code """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class RegisterAccount(MakeItDict):
    """Signature for SingleDispatch:
        Route: Register account """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class SettingsAccount(MakeItDict):
    """Signature For SingleDispatch:
        Route: Change settings for account"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
