import curses
import logging
from curses import wrapper
from typing import TYPE_CHECKING

from .entities import Coord, Row, Window
from .filemanager import read_file

if TYPE_CHECKING:
    from curses import _CursesWindow

logging.basicConfig(filename="./yacte.log", level=logging.DEBUG)


class DisplayManager:
    def __init__(self) -> None:
        self.file_path: str
        self.window: Window
        self.curses_win: '_CursesWindow'

        self._start_row_number = 0
        self._displayed_rows: list[Row] = []

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
        self._full_window_refresh()
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
        try:
            self.curses_win.addstr(1, 0, "─"*max_x)
        except curses.error:
            pass

    def _display_file_info(self) -> None:
        try:
            self.curses_win.addstr(0, 0, f"{self.file_path}", curses.A_BOLD)
        except curses.error:
            pass

    def _display_text(self) -> None:
        self._clear_text()

        self._displayed_rows = []
        self.window.text_coords = []
        max_y, max_x = self.curses_win.getmaxyx()
        ptr_x, ptr_y = 0, 1
        row_gen = self.window.next_row(self._start_row_number)
        is_symbols_finished = True

        while ptr_y < max_y-1:
            try:
                if is_symbols_finished:
                    row = next(row_gen)
                    ptr_y += 1
                    ptr_x = 0
                    self._displayed_rows.append(row)
            except StopIteration:
                return

            if is_symbols_finished:
                symbol_gen = row.next_symbol()
                is_symbols_finished = False
            try:
                symbol = next(symbol_gen)
            except StopIteration:
                is_symbols_finished = True
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
        self._full_window_refresh()

    def _move_right(self) -> None:
        current_y, current_x = self.curses_win.getyx()
        try:
            _, max_x = self.curses_win.getmaxyx()
            if (
                current_x == max_x-1 or
                not self.window.is_coord_exist(current_x+1, current_y)
            ):
                if self.window.is_coord_exist(0, current_y+1):
                    self.curses_win.move(current_y+1, 0)
            elif self.window.is_coord_exist(current_x+1, current_y):
                self.curses_win.move(current_y, current_x+1)
        except curses.error:
            pass

    def _move_left(self) -> None:
        current_y, current_x = self.curses_win.getyx()
        try:
            if current_x == 0 and current_y != 2:
                _, max_x = self.curses_win.getmaxyx()
                new_x, new_y = max_x-1, current_y-1
                while not self.window.is_coord_exist(new_x, new_y):
                    new_x -= 1
                self.curses_win.move(new_y, new_x)
            elif self.window.is_coord_exist(current_x-1, current_y):
                self.curses_win.move(current_y, current_x-1)
        except curses.error:
            pass

    def _move_up(self) -> None:
        current_y, current_x = self.curses_win.getyx()
        try:
            if current_y != 2:
                new_x, new_y = current_x, current_y-1
                while not self.window.is_coord_exist(new_x, new_y):
                    new_x -= 1
                self.curses_win.move(new_y, new_x)
            elif current_y == 2 and self._start_row_number != 0:
                self._start_row_number -= 1
                self._display_text()

                first_row_first_symbol = self._displayed_rows[0].symbols[0]
                self.curses_win.move(
                    first_row_first_symbol.coord.y,
                    first_row_first_symbol.coord.x,
                )
        except curses.error:
            pass

    def _move_down(self) -> None:
        current_y, current_x = self.curses_win.getyx()
        max_y, _ = self.curses_win.getmaxyx()
        try:
            if current_y+1 != max_y-1:
                new_x, new_y = current_x, current_y+1
                while (not self.window.is_coord_exist(new_x, new_y) and
                       new_x >= 0):
                    new_x -= 1
                self.curses_win.move(new_y, new_x)
            elif self._start_row_number + 1 < len(self.window.rows) - 1:
                self._start_row_number += 1
                self._display_text()
                self.curses_win.refresh()

                last_row_first_symbol = self._displayed_rows[-1].symbols[0]
                self.curses_win.move(
                    last_row_first_symbol.coord.y,
                    last_row_first_symbol.coord.x,
                )
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
        self.curses_win.clear()
        self._display_sys_info_board()
        self._display_file_info()
        self.curses_win.refresh()

    def _move_cursor_to_begin(self):
        self.curses_win.move(2, 0)

    def _full_window_refresh(self):
        self.curses_win.clear()
        self._display_sys_info_board()
        self._display_file_info()
        self._display_text()
        self.curses_win.refresh()
