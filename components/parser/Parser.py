from anytree import Node

from components.parser.NonTerminal import *
from components.scanner.State import TokenType, Keywords


def without_epsilon(input):
    return tuple(x for x in input if x != EPSILON)


grammer_rules = {
    NonTerminal.Program: {
        without_epsilon(NonTerminal.Declaration_list.first + NonTerminal.Program.follow): [NonTerminal.Declaration_list]
    },
    NonTerminal.Declaration_list: {
        NonTerminal.Declaration.first: [NonTerminal.Declaration, NonTerminal.Declaration_list]
    },
    NonTerminal.Declaration: {
        NonTerminal.Declaration_initial.first: [NonTerminal.Declaration_initial, NonTerminal.Declaration_prime]
    },
    NonTerminal.Declaration_initial: {
        NonTerminal.Type_specifier.first: [NonTerminal.Type_specifier, TokenType.ID]
    },
    NonTerminal.Declaration_prime: {
        NonTerminal.Fun_declaration_prime.first: [NonTerminal.Fun_declaration_prime],
        NonTerminal.Var_declaration_prime.first: [NonTerminal.Var_declaration_prime]
    },
    NonTerminal.Var_declaration_prime: {
        (SEMICOLON,): [SEMICOLON],
        (OPEN_BRACKET,): [OPEN_BRACKET, TokenType.NUM, CLOSED_BRACKET, SEMICOLON]
    },
    NonTerminal.Fun_declaration_prime: {
        (OPEN_PARENTHESIS,): [OPEN_PARENTHESIS, NonTerminal.Params, CLOSED_PARENTHESIS, NonTerminal.Compound_stmt]
    },
    NonTerminal.Type_specifier: {
        (Keywords.INT.value,): [Keywords.INT.value],
        (Keywords.VOID.value,): [Keywords.VOID.value]
    },
    NonTerminal.Params: {
        (Keywords.INT.value,): [Keywords.INT.value, TokenType.ID, NonTerminal.Param_prime, NonTerminal.Param_list],
        (Keywords.VOID.value,): [Keywords.VOID.value]
    },
    NonTerminal.Param_list: {
        (COMMA,): [COMMA, NonTerminal.Param, NonTerminal.Param_list]
    },
    NonTerminal.Param: {
        NonTerminal.Declaration_initial.first: [NonTerminal.Declaration_initial, NonTerminal.Param_prime]
    },
    NonTerminal.Param_prime: {
        (OPEN_BRACKET,): [OPEN_BRACKET, CLOSED_BRACKET]
    },
    NonTerminal.Compound_stmt: {
        (OPEN_CURLY_BRACKET,): [OPEN_CURLY_BRACKET, NonTerminal.Declaration_list, NonTerminal.Statement_list,
                                CLOSED_CURLY_BRACKET]
    },
    NonTerminal.Statement_list: {
        NonTerminal.Statement.first: [NonTerminal.Statement, NonTerminal.Statement_list]
    },
    NonTerminal.Statement: {
        NonTerminal.Return_stmt.first: [NonTerminal.Return_stmt],
        NonTerminal.Expression_stmt.first: [NonTerminal.Expression_stmt],
        NonTerminal.Compound_stmt.first: [NonTerminal.Compound_stmt],
        NonTerminal.Selection_stmt.first: [NonTerminal.Selection_stmt],
        NonTerminal.Iteration_stmt.first: [NonTerminal.Iteration_stmt]
    },
    NonTerminal.Expression_stmt: {
        NonTerminal.Expression.first: [NonTerminal.Expression, SEMICOLON],
        (Keywords.BREAK.value,): [Keywords.BREAK.value, SEMICOLON],
        (SEMICOLON,): [SEMICOLON]
    },
    NonTerminal.Selection_stmt: {
        (Keywords.IF.value,): [Keywords.IF.value, OPEN_PARENTHESIS, NonTerminal.Expression, CLOSED_PARENTHESIS,
                               NonTerminal.Statement, NonTerminal.Else_stmt]
    },
    NonTerminal.Else_stmt: {
        (Keywords.ENDIF.value,): [Keywords.ENDIF.value],
        (Keywords.ELSE.value,): [Keywords.ELSE.value, NonTerminal.Statement, Keywords.ENDIF.value]
    },
    NonTerminal.Iteration_stmt: {
        (Keywords.FOR.value,): [Keywords.FOR.value, OPEN_PARENTHESIS, NonTerminal.Expression, SEMICOLON,
                                NonTerminal.Expression, SEMICOLON, NonTerminal.Expression, CLOSED_PARENTHESIS,
                                NonTerminal.Statement]
    },
    NonTerminal.Return_stmt: {
        (Keywords.RETURN.value,): [Keywords.RETURN.value, NonTerminal.Return_stmt_prime]
    },
    NonTerminal.Return_stmt_prime: {
        NonTerminal.Expression.first: [NonTerminal.Expression, SEMICOLON],
        (SEMICOLON,): [SEMICOLON]
    },
    NonTerminal.Expression: {
        NonTerminal.Simple_expression_zegond.first: [NonTerminal.Simple_expression_zegond],
        (TokenType.ID,): [TokenType.ID, NonTerminal.B]
    },
    NonTerminal.B: {
        (EQUAL,): [EQUAL, NonTerminal.Expression],
        (OPEN_BRACKET,): [OPEN_BRACKET, NonTerminal.Expression, CLOSED_BRACKET, NonTerminal.H],
        without_epsilon(NonTerminal.Simple_expression_prime.first + NonTerminal.B.follow): [
            NonTerminal.Simple_expression_prime]
    },
    NonTerminal.H: {
        (EQUAL,): [EQUAL, NonTerminal.Expression],
        without_epsilon(NonTerminal.G.first + NonTerminal.D.first + NonTerminal.C.first + NonTerminal.H.follow): [
            NonTerminal.G, NonTerminal.D, NonTerminal.C]
    },
    NonTerminal.Simple_expression_zegond: {
        NonTerminal.Additive_expression_zegond.first: [NonTerminal.Additive_expression_zegond, NonTerminal.C]
    },
    NonTerminal.Simple_expression_prime: {
        without_epsilon(
            NonTerminal.Additive_expression_prime.first + NonTerminal.C.first + NonTerminal.Simple_expression_prime.follow): [
            NonTerminal.Additive_expression_prime, NonTerminal.C]
    },
    NonTerminal.C: {
        NonTerminal.Relop.first: [NonTerminal.Relop, NonTerminal.Additive_expression]
    },
    NonTerminal.Relop: {
        (LESS_THAN,): [LESS_THAN],
        (EQUALITY_OPERATOR,): [EQUALITY_OPERATOR, ]
    },
    NonTerminal.Additive_expression: {
        NonTerminal.Term.first: [NonTerminal.Term, NonTerminal.D]
    },
    NonTerminal.Additive_expression_prime: {
        without_epsilon(
            NonTerminal.Term_prime.first + NonTerminal.D.first + NonTerminal.Additive_expression_prime.follow): [
            NonTerminal.Term_prime, NonTerminal.D]
    },
    NonTerminal.Additive_expression_zegond: {
        NonTerminal.Term_zegond.first: [NonTerminal.Term_zegond, NonTerminal.D]
    },
    NonTerminal.D: {
        NonTerminal.Addop.first: [NonTerminal.Addop, NonTerminal.Term, NonTerminal.D]
    },
    NonTerminal.Addop: {
        (PLUS,): [PLUS],
        (MINUS,): [MINUS]
    },
    NonTerminal.Term: {
        NonTerminal.Signed_factor.first: [NonTerminal.Signed_factor, NonTerminal.G]
    },
    NonTerminal.Term_prime: {
        without_epsilon(NonTerminal.Signed_factor_prime.first + NonTerminal.G.first + NonTerminal.Term_prime.follow): [
            NonTerminal.Signed_factor_prime, NonTerminal.G]
    },
    NonTerminal.Term_zegond: {
        NonTerminal.Signed_factor_zegond.first: [NonTerminal.Signed_factor_zegond, NonTerminal.G]
    },
    NonTerminal.G: {
        (MULTIPLY_OPERATOR,): [MULTIPLY_OPERATOR, NonTerminal.Signed_factor, NonTerminal.G]
    },
    NonTerminal.Signed_factor: {
        (PLUS,): [PLUS, NonTerminal.Factor],
        (MINUS,): [MINUS, NonTerminal.Factor],
        NonTerminal.Factor.first: [NonTerminal.Factor]
    },
    NonTerminal.Signed_factor_prime: {
        without_epsilon(NonTerminal.Factor_prime.first + NonTerminal.Signed_factor_prime.follow): [
            NonTerminal.Factor_prime]
    },
    NonTerminal.Signed_factor_zegond: {
        (PLUS,): [PLUS, NonTerminal.Factor],
        (MINUS,): [MINUS, NonTerminal.Factor],
        NonTerminal.Factor_zegond.first: [NonTerminal.Factor_zegond]
    },
    NonTerminal.Factor: {
        (OPEN_PARENTHESIS,): [OPEN_PARENTHESIS, NonTerminal.Expression, CLOSED_PARENTHESIS],
        (TokenType.ID,): [TokenType.ID, NonTerminal.Var_call_prime],
        (TokenType.NUM,): [TokenType.NUM]
    },
    NonTerminal.Var_call_prime: {
        (OPEN_PARENTHESIS,): [OPEN_PARENTHESIS, NonTerminal.Args, CLOSED_PARENTHESIS],
        without_epsilon(NonTerminal.Var_prime.first + NonTerminal.Var_call_prime.follow): [NonTerminal.Var_prime]
    },
    NonTerminal.Var_prime: {
        (OPEN_BRACKET,): [OPEN_BRACKET, NonTerminal.Expression, CLOSED_BRACKET]
    },
    NonTerminal.Factor_prime: {
        (OPEN_PARENTHESIS,): [OPEN_PARENTHESIS, NonTerminal.Args, CLOSED_PARENTHESIS]
    },
    NonTerminal.Factor_zegond: {
        (OPEN_PARENTHESIS,): [OPEN_PARENTHESIS, NonTerminal.Expression, CLOSED_PARENTHESIS],
        (TokenType.NUM,): [TokenType.NUM]
    },
    NonTerminal.Args: {
        NonTerminal.Arg_list.first: [NonTerminal.Arg_list]
    },
    NonTerminal.Arg_list: {
        NonTerminal.Expression.first: [NonTerminal.Expression, NonTerminal.Arg_list_prime]
    },
    NonTerminal.Arg_list_prime: {
        (COMMA,): [COMMA, NonTerminal.Expression, NonTerminal.Arg_list_prime]
    }
}


def get_lexeme_or_type(token):
    return token.token_type.name if token.token_type in (TokenType.ID, TokenType.NUM) else token.lexeme


unexpected_eof = False

class Parser:

    def __init__(self, scanner):
        self.scanner = scanner
        self.current_token = None
        self.errors = []

    def parse_all(self):
        root = Node(str(NonTerminal.Program.name))
        self.get_next_token()
        self.parse(NonTerminal.Program, root)
        if not unexpected_eof: Node("$", root)
        return root

    def parse(self, current_state, current_node):
        global unexpected_eof
        print(self.current_token.lineno, current_state.name, self.current_token.lexeme)
        for possible_token, rule in grammer_rules.get(current_state).items():
            # print(self.current_token, possible_token)
            if self.is_current_token_in(possible_token):
                # print("%s start %s" % (self.current_token.lineno, rule))
                for var in rule:
                    print("%s %s put %s" % (self.current_token.lineno, self.current_token.lexeme, var))
                    if isinstance(var, NonTerminal):
                        node = Node(str(var.name.replace('_', '-')), current_node)
                        self.parse(var, node)
                        if unexpected_eof: return
                    else:
                        token_str = "(%s, %s)" % (self.current_token.token_type.name, self.current_token.lexeme)
                        if self.is_current_token_in((var,)):
                            Node(token_str, current_node)
                            self.get_next_token()
                        else:
                            if self.is_current_token_in(current_state.follow):
                                # current_node.parent = None  # remove expected but missing node
                                self.errors.append("#%s : syntax error, missing %s"
                                                   % (self.current_token.lineno,
                                                      str(var).replace('_', '-')))
                                print(self.errors[-1])
                            else:
                                if self.current_token.token_type == TokenType.EOF:
                                    self.errors.append("#%s : syntax error, Unexpected EOF" % self.current_token.lineno)
                                    print(self.errors[-1])
                                    unexpected_eof = True
                                    return
                                self.errors.append("#%s : syntax error, illegal %s" % (
                                    self.current_token.lineno, get_lexeme_or_type(self.current_token)))
                                print(self.errors[-1])
                                self.get_next_token()
                                return
                return
        if EPSILON in current_state.first and self.is_current_token_in(current_state.follow):
            print("saw EPS")
            Node(EPSILON, current_node)
            return
        if self.is_current_token_in(current_state.follow):
            current_node.parent = None  # remove expected but missing node
            self.errors.append("#%s : syntax error, missing %s"
                               % (self.current_token.lineno, current_state.name.replace('_', '-')))
            print(self.errors[-1])
        else:
            if self.current_token.token_type == TokenType.EOF:
                current_node.parent = None
                self.errors.append("#%s : syntax error, Unexpected EOF" % self.current_token.lineno)
                print(self.errors[-1])
                unexpected_eof = True
                return
            self.errors.append("#%s : syntax error, illegal %s"
                               % (self.current_token.lineno, get_lexeme_or_type(self.current_token)))
            print(self.errors[-1])
            self.get_next_token()
            self.parse(current_state, current_node)

    def get_next_token(self):
        while True:
            next_token = self.scanner.get_next_token()
            if next_token.token_type not in (TokenType.WHITESPACE, TokenType.COMMENT):
                self.current_token = next_token
                return

    def is_current_token_in(self, input_set):
        return self.current_token.lexeme in input_set or self.current_token.token_type in input_set
