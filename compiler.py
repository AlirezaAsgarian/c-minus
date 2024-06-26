'''
C-minus Compiler
by Alireza Asgarian 400105133
and Alireza Mosallanezhad 400108944
'''

from components.parser.Parser import Parser
from components.scanner.Scanner import *

if __name__ == '__main__':
    file_path = "input.txt"

    scanner = Scanner(open(file_path))
    parser = Parser(scanner)
    parse_tree = parser.parse_all()

    with open("semantic_errors.txt", "w") as f:
        errors = parser.code_generator.semantic_errors
        if not errors:
            f.write("The input program is semantically correct")
        else:
            for lineno, err in errors:
                f.write("#%s : Semantic Error! %s\n" % (lineno, err))

    with open("output.txt", "w") as f:
        for i, x in enumerate(parser.code_generator.codes):
            f.write("%s\t(%s, %s, %s, %s)\n" % (
                    i,
                    x[0].name,
                    x[1],
                    x[2] if len(x) >= 3 else '',
                    x[3] if len(x) >= 4 else ''
                ))