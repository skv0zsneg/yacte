from .models import Cursor, Terminal


def create_terminal(width: int, length: int) -> Terminal:
    """Creating new terminal with empty content.

    :param size_x: Terminal width
    :param size_y: Terminal height
    :return: New terminal
    """
    content = None
    if width > 0 and length > 0:
        content = [[None for _ in range(width)] for _ in range(length)]

    new_terminal = Terminal(
        cursor=Cursor(0, 0),
        content=content,
    )
    return new_terminal
