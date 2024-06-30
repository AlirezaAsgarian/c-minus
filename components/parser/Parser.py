from anytree import Node

from components.codegen.CodeGenerator import *
from components.parser.NonTerminal import *
from components.scanner.State import Keywords


def without_epsilon(input):
    return tuple(x for x in input if x != EPSILON)


grammer_rules = {
    NonTerminal.Program: {
        without_epsilon(NonTerminal.Declaration_list.first + NonTerminal.Program.follow): [
            Action.push_lineno,
            Action.placeholder_line, Action.placeholder_line,  # push return-address = end of program lineno
            Action.push_fp_value,
            Action.placeholder_line,  # set fp = current sp
            Action.placeholder_line,  # jp to main
            Action.return_code_block,
            NonTerminal.Declaration_list,
            Action.call_main
            ]
    },
    NonTerminal.Declaration_list: {
        NonTerminal.Declaration.first: [NonTerminal.Declaration, NonTerminal.Declaration_list]
    },
    NonTerminal.Declaration: {
        NonTerminal.Declaration_initial.first: [NonTerminal.Declaration_initial, NonTerminal.Declaration_prime]
    },
    NonTerminal.Declaration_initial: {
        NonTerminal.Type_specifier.first: [Action.push_id, NonTerminal.Type_specifier, Action.push_id, TokenType.ID]
    },
    NonTerminal.Declaration_prime: {
        NonTerminal.Fun_declaration_prime.first: [NonTerminal.Fun_declaration_prime],
        NonTerminal.Var_declaration_prime.first: [NonTerminal.Var_declaration_prime]
    },
    NonTerminal.Var_declaration_prime: {
        (SEMICOLON,): [Action.declare_int, SEMICOLON],
        (OPEN_BRACKET,): [OPEN_BRACKET, Action.push_id, TokenType.NUM, CLOSED_BRACKET, Action.declare_array, SEMICOLON]
    },
    NonTerminal.Fun_declaration_prime: {
        (OPEN_PARENTHESIS,): [Action.register_function, OPEN_PARENTHESIS, NonTerminal.Params, CLOSED_PARENTHESIS,
                              Action.begin_function, NonTerminal.Compound_stmt,
                              Action.function_return, Action.end_function]
    },
    NonTerminal.Type_specifier: {
        (Keywords.INT.value,): [Keywords.INT.value],
        (Keywords.VOID.value,): [Keywords.VOID.value]
    },
    NonTerminal.Params: {
        (Keywords.INT.value,): [Action.push_id, Keywords.INT.value, Action.push_id, Action.add_function_param,
                                TokenType.ID, NonTerminal.Param_prime, NonTerminal.Param_list],
        (Keywords.VOID.value,): [Keywords.VOID.value]
    },
    NonTerminal.Param_list: {
        (COMMA,): [COMMA, NonTerminal.Param, NonTerminal.Param_list]
    },
    NonTerminal.Param: {
        NonTerminal.Declaration_initial.first: [NonTerminal.Declaration_initial, Action.add_function_param,
                                                NonTerminal.Param_prime]
    },
    NonTerminal.Param_prime: {
        (OPEN_BRACKET,): [OPEN_BRACKET, CLOSED_BRACKET, Action.param_type_to_array]
    },
    NonTerminal.Compound_stmt: {
        (OPEN_CURLY_BRACKET,): [OPEN_CURLY_BRACKET, Action.open_block, NonTerminal.Declaration_list,
                                NonTerminal.Statement_list,
                                Action.close_block, CLOSED_CURLY_BRACKET]
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
                               Action.pop_stack, Action.push_lineno, Action.placeholder_line,
                               NonTerminal.Statement, Action.push_lineno, Action.placeholder_line,
                               Action.jpf_from_skipped2, NonTerminal.Else_stmt, Action.jp_from_skipped1]
    },
    NonTerminal.Else_stmt: {
        (Keywords.ENDIF.value,): [Keywords.ENDIF.value],
        (Keywords.ELSE.value,): [Keywords.ELSE.value, NonTerminal.Statement, Keywords.ENDIF.value]
    },
    NonTerminal.Iteration_stmt: {
        (Keywords.FOR.value,): [Keywords.FOR.value, OPEN_PARENTHESIS, NonTerminal.Expression, SEMICOLON,
                                Action.push_lineno, NonTerminal.Expression, SEMICOLON,
                                Action.pop_stack,
                                Action.push_lineno, Action.placeholder_line,
                                Action.push_lineno, Action.placeholder_line,
                                Action.push_lineno,
                                NonTerminal.Expression, Action.jp_to_skipped4, CLOSED_PARENTHESIS,
                                Action.jp_from_skipped2,
                                NonTerminal.Statement,
                                Action.jp_to_skipped1, Action.jpf_from_skipped1]
    },
    NonTerminal.Return_stmt: {
        (Keywords.RETURN.value,): [Keywords.RETURN.value, NonTerminal.Return_stmt_prime, Action.function_return]
    },
    NonTerminal.Return_stmt_prime: {
        NonTerminal.Expression.first: [NonTerminal.Expression, Action.set_function_return_value, SEMICOLON],
        (SEMICOLON,): [SEMICOLON]
    },
    NonTerminal.Expression: {
        NonTerminal.Simple_expression_zegond.first: [NonTerminal.Simple_expression_zegond],
        (TokenType.ID,): [Action.push_id, TokenType.ID, NonTerminal.B]
    },
    NonTerminal.B: {
        (EQUAL,): [EQUAL, NonTerminal.Expression, Action.assign],
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
        NonTerminal.Relop.first: [Action.push_id, NonTerminal.Relop, NonTerminal.Additive_expression, Action.relop]
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
        NonTerminal.Addop.first: [Action.push_id, NonTerminal.Addop, NonTerminal.Term, Action.addsub, NonTerminal.D]
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
        (MULTIPLY_OPERATOR,): [MULTIPLY_OPERATOR, NonTerminal.Signed_factor, Action.multiply, NonTerminal.G]
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
        (TokenType.ID,): [Action.push_id, TokenType.ID, NonTerminal.Var_call_prime],
        (TokenType.NUM,): [Action.push_id, TokenType.NUM]
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
        (TokenType.NUM,): [Action.push_id, Action.push_stack, TokenType.NUM]
    },
    NonTerminal.Args: {
        NonTerminal.Arg_list.first: [Action.push_lineno,
                                     Action.placeholder_line,  # push return_value_placeholder
                                     Action.placeholder_line, Action.placeholder_line,  # push return_address
                                     Action.push_fp_value,
                                     NonTerminal.Arg_list, Action.call_function]
    },
    NonTerminal.Arg_list: {
        NonTerminal.Expression.first: [NonTerminal.Expression, NonTerminal.Arg_list_prime]
    },
    NonTerminal.Arg_list_prime: {
        (COMMA,): [COMMA, NonTerminal.Expression, NonTerminal.Arg_list_prime]
    }
}

epsilon_rule_actions = {
    NonTerminal.Factor_prime: [Action.push_stack],
    NonTerminal.Var_prime: [Action.push_stack]
}


def get_lexeme_or_type(token):
    return token.token_type.name if token.token_type in (TokenType.ID, TokenType.NUM) else token.lexeme


def get_terminal_or_type(terminal):
    return str(terminal.name) if isinstance(terminal, TokenType) else str(terminal)


unexpected_eof = False


class Parser:

    def __init__(self, scanner):
        self.scanner = scanner
        self.current_token = None
        self.errors = []
        self.code_generator = CodeGenerator()

    def parse_all(self):
        root = Node(str(NonTerminal.Program.name))
        self.get_next_token()
        self.parse(NonTerminal.Program, root)
        if not unexpected_eof: Node("$", root)
        return root

    def parse(self, current_state, current_node):
        global unexpected_eof
        for possible_token, rule in grammer_rules.get(current_state).items():
            if self.is_current_token_in(possible_token):
                for var in rule:
                    if isinstance(var, Action):
                        self.code_generator.codegen(var, self.current_token)
                    elif isinstance(var, NonTerminal):
                        node = Node(str(var.name.replace('_', '-')), current_node)
                        self.parse(var, node)
                        if unexpected_eof: return
                    else:
                        while True:
                            is_matched_or_skip = self.match_token(var, current_state, current_node)
                            if unexpected_eof: return
                            if is_matched_or_skip: break
                return
        if EPSILON in current_state.first and self.is_current_token_in(current_state.follow):
            Node(EPSILON, current_node)
            if current_state in epsilon_rule_actions:
                for action in epsilon_rule_actions[current_state]:
                    self.code_generator.codegen(action, None)
            return

        if self.is_current_token_in(current_state.follow):
            current_node.parent = None  # remove expected but missing current node
            self.add_error_missing_token(current_state.name)
        else:
            if self.current_token.token_type == TokenType.EOF:
                current_node.parent = None
                self.add_error_unexpected_eof()
                unexpected_eof = True
                return
            self.add_error_illegal_token()
            self.get_next_token()
            self.parse(current_state, current_node)

    def get_next_token(self):
        while True:
            next_token = self.scanner.get_next_token()
            if next_token.token_type not in (TokenType.WHITESPACE, TokenType.COMMENT):
                self.current_token = next_token
                return

    def match_token(self, expected_token, current_state, current_node):
        global unexpected_eof
        if self.is_current_token_in((expected_token,)):
            token_str = "(%s, %s)" % (self.current_token.token_type.name, self.current_token.lexeme)
            Node(token_str, current_node)
            self.get_next_token()
            return True
        else:
            if self.current_token.token_type == TokenType.EOF:
                self.add_error_unexpected_eof()
                unexpected_eof = True
                return False
            self.add_error_missing_token(get_terminal_or_type(expected_token))
            return True

    def is_current_token_in(self, input_set):
        return self.current_token.lexeme in input_set or self.current_token.token_type in input_set

    def add_error_missing_token(self, token):
        self.errors.append("#%s : syntax error, missing %s"
                           % (self.current_token.lineno, token.replace('_', '-')))
        print(self.errors[-1])

    def add_error_illegal_token(self):
        self.errors.append("#%s : syntax error, illegal %s"
                           % (self.current_token.lineno, get_lexeme_or_type(self.current_token)))
        print(self.errors[-1])

    def add_error_unexpected_eof(self):
        self.errors.append("#%s : syntax error, Unexpected EOF" % self.current_token.lineno)
        print(self.errors[-1])
