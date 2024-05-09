from enum import Enum, auto

from components.scanner.State import TokenType

EPSILON = 'epsilon'
SEMICOLON = ";"
OPEN_PARENTHESIS = "("
CLOSED_PARENTHESIS = ")"
OPEN_BRACKET = "["
CLOSED_BRACKET = "]"
OPEN_CURLY_BRACKET = "{"
CLOSED_CURLY_BRACKET = "}"
COMMA = ","
EQUALITY_OPERATOR = "=="
EQUAL = "="
PLUS = '+'
MINUS = '-'
MULTIPLY_OPERATOR = '*'
LESS_THAN = "<"
GREATER_THAN = ">"

grammer_terminals = [TokenType.ID, ';', '[', TokenType.NUM, ']', '(', ')', 'int', 'void', ',', '{', '}', 'break', 'if', 'endif', 'else', 'for', 'return', '=', '<', '==', '+', '-', '*']

first_set_raw = '''Program − − − − − − − + + − − − − − − − − − − − − − − − +
Declaration_list − − − − − − − + + − − − − − − − − − − − − − − − +
Declaration − − − − − − − + + − − − − − − − − − − − − − − − −
Declaration_initial − − − − − − − + + − − − − − − − − − − − − − − − −
Declaration_prime − + + − − + − − − − − − − − − − − − − − − − − − −
Var_declaration_prime − + + − − − − − − − − − − − − − − − − − − − − − −
Fun_declaration_prime − − − − − + − − − − − − − − − − − − − − − − − − −
Type_specifier − − − − − − − + + − − − − − − − − − − − − − − − −
Params − − − − − − − + + − − − − − − − − − − − − − − − −
Param_list − − − − − − − − − + − − − − − − − − − − − − − − +
Param − − − − − − − + + − − − − − − − − − − − − − − − −
Param_prime − − + − − − − − − − − − − − − − − − − − − − − − +
Compound_stmt − − − − − − − − − − + − − − − − − − − − − − − − −
Statement_list + + − + − + − − − − + − + + − − + + − − − + + − +
Statement + + − + − + − − − − + − + + − − + + − − − + + − −
Expression_stmt + + − + − + − − − − − − + − − − − − − − − + + − −
Selection_stmt − − − − − − − − − − − − − + − − − − − − − − − − −
Else_stmt − − − − − − − − − − − − − − + + − − − − − − − − −
Iteration_stmt − − − − − − − − − − − − − − − − + − − − − − − − −
Return_stmt − − − − − − − − − − − − − − − − − + − − − − − − −
Return_stmt_prime + + − + − + − − − − − − − − − − − − − − − + + − −
Expression + − − + − + − − − − − − − − − − − − − − − + + − −
B − − + − − + − − − − − − − − − − − − + + + + + + +
H − − − − − − − − − − − − − − − − − − + + + + + + +
Simple_expression_zegond − − − + − + − − − − − − − − − − − − − − − + + − −
Simple_expression_prime − − − − − + − − − − − − − − − − − − − + + + + + +
C − − − − − − − − − − − − − − − − − − − + + − − − +
Relop − − − − − − − − − − − − − − − − − − − + + − − − −
Additive_expression + − − + − + − − − − − − − − − − − − − − − + + − −
Additive_expression_prime − − − − − + − − − − − − − − − − − − − − − + + + +
Additive_expression_zegond − − − + − + − − − − − − − − − − − − − − − + + − −
D − − − − − − − − − − − − − − − − − − − − − + + − +
Addop − − − − − − − − − − − − − − − − − − − − − + + − −
Term + − − + − + − − − − − − − − − − − − − − − + + − −
Term_prime − − − − − + − − − − − − − − − − − − − − − − − + +
Term_zegond − − − + − + − − − − − − − − − − − − − − − + + − −
G − − − − − − − − − − − − − − − − − − − − − − − + +
Signed_factor + − − + − + − − − − − − − − − − − − − − − + + − −
Signed_factor_prime − − − − − + − − − − − − − − − − − − − − − − − − +
Signed_factor_zegond − − − + − + − − − − − − − − − − − − − − − + + − −
Factor + − − + − + − − − − − − − − − − − − − − − − − − −
Var_call_prime − − + − − + − − − − − − − − − − − − − − − − − − +
Var_prime − − + − − − − − − − − − − − − − − − − − − − − − +
Factor_prime − − − − − + − − − − − − − − − − − − − − − − − − +
Factor_zegond − − − + − + − − − − − − − − − − − − − − − − − − −
Args + − − + − + − − − − − − − − − − − − − − − + + − +
Arg_list + − − + − + − − − − − − − − − − − − − − − + + − −
Arg_list_prime − − − − − − − − − + − − − − − − − − − − − − − − +'''

follow_set_raw = '''Program − − − − − − − − − − − − − − − − − − − − − − − − +
Declaration_list + + − + − + − − − − + + + + − − + + − − − + + − +
Declaration + + − + − + − + + − + + + + − − + + − − − + + − +
Declaration_initial − + + − − + + − − + − − − − − − − − − − − − − − −
Declaration_prime + + − + − + − + + − + + + + − − + + − − − + + − +
Var_declaration_prime + + − + − + − + + − + + + + − − + + − − − + + − +
Fun_declaration_prime + + − + − + − + + − + + + + − − + + − − − + + − +
Type_specifier + − − − − − − − − − − − − − − − − − − − − − − − −
Params − − − − − − + − − − − − − − − − − − − − − − − − −
Param_list − − − − − − + − − − − − − − − − − − − − − − − − −
Param − − − − − − + − − + − − − − − − − − − − − − − − −
Param_prime − − − − − − + − − + − − − − − − − − − − − − − − −
Compound_stmt + + − + − + − + + − + + + + + + + + − − − + + − +
Statement_list − − − − − − − − − − − + − − − − − − − − − − − − −
Statement + + − + − + − − − − + + + + + + + + − − − + + − −
Expression_stmt + + − + − + − − − − + + + + + + + + − − − + + − −
Selection_stmt + + − + − + − − − − + + + + + + + + − − − + + − −
Else_stmt + + − + − + − − − − + + + + + + + + − − − + + − −
Iteration_stmt + + − + − + − − − − + + + + + + + + − − − + + − −
Return_stmt + + − + − + − − − − + + + + + + + + − − − + + − −
Return_stmt_prime + + − + − + − − − − + + + + + + + + − − − + + − −
Expression − + − − + − + − − + − − − − − − − − − − − − − − −
B − + − − + − + − − + − − − − − − − − − − − − − − −
H − + − − + − + − − + − − − − − − − − − − − − − − −
Simple_expression_zegond − + − − + − + − − + − − − − − − − − − − − − − − −
Simple_expression_prime − + − − + − + − − + − − − − − − − − − − − − − − −
C − + − − + − + − − + − − − − − − − − − − − − − − −
Relop + − − + − + − − − − − − − − − − − − − − − + + − −
Additive_expression − + − − + − + − − + − − − − − − − − − − − − − − −
Additive_expression_prime − + − − + − + − − + − − − − − − − − − + + − − − −
Additive_expression_zegond − + − − + − + − − + − − − − − − − − − + + − − − −
D − + − − + − + − − + − − − − − − − − − + + − − − −
Addop + − − + − + − − − − − − − − − − − − − − − + + − −
Term − + − − + − + − − + − − − − − − − − − + + + + − −
Term_prime − + − − + − + − − + − − − − − − − − − + + + + − −
Term_zegond − + − − + − + − − + − − − − − − − − − + + + + − −
G − + − − + − + − − + − − − − − − − − − + + + + − −
Signed_factor − + − − + − + − − + − − − − − − − − − + + + + + −
Signed_factor_prime − + − − + − + − − + − − − − − − − − − + + + + + −
Signed_factor_zegond − + − − + − + − − + − − − − − − − − − + + + + + −
Factor − + − − + − + − − + − − − − − − − − − + + + + + −
Var_call_prime − + − − + − + − − + − − − − − − − − − + + + + + −
Var_prime − + − − + − + − − + − − − − − − − − − + + + + + −
Factor_prime − + − − + − + − − + − − − − − − − − − + + + + + −
Factor_zegond − + − − + − + − − + − − − − − − − − − + + + + + −
Args − − − − − − + − − − − − − − − − − − − − − − − − −
Arg_list − − − − − − + − − − − − − − − − − − − − − − − − −
Arg_list_prime − − − − − − + − − − − − − − − − − − − − − − − − −'''


class NonTerminal(Enum):

    def __init__(self, id, first, follow):
        self.first = first
        self.follow = follow

    Program = (auto(), [], [])
    Declaration_list = (auto(), [], [])
    Declaration = (auto(), [], [])
    Declaration_initial = (auto(), [], [])
    Declaration_prime = (auto(), [], [])
    Var_declaration_prime = (auto(), [], [])
    Fun_declaration_prime = (auto(), [], [])
    Type_specifier = (auto(), [], [])
    Params = (auto(), [], [])
    Param_list = (auto(), [], [])
    Param = (auto(), [], [])
    Param_prime = (auto(), [], [])
    Compound_stmt = (auto(), [], [])
    Statement_list = (auto(), [], [])
    Statement = (auto(), [], [])
    Expression_stmt = (auto(), [], [])
    Selection_stmt = (auto(), [], [])
    Else_stmt = (auto(), [], [])
    Iteration_stmt = (auto(), [], [])
    Return_stmt = (auto(), [], [])
    Return_stmt_prime = (auto(), [], [])
    Expression = (auto(), [], [])
    B = (auto(), [], [])
    H = (auto(), [], [])
    Simple_expression_zegond = (auto(), [], [])
    Simple_expression_prime = (auto(), [], [])
    C = (auto(), [], [])
    Relop = (auto(), [], [])
    Additive_expression = (auto(), [], [])
    Additive_expression_prime = (auto(), [], [])
    Additive_expression_zegond = (auto(), [], [])
    D = (auto(), [], [])
    Addop = (auto(), [], [])
    Term = (auto(), [], [])
    Term_prime = (auto(), [], [])
    Term_zegond = (auto(), [], [])
    G = (auto(), [], [])
    Signed_factor = (auto(), [], [])
    Signed_factor_prime = (auto(), [], [])
    Signed_factor_zegond = (auto(), [], [])
    Factor = (auto(), [], [])
    Var_call_prime = (auto(), [], [])
    Var_prime = (auto(), [], [])
    Factor_prime = (auto(), [], [])
    Factor_zegond = (auto(), [], [])
    Args = (auto(), [], [])
    Arg_list = (auto(), [], [])
    Arg_list_prime = (auto(), [], [])


for line in first_set_raw.splitlines():
    vals = line.split()
    name = vals[0]
    for i, x in enumerate(grammer_terminals + [EPSILON]):
        if vals[i + 1] == '+':
            NonTerminal[name].first.append(x)
    NonTerminal[name].first = tuple(NonTerminal[name].first)

for line in follow_set_raw.splitlines():
    vals = line.split()
    name = vals[0]
    for i, x in enumerate(grammer_terminals + ['$']):
        if vals[i + 1] == '+':
            NonTerminal[name].follow.append(x)
    NonTerminal[name].follow = tuple(NonTerminal[name].follow)