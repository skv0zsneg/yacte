from models import Terminal, FileSymbol


def fill_terminal(terminal: Terminal, symbols: list[FileSymbol]) -> Terminal:
    """Filling terminal with symbols.

    :param terminal: Terminal
    :param symbols: List of symbols in right order
    :return: Terminal with giving symbols
    """
    if not symbols:
        return terminal

    print(terminal.content)
    term_ptr_x, term_ptr_y = 0, 0
    last_symbol_line = symbols[0].line
    for symbol in symbols:
        if last_symbol_line < symbol.line:
            term_ptr_y += symbol.line - last_symbol_line
            term_ptr_x = 0
        if term_ptr_x >= terminal.size_x:
            term_ptr_y += 1
            term_ptr_x = 0
        if term_ptr_y >= terminal.size_y:
            break

        terminal.content[term_ptr_y][term_ptr_x] = symbol

        term_ptr_x += 1
        last_symbol_line = symbol.line
    print(terminal.content)
    return terminal
