# https://docs.python.org/3/howto/curses.html#curses-howto
# https://docs.python.org/3/library/curses.html#module-curses

import argparse

from core.displaymanager import DisplayManager

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog="pycte",
        description="CLI Python text editor",
    )
    parser.add_argument('filename')
    args = parser.parse_args()

    dm = DisplayManager()
    dm.launch(args.filename)
