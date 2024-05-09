'''
C-minus Compiler
by Alireza Asgarian 400105133
and Alireza Mosallanezhad 400108944
'''
from anytree import RenderTree

from components.parser.Parser import Parser
from components.scanner.Scanner import *

if __name__ == '__main__':
    file_path = "input.txt"

    scanner = Scanner(open(file_path))
    parser = Parser(scanner)
    parse_tree = parser.parse_all()

    with open("parse_tree.txt", "w") as f:
        for pre, fill, node in RenderTree(parse_tree):
            f.write("%s%s\n" % (pre, node.name))

    with open("syntax_errors.txt", "w") as f:
        if not parser.errors:
            f.write("There is no syntax error.")
        else:
            f.write('\n'.join(parser.errors))
