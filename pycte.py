# https://docs.python.org/3/howto/curses.html#curses-howto
# https://docs.python.org/3/library/curses.html#module-curses

import curses
from curses import wrapper

from core.filemanager import read_file


if __name__ == '__main__':
    text = read_file("tests/textbig")

    def main(stdscr):
        stdscr.clear()

        for i, row in enumerate(text.rows[:4]):
            stdscr.addstr(i, 0, row.symbols)

        while True:
            stdscr.refresh()
            key = stdscr.getch()
            if key == ord('q'):
                break
            elif key == curses.KEY_RIGHT:
                y, x = stdscr.getyx()
                stdscr.move(y, x+1)  # RIGHT
            elif key == curses.KEY_LEFT:
                y, x = stdscr.getyx()
                stdscr.move(y, x-1)  # LEFT
            elif key == curses.KEY_DOWN:
                y, x = stdscr.getyx()
                stdscr.move(y+1, x)  # DOWN
            elif key == curses.KEY_UP:
                y, x = stdscr.getyx()
                stdscr.move(y-1, x)  # UP
            else:
                stdscr.insch(chr(key))

    wrapper(main)
