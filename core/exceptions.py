class BaseYacteException(BaseException):
    pass


class TerminalException(BaseYacteException):
    pass


class TerminalContentIsEmpty(TerminalException):
    def __init__(self) -> None:
        super().__init__("Terminal content is empty")


class ContentPositionDoesntExist(TerminalException):
    def __init__(self) -> None:
        super().__init__("This content position does't exist")


class CantSetCursor(TerminalException):
    def __init__(self) -> None:
        super().__init__("Cannot set cursor")
