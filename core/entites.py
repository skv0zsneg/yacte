from dataclasses import dataclass


@dataclass
class Row:
    symbols: str


@dataclass
class Text:
    rows: list[Row]
