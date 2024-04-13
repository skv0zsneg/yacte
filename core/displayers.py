import curses
from abc import abstractmethod
from typing import TYPE_CHECKING

from .file_reader import FileReader
from .models import Terminal
from .repositories import create_terminal

if TYPE_CHECKING:
    from curses import _CursesWindow


class BaseDisplayer:
    """Base implementation of terminal display."""
    @abstractmethod
    def launch(self) -> None:
        """Enter point of displayer.

        :param file_path: Path to file.
        """
        pass


class LinuxDisplayer(BaseDisplayer):
    def __init__(self, file_reader: FileReader) -> None:
        self._file_reader: FileReader = file_reader
        self._terminal: Terminal | None = None
        self._screen: '_CursesWindow | None' = None

    def launch(self) -> None:
        curses.wrapper(self._curse_wrapper)

    def _curse_wrapper(self, screen: '_CursesWindow'):
        self._screen = screen

        self._screen.clear()
        self._screen.refresh()
        max_curse_y, max_curse_x = self._screen.getmaxyx()
        self._terminal = create_terminal(max_curse_x, max_curse_y)
        self._terminal.fill_terminal(self._file_reader.read_all())
        self._display_terminal_content()
        self._screen.move(self._terminal.cursor.y, self._terminal.cursor.x)

        while True:
            self._screen.refresh()
            self._action_handlers(
                key=self._screen.getch(),
                symbol_cursor_on=self._screen.inch(),
            )

    def _action_handlers(self, key: int, symbol_cursor_on: int):
        if key == ord('q'):
            self._exit()
        elif key == curses.KEY_RESIZE:
            self._resize()

    def _display_terminal_content(self) -> None:
        if not self._terminal:
            raise ValueError("Terminal is not initialized.")
        if not self._terminal.content:
            raise ValueError("Terminal content is empty.")

        for x in range(self._terminal.width):
            for y in range(self._terminal.length):
                if symbol := self._terminal.content[y][x]:
                    try:
                        self._screen.addch(y, x, symbol.ch)
                    except curses.error:
                        continue

    # actions

    def _exit(self):
        exit(1)

    def _resize(self):
        if not self._screen:
            raise ValueError("Curse window object is't created.")

        self._screen.clear()
        max_curse_y, max_curse_x = self._screen.getmaxyx()
        self._terminal = create_terminal(max_curse_x, max_curse_y)
        self._terminal.fill_terminal(self._file_reader.read_all())
        self._display_terminal_content()
        self._screen.refresh()