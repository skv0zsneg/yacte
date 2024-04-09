from .entities import Row, Symbol


def read_file(file_path: str) -> list[Row]:
    with open(file_path, 'r') as rf:
        rows = []
        for n, line in enumerate(rf.readlines()):
            symbols = [Symbol(ch=ch) for ch in line]
            rows.append(Row(row_number=n, symbols=symbols))
        return rows
