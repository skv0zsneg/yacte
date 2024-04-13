from .models import FileSymbol


class FileReader:
    def __init__(self, file_path: str) -> None:
        self.file_path: str = file_path

    def read_all(self) -> list[FileSymbol]:
        fp = open(self.file_path, 'r')

        file_symbols = []
        for line_n, line in enumerate(fp.readlines()):
            for col_n, symbol in enumerate(line):
                file_symbols.append(
                    FileSymbol(symbol, line=line_n, column=col_n)
                )

        fp.close()
        return file_symbols
