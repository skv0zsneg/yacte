from dataclasses import dataclass

from .exceptions import (CantSetCursor, ContentPositionDoesntExist,
                         TerminalContentIsEmpty)


@dataclass
class Terminal:
    cursor: 'Cursor'
    content: list[list['BaseSymbol | None']] | None

    @property
    def size(self) -> tuple[int, int]:
        if self.content:
            return len(self.content), len(self.content[0])
        return 0, 0

    @property
    def width(self) -> int:
        if self.content:
            return len(self.content[0])
        return 0

    @property
    def length(self) -> int:
        if self.content:
            return len(self.content)
        return 0

    def fill_terminal(self, symbols: list['FileSymbol']) -> None:
        if not symbols or not self.content:
            return None

        term_ptr_x, term_ptr_y = 0, 0
        last_symbol_line = symbols[0].line
        for symbol in symbols:
            if last_symbol_line < symbol.line:
                term_ptr_y += symbol.line - last_symbol_line
                term_ptr_x = 0
            if term_ptr_x >= self.width:
                term_ptr_y += 1
                term_ptr_x = 0
            if term_ptr_y >= self.length:
                break

            self.content[term_ptr_y][term_ptr_x] = symbol

            term_ptr_x += 1
            last_symbol_line = symbol.line

    def cursor_set_position(self, x: int, y: int) -> None:
        if not self.content:
            raise TerminalContentIsEmpty()
        try:
            position = self.content[y][x]
        except IndexError:
            raise ContentPositionDoesntExist()

        if (
            position or
            (x == 0 and y > 0 and self.content[y-1][-1]) or
            (x > 0 and self.content[y][x-1])
        ):
            self.cursor.x = x
            self.cursor.y = y
        else:
            raise CantSetCursor()

    def cursor_move_right(self) -> None:
        pass

    def cursor_move_left(self) -> None:
        pass

    def cursor_move_down(self) -> None:
        pass

    def cursor_move_up(self) -> None:
        pass


@dataclass
class Cursor:
    x: int
    y: int


@dataclass
class BaseSymbol:
    ch: str


@dataclass
class FileSymbol(BaseSymbol):
    line: int
    column: int


@dataclass
class SystemSymbol(BaseSymbol):
    pass
