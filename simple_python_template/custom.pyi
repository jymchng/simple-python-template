class Custom:
    """
    Custom objects that hold a first name, last name, and a custom number.
    """

    def __init__(self, first: str = "", last: str = "", number: int = 0) -> None: ...

    first: str
    last: str
    number: int

    def name(self) -> str:
        """
        Return the name, combining the first and last name.
        """
        ...

CUSTOM_GLOBAL: str
