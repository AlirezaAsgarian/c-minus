'''
C-minus Compiler
by Alireza Asgarian 400105133
and Alireza Mosallanezhad 400108944
'''
from components.scanner.Scanner import *
from components.scanner.State import *
from components.parser.Parser import grammer_rules, Parser
from components.parser.NonTerminal import NonTerminal


if __name__ == '__main__':
    file_path = "input.txt"

    scanner = Scanner(open(file_path))
    parser = Parser(scanner)
    parser.parse()
    tokens = []

    while True:
        token = scanner.get_next_token()
        if token.token_type == TokenType.EOF: break
        elif token.token_type not in (TokenType.WHITESPACE, TokenType.COMMENT):
            tokens.append(token)

    symbol_table = scanner.symbols
    with open("symbol_table.txt", "w") as f:
        for idx, symbol in enumerate(symbol_table):
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
