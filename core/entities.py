from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Coord:
    x: int
    y: int


@dataclass
class Symbol:
    ch: str

    _row_ref: Optional['Row'] = None
    _coord: Coord | None = None

    @property
    def coord(self) -> Coord | None:
        return self._coord

    @coord.setter
    def coord(self, value) -> None:
        if isinstance(value, Coord):
            self._coord = value
            self._row_ref._window_ref.text_coords.append(value)

    @coord.deleter
    def coord(self) -> None:
        self._coord = None


@dataclass
class Row:
    row_number: int
    symbols: list[Symbol]

    _window_ref: Optional['Window'] = None

    def next_symbol(self):
        for symbol in self.symbols:
            yield symbol


@dataclass
class Window:
    rows: list[Row]
    text_coords: list[Coord] = field(default_factory=list)

    def next_row(self, start_row_n: int):
        for row in self.rows[start_row_n:]:
            yield row

    def is_coord_exist(self, x: int, y: int) -> bool:
        for coord in self.text_coords:
            if coord.x == x and coord.y == y:
                return True
        return False
