from components.Scanner import Scanner
from components.State import TokenType


def write_symbol_table(symbols):
    with open("symbol_table.txt", "w+") as f:
        for idx, symbol in enumerate(symbols):
            f.write(f"{idx + 1}. {symbol}\n")

if __name__ == '__main__':
    filePath = "/home/alireza/PycharmProjects/c-minus/samples_p1/T03/input.txt"
    scanner = Scanner(filePath)
    for i in range(0, 1000):
        token = scanner.get_next_token()
        if (token.token_type != TokenType.WHITESPACE):
            print(i)
            print(token.token_type, end=" ")
            print(scanner.lineno, end=" ")
            print(token.lexeme)
        if (token.token_type == TokenType.EOF):
            break

    write_symbol_table(scanner.symbols)
