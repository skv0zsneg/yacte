from .entites import Text, Row


def read_file(file_path: str) -> Text:
    with open(file_path, 'r') as rf:
        text = Text(rows=[Row(symbols=line) for line in rf.readlines()])
    return text


def save_file(text: Text, file_path: str) -> None:
    with open(file_path, 'w') as wf:
        wf.writelines([line.symbols for line in text.rows])
