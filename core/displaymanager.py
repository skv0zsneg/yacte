import curses
import logging
from curses import wrapper
from typing import TYPE_CHECKING

from .entities import Coord, Row, Window
from .filemanager import read_file

if TYPE_CHECKING:
    from curses import _CursesWindow

logging.basicConfig(filename="./pycte.log", level=logging.DEBUG)


class DisplayManager:
    def __init__(self) -> None:
        self.file_path: str
        self.window: Window
        self.curses_win: '_CursesWindow'

        self._start_row_n = 0
        self._full_displayed_rows = 0

    def launch(self, file_path: str) -> None:
        self.file_path = file_path
        self.window = self._create_window(read_file(file_path))
        wrapper(self._main_loop)

    def _create_window(self, rows: list[Row]) -> Window:
        win = Window(rows=[])
        for row in rows:
            row._window_ref = win
            for symbol in row.symbols:
                symbol._row_ref = row
            win.rows.append(row)
        return win

    def _main_loop(self, curses_win: '_CursesWindow') -> None:
        self.curses_win = curses_win

        self.curses_win.clear()
        curses.use_default_colors()
        self._display_sys_info_board()
        self._display_file_info()
        self._display_text()
        self._move_cursor_to_begin()

        while True:
            self.curses_win.refresh()
            self._action_handler(
                key=curses_win.getch(),
                symbol_cursor_on=curses_win.inch(),
            )

    def _action_handler(self, key: int, symbol_cursor_on: int) -> None:
        if key == ord('q'):
            self._exit()
        elif key == curses.KEY_RESIZE:
            self._resize()
        elif key == curses.KEY_RIGHT:
            self._move_right()
        elif key == curses.KEY_LEFT:
            self._move_left()
        elif key == curses.KEY_DOWN:
            self._move_down()
        elif key == curses.KEY_UP:
            self._move_up()
        elif key == curses.KEY_BACKSPACE:
            self._delch()
        else:
            try:
                self.curses_win.insch(chr(key))
            except OverflowError:
                pass

    # actions

    def _display_sys_info_board(self) -> None:
        _, max_x = self.curses_win.getmaxyx()
        self.curses_win.addstr(1, 0, "─"*max_x)

    def _display_file_info(self) -> None:
        self.curses_win.addstr(0, 0, f"{self.file_path}", curses.A_BOLD)

    def _display_text(self) -> None:
        self._clear_text()
        self._full_displayed_rows = 0

        max_y, max_x = self.curses_win.getmaxyx()
        ptr_x, ptr_y = 0, 1
        row_gen = self.window.next_row(self._start_row_n)
        is_symbols_finished = True

        while ptr_y < max_y-1:
            try:
                if is_symbols_finished:
                    row = next(row_gen)
                    ptr_y += 1
                    ptr_x = 0
            except StopIteration:
                return

            if is_symbols_finished:
                symbol_gen = row.next_symbol()
                is_symbols_finished = False
            try:
                symbol = next(symbol_gen)
            except StopIteration:
                is_symbols_finished = True
                self._full_displayed_rows += 1
                continue

            try:
                self.curses_win.addch(ptr_y, ptr_x, symbol.ch)
                symbol.coord = Coord(x=ptr_x, y=ptr_y)
            except curses.error:
                pass

            if ptr_x == max_x-1:
                ptr_y += 1
                ptr_x = 0
            else:
                ptr_x += 1

    def _exit(self) -> None:
        exit(1)

    def _resize(self) -> None:
        self.curses_win.clear()
        self._display_sys_info_board()
        self._display_file_info()
        self._display_text()

    def _move_right(self) -> None:
        current_y, current_x = self.curses_win.getyx()
        try:
            _, max_x = self.curses_win.getmaxyx()
            if current_x == max_x-1:
                self.curses_win.move(current_y+1, 0)
            if (
                current_x+1 in self.window.text_coords_x and
                current_y in self.window.text_coords_y
            ):
                self.curses_win.move(current_y, current_x+1)
        except curses.error:
            pass

    def _move_left(self) -> None:
        current_y, current_x = self.curses_win.getyx()
        try:
            if current_x == 0 and current_y != 2:
                _, max_x = self.curses_win.getmaxyx()
                self.curses_win.move(current_y-1, max_x-1)
            elif (
                current_x-1 in self.window.text_coords_x and
                current_y in self.window.text_coords_y
            ):
                self.curses_win.move(current_y, current_x-1)
        except curses.error:
            pass

    def _move_up(self) -> None:
        current_y, current_x = self.curses_win.getyx()
        try:
            if current_y != 2:
                if (
                    current_x in self.window.text_coords_x and
                    current_y-1 in self.window.text_coords_y
                ):
                    self.curses_win.move(current_y-1, current_x)
            elif current_y == 2 and self._start_row_n != 0:
                self._start_row_n -= 1
                self._display_text()
        except curses.error:
            pass

    def _move_down(self) -> None:
        current_y, current_x = self.curses_win.getyx()
        max_y, _ = self.curses_win.getmaxyx()
        try:
            if (
                current_x in self.window.text_coords_x and
                current_y+1 in self.window.text_coords_y
            ):
                self.curses_win.move(current_y+1, current_x)
            elif (
                current_y == max_y - 2 and
                self._full_displayed_rows < len(self.window.rows) - 1
            ):
                self._start_row_n += 1
                self._clear_text()
                self._display_text()
                # TODO: realize scroll down
                self.curses_win.move(max_y - 2, curses.COLS+5)
        except curses.error:
            pass

    def _delch(self):
        current_y, current_x = self.curses_win.getyx()
        try:
            self.curses_win.delch(current_y, current_x-1)
            if current_x-1 == 0:
                self._move_left()
        except curses.error:
            pass

    def _clear_text(self):
        self.curses_win.move(2, 0)
        self.curses_win.clrtoeol()

    def _move_cursor_to_begin(self):
        self.curses_win.move(2, 0)
