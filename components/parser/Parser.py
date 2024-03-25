from components.parser.NonTerminal import *
from operator import sub
from components.scanner.State import TokenType, Keywords


def without_epsilon(input):
    return tuple(x for x in input if x != EPSILON)


grammer_rules = {
    NonTerminal.PROGRAM: {
        without_epsilon(NonTerminal.DECLARATION_LIST.first): [NonTerminal.DECLARATION_LIST]
    },
    NonTerminal.DECLARATION_LIST: {
        NonTerminal.Declaration.first: [NonTerminal.Declaration, NonTerminal.DECLARATION_LIST]
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
        (OPEN_BRACKET,): [OPEN_BRACKET, TokenType.NUM, CLOSED_BRACKET]
    },
    NonTerminal.Fun_declaration_prime: {
        (OPEN_PARENTHESIS, ): [OPEN_PARENTHESIS, NonTerminal.Params, CLOSED_PARENTHESIS, NonTerminal.Compound_stmt]
    },
    NonTerminal.Type_specifier: {
        (Keywords.INT.value,): [Keywords.INT.value],
        (Keywords.VOID.value,): [Keywords.VOID.value]
    }
}


class Parser:

    def __init__(self, scanner):
        self.scanner = scanner
        self.current_token = scanner.get_next_token()

    def parse(self, current_state=NonTerminal.PROGRAM, parent=None):
        for first, rule in grammer_rules.get(current_state).items():
            if self.is_current_token_in_first(first):
                for var in rule:
                    if isinstance(var, NonTerminal):
                        self.match_non_terminal(var, current_state)
                    else:
                        self.match_terminal(var)
                return
        if EPSILON in current_state.first and self.current_token in current_state.follow:
            # This means we use epsilon rule here
            return
        # TODO: Handle errors

    def match_non_terminal(self, var, current_state):
        self.parse(var, current_state)

    def match_terminal(self, var):
        if self.current_token.lexeme == var or self.current_token.token_type == var:
            self.current_token = self.get_next_token()
        else:
            "error dide shode!"

    def get_next_token(self):
        while True:
            next_token = self.scanner.get_next_token()
            if next_token.token_type != TokenType.WHITESPACE:
                return next_token

    def is_current_token_in_first(self, first):
        return self.current_token.lexeme in first or self.current_token.token_type in first
