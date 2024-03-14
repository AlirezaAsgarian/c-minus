'''
C-minus Compiler
by Alireza Asgarian 400105133
and Alireza Mosallanezhad 400108944
'''
from components.Scanner import Scanner
from components.State import TokenType

if __name__ == '__main__':
    filePath = "samples_p1/T02/input.txt"

    scanner = Scanner(filePath)
    tokens = []

    while True:
        token = scanner.get_next_token()
        if token.token_type == TokenType.EOF: break
        elif token.token_type not in (TokenType.WHITESPACE, TokenType.COMMENT):
            tokens.append(token)

    with open("symbol_table.txt", "w") as f:
        for idx, symbol in enumerate(scanner.symbols):
            f.write(f"{idx + 1}.\t{symbol}\n")

    with open("tokens.txt", "w") as f:
        l = 0
        while l < len(tokens):
            f.write(f"{tokens[l].lineno}.\t")
            r = l
            while r < len(tokens) and tokens[r].lineno == tokens[l].lineno:
                if r > l: f.write(' ')
                f.write(f"({tokens[r].token_type.name}, {tokens[r].lexeme})")
                r += 1
            f.write('\n')
            l = r

    with open("lexical_errors.txt", "w") as f:
        errors = scanner.errors
        if not errors:
            f.write("There is no lexical error.")
        l = 0
        while l < len(errors):
            f.write(f"{errors[l].lineno}.\t")
            r = l
            while r < len(errors) and errors[r].lineno == errors[l].lineno:
                if r > l: f.write(' ')
                f.write(f"({errors[r].buffer}, {errors[r].message})")
                r += 1
            f.write('\n')
            l = r
