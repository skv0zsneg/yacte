# flake8: noqa

import sys

import pytest

sys.path.insert(0, "core")

from core.exceptions import CantSetCursor
from core.models import Cursor, FileSymbol, Terminal
from core.repositories import create_terminal


class TestTerminalActions:
    @pytest.fixture
    def empty_terminal_5_x_5(self) -> Terminal:
        return Terminal(
            cursor=Cursor(x=0, y=0),
            content=[[None for _ in range(5)] for _ in range(5)],
        )

    @pytest.fixture
    def empty_terminal_2_x_2(self) -> Terminal:
        return Terminal(
            cursor=Cursor(x=0, y=0),
            content=[[None for _ in range(2)] for _ in range(2)],
        )

    @pytest.fixture
    def empty_terminal_0_x_0(self) -> Terminal:
        return Terminal(
            cursor=Cursor(x=0, y=0),
            content=None,
        )

    @pytest.fixture
    def partly_filled_terminal_3_x_4(self) -> Terminal:
        return Terminal(
            cursor=Cursor(x=0, y=0),
            content=[
                [FileSymbol('T', 0, 0), FileSymbol('e', 0, 0), None],
                [None, None, None],
                [FileSymbol('s', 0, 0), FileSymbol('t', 0, 0), None],
                [FileSymbol('s', 0, 0), FileSymbol('1', 0, 0), None],
            ],
        )

    @pytest.fixture
    def partly_filled_terminal_4_x_4(self) -> Terminal:
        return Terminal(
            cursor=Cursor(x=0, y=0),
            content=[
                [FileSymbol('T', 0, 0), FileSymbol('e', 0, 0), None, None],
                [FileSymbol('\n', 0, 0), None, None],
                [FileSymbol('s', 0, 0), FileSymbol('t', 0, 0), None, None],
                [FileSymbol('s', 0, 0), FileSymbol('1', 0, 0), None, None],
            ],
        )

    def test_perfect_terminal_fill(self, empty_terminal_5_x_5: Terminal):
        empty_terminal_5_x_5.fill_terminal(
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

        assert empty_terminal_5_x_5.content == [
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

    def test_multi_lines_terminal_fill(self, empty_terminal_5_x_5: Terminal):
        empty_terminal_5_x_5.fill_terminal(
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

        assert empty_terminal_5_x_5.content == [
            [FileSymbol("I", line=0, column=0), None, None, None, None],
            [FileSymbol("'", line=1, column=0), None, None, None, None],
            [FileSymbol("m", line=2, column=0), None, None, None, None],
            [FileSymbol(" ", line=3, column=0), None, None, None, None],
            [FileSymbol("T", line=4, column=0), None, None, None, None],
        ]

    def test_overflow_terminal_fill(self, empty_terminal_2_x_2):
        empty_terminal_2_x_2.fill_terminal(
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

        assert empty_terminal_2_x_2.content == [
            [
                FileSymbol("I", line=0, column=0),
                FileSymbol("'", line=0, column=1)
            ],
            [
                FileSymbol("m", line=0, column=2),
                FileSymbol(" ", line=0, column=3)
            ],
        ]

    def test_no_symbols_terminal_fill(self, empty_terminal_2_x_2: Terminal):
        empty_terminal_2_x_2.fill_terminal([])

        assert empty_terminal_2_x_2.content == [
            [None, None],
            [None, None],
        ]

    def test_zero_size_terminal_fill(self, empty_terminal_0_x_0: Terminal):
        empty_terminal_0_x_0.fill_terminal(
            [FileSymbol('H', line=0, column=0)]
        )
        assert empty_terminal_0_x_0.content is None

    def test_create_1000_x_1000_terminal(self):
        new_terminal = create_terminal(1000, 1000)
        assert new_terminal.content == [[None for _ in range(1000)] for _ in range(1000)]

    def test_create_0_x_0_terminal(self):
        new_terminal = create_terminal(0, 0)
        assert new_terminal.content is None

    def test_create_1_x_0_terminal(self):
        new_terminal = create_terminal(1, 0)
        assert new_terminal.content is None

    def test_create_0_x_1_terminal(self):
        new_terminal = create_terminal(0, 1)
        assert new_terminal.content is None

    def test_set_cursor_position_on_symbol_with_left_symbol(self, partly_filled_terminal_3_x_4: Terminal):
        partly_filled_terminal_3_x_4.cursor_set_position(1, 3)
        assert partly_filled_terminal_3_x_4.cursor.x == 1
        assert partly_filled_terminal_3_x_4.cursor.y == 3

    def test_set_cursor_position_on_None_with_left_is_symbol(self, partly_filled_terminal_3_x_4: Terminal):
        partly_filled_terminal_3_x_4.cursor_set_position(2, 2)
        assert partly_filled_terminal_3_x_4.cursor.x == 2
        assert partly_filled_terminal_3_x_4.cursor.y == 2

    def test_set_cursor_position_on_None_with_left_is_symbol_on_line_above(self, partly_filled_terminal_3_x_4: Terminal):
        partly_filled_terminal_3_x_4.cursor_set_position(0, 2)
        assert partly_filled_terminal_3_x_4.cursor.x == 0
        assert partly_filled_terminal_3_x_4.cursor.y == 2

    def test_set_cursor_position_on_None_without_neighbors(self, partly_filled_terminal_3_x_4: Terminal):
        with pytest.raises(CantSetCursor):
            partly_filled_terminal_3_x_4.cursor_set_position(1, 1)

    def test_set_cursor_position_on_None_without_neighbors_on_line_above(self, partly_filled_terminal_3_x_4: Terminal):
        with pytest.raises(CantSetCursor):
            partly_filled_terminal_3_x_4.cursor_set_position(0, 1)

    def test_move_cursor_right_(self, partly_filled_terminal_4_x_4: Terminal):
        partly_filled_terminal_4_x_4.cursor.x = 2
        partly_filled_terminal_4_x_4.cursor.y = 0
        partly_filled_terminal_4_x_4.cursor_move_right()
        assert partly_filled_terminal_4_x_4.cursor.x == 0
        assert partly_filled_terminal_4_x_4.cursor.y == 1

    def test_move_cursor_right_in_dead_end(self, partly_filled_terminal_4_x_4: Terminal):
        partly_filled_terminal_4_x_4.cursor.x = 3
        partly_filled_terminal_4_x_4.cursor.y = 3
        partly_filled_terminal_4_x_4.cursor_move_right()
        assert partly_filled_terminal_4_x_4.cursor.x == 3
        assert partly_filled_terminal_4_x_4.cursor.y == 3