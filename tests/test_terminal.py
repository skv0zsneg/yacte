import sys

import pytest

sys.path.insert(0, "core")

from core.models import Cursor, FileSymbol, Terminal
from core.repositories import fill_terminal


class TestTerminalActions:
    @pytest.fixture
    def empty_terminal_5_x_5(self):
        return Terminal(
            cursor=Cursor(x=0, y=0),
            content=[[None for _ in range(5)] for _ in range(5)],
        )

    @pytest.fixture
    def empty_terminal_2_x_2(self):
        return Terminal(
            cursor=Cursor(x=0, y=0),
            content=[[None for _ in range(2)] for _ in range(2)],
        )

    def test_perfect_terminal_fill(self, empty_terminal_5_x_5):
        upd_terminal = fill_terminal(
            empty_terminal_5_x_5,
            [
                FileSymbol('H', column=0, line=0),
                FileSymbol('i', column=1, line=0),
                FileSymbol('!', column=2, line=0),
                FileSymbol('\n', column=0, line=1),
                FileSymbol('U', column=0, line=2),
                FileSymbol(' ', column=1, line=2),
                FileSymbol('o', column=2, line=2),
                FileSymbol('k', column=3, line=2),
                FileSymbol('?', column=4, line=2),
            ]
        )

        assert upd_terminal.content == [
            [
                FileSymbol('H', column=0, line=0),
                FileSymbol('i', column=1, line=0),
                FileSymbol('!', column=2, line=0),
                None,
                None,
            ],
            [
                FileSymbol('\n', column=0, line=1),
                None,
                None,
                None,
                None,
            ],
            [
                FileSymbol('U', column=0, line=2),
                FileSymbol(' ', column=1, line=2),
                FileSymbol('o', column=2, line=2),
                FileSymbol('k', column=3, line=2),
                FileSymbol('?', column=4, line=2),
            ],
            [None, None, None, None, None],
            [None, None, None, None, None],
        ]

    def test_multi_lines_terminal_fill(self, empty_terminal_5_x_5):
        upd_terminal = fill_terminal(
            empty_terminal_5_x_5,
            [
                FileSymbol("I", line=0, column=0),
                FileSymbol("'", line=1, column=0),
                FileSymbol("m", line=2, column=0),
                FileSymbol(" ", line=3, column=0),
                FileSymbol("T", line=4, column=0),
                FileSymbol("o", line=5, column=0),
                FileSymbol("o", line=6, column=0),
                FileSymbol(" ", line=7, column=0),
                FileSymbol("b", line=8, column=0),
                FileSymbol("i", line=9, column=0),
                FileSymbol("g", line=10, column=0),
            ]
        )

        assert upd_terminal.content == [
            [FileSymbol("I", line=0, column=0), None, None, None, None],
            [FileSymbol("'", line=1, column=0), None, None, None, None],
            [FileSymbol("m", line=2, column=0), None, None, None, None],
            [FileSymbol(" ", line=3, column=0), None, None, None, None],
            [FileSymbol("T", line=4, column=0), None, None, None, None],
        ]

    def test_overflow_terminal_fill(self, empty_terminal_2_x_2):
        upd_terminal = fill_terminal(
            empty_terminal_2_x_2,
            [
                FileSymbol("I", line=0, column=0),
                FileSymbol("'", line=0, column=1),
                FileSymbol("m", line=0, column=2),
                FileSymbol(" ", line=0, column=3),
                FileSymbol("T", line=0, column=4),
                FileSymbol("o", line=0, column=5),
                FileSymbol("o", line=0, column=6),
                FileSymbol(" ", line=0, column=7),
                FileSymbol("b", line=0, column=8),
                FileSymbol("i", line=0, column=9),
                FileSymbol("g", line=0, column=10),
            ]
        )

        assert upd_terminal.content == [
            [
                FileSymbol("I", line=0, column=0),
                FileSymbol("'", line=0, column=1)
            ],
            [
                FileSymbol("m", line=0, column=2),
                FileSymbol(" ", line=0, column=3)
            ],
        ]

    def test_no_symbols_terminal_fill(self, empty_terminal_2_x_2):
        upd_terminal = fill_terminal(empty_terminal_2_x_2, [])

        assert upd_terminal.content == [
            [None, None],
            [None, None],
        ]
