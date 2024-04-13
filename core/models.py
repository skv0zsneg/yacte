from dataclasses import dataclass
from typing import Optional


@dataclass
class Terminal:
    cursor: 'Cursor'
    content: list[list[Optional['BaseSymbol']]]

    @property
    def size(self) -> tuple[int, int]:
        return len(self.content), len(self.content[0])

    @property
    def size_x(self) -> int:
        return len(self.content[0])

    @property
    def size_y(self) -> int:
        return len(self.content)


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
