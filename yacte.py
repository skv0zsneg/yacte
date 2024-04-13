# https://docs.python.org/3/howto/curses.html#curses-howto
# https://docs.python.org/3/library/curses.html#module-curses

import argparse
import logging
import sys

from core.file_reader import FileReader
from core.displayers import BaseDisplayer, LinuxDisplayer

logging.basicConfig(filename='yacte.log', level=logging.DEBUG)


def main():
    parser = argparse.ArgumentParser(
        prog="Yacte",
        description=("Yacte (Yet Another CLI Text Editor) - Text CLI Editor "
                     "on Python for best interaction with files in "
                     "your terminal."),
    )
    parser.add_argument('filename')
    args = parser.parse_args()

    platform_to_terminal_display: dict[str, type[BaseDisplayer]] = {
        'linux': LinuxDisplayer,
    }

    file_reader = FileReader(args.filename)
    terminal_display = platform_to_terminal_display[sys.platform](file_reader)
    terminal_display.launch()


if __name__ == '__main__':
    main()
