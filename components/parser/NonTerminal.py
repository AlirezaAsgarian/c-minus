from enum import Enum, auto

from components.scanner.State import TokenType, EOF_VALUE
from components.scanner.State import Keywords as k

EPSILON = 'epsilon'
SEMICOLON = ";"
OPEN_PARENTHESIS = "("
CLOSED_PARENTHESIS = ")"
OPEN_BRACKET = "("
CLOSED_BRACKET = ")"
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


class NonTerminal(Enum):

    def __init__(self, id, first, follow):
        self.first = first
        self.follow = follow

    PROGRAM = (auto(), (EPSILON, k.INT.value, k.VOID.value), (EOF_VALUE,))
    DECLARATION_LIST = (auto(), (EPSILON, k.INT.value, k.VOID.value),
                        (EOF_VALUE, SEMICOLON, TokenType.ID, TokenType.NUM))
    Declaration = (auto(), (k.INT.value, k.VOID.value),
                   (TokenType.ID, SEMICOLON, TokenType.NUM, OPEN_PARENTHESIS, k.INT.value, k.VOID.value,
                    OPEN_CURLY_BRACKET, CLOSED_CURLY_BRACKET, k.BREAK.value, k.IF.value, k.FOR.value, k.RETURN.value,
                    MINUS, PLUS, EOF_VALUE))
    Declaration_initial = (auto(), (k.INT.value, k.VOID.value),
                           (SEMICOLON, OPEN_BRACKET, OPEN_PARENTHESIS, CLOSED_PARENTHESIS, COMMA))
    Declaration_prime = (auto(), (SEMICOLON, OPEN_BRACKET, OPEN_PARENTHESIS),
                         (TokenType.ID, SEMICOLON, TokenType.NUM, OPEN_PARENTHESIS, k.INT.value, k.VOID.value,
                          OPEN_CURLY_BRACKET, CLOSED_CURLY_BRACKET, k.BREAK.value, k.IF.value, k.FOR.value,
                          k.RETURN.value, PLUS, MINUS, EOF_VALUE))
    Var_declaration_prime = (auto(), (SEMICOLON, OPEN_BRACKET),
                             (TokenType.ID, SEMICOLON, TokenType.NUM, OPEN_PARENTHESIS, k.INT.value, k.VOID.value,
                              OPEN_CURLY_BRACKET, CLOSED_CURLY_BRACKET, k.BREAK.value, k.IF.value, k.FOR.value,
                              k.RETURN.value, PLUS, MINUS, EOF_VALUE))
    Fun_declaration_prime = (auto(), (OPEN_PARENTHESIS,),
                             (TokenType.ID, SEMICOLON, TokenType.NUM, OPEN_PARENTHESIS, k.INT.value, k.VOID.value,
                              OPEN_CURLY_BRACKET, CLOSED_CURLY_BRACKET, k.BREAK.value, k.IF.value, k.FOR.value,
                              k.RETURN.value, PLUS, MINUS, EOF_VALUE))
    Type_specifier = (auto(), (k.INT.value, k.VOID.value), (TokenType.ID,))
    Params = (auto(), (k.INT.value, k.VOID.value), (CLOSED_PARENTHESIS,))
    Param_list = (auto(), (COMMA, EPSILON), (CLOSED_PARENTHESIS,))
    Param = (auto(), (k.INT.value, k.VOID.value), (CLOSED_PARENTHESIS, COMMA))
    Param_prime = (auto(), (OPEN_BRACKET, EPSILON), (CLOSED_PARENTHESIS, COMMA))
    Compound_stmt = (auto(), (OPEN_CURLY_BRACKET,),
                     (TokenType.ID, SEMICOLON, TokenType.NUM, OPEN_PARENTHESIS, k.INT.value, k.VOID.value,
                      OPEN_CURLY_BRACKET, CLOSED_CURLY_BRACKET, k.BREAK.value, k.IF.value, k.ENDIF.value, k.ELSE.value,
                      k.FOR.value, k.RETURN.value, PLUS, MINUS, EOF_VALUE))
    Statement_list = (auto(),
                      (TokenType.ID, SEMICOLON, TokenType.NUM, OPEN_PARENTHESIS, COMMA, k.BREAK.value, k.IF.value,
                       k.FOR.value, k.RETURN.value, MINUS, PLUS, EPSILON),
                      (CLOSED_CURLY_BRACKET,))
    Statement = (auto(), (TokenType.ID, SEMICOLON, TokenType.NUM, OPEN_PARENTHESIS, OPEN_CURLY_BRACKET, k.BREAK.value,
                          k.IF.value, k.FOR.value, k.RETURN.value, PLUS, MINUS)
                 , (TokenType.ID, SEMICOLON, TokenType.NUM, OPEN_PARENTHESIS, OPEN_CURLY_BRACKET, CLOSED_CURLY_BRACKET,
                    k.BREAK.value, k.IF.value, k.ENDIF.value, k.ELSE.value, k.FOR.value, k.RETURN.value, PLUS, MINUS))
    Expression_stmt = (auto(), (TokenType.ID, SEMICOLON, TokenType.NUM, OPEN_PARENTHESIS, k.BREAK.value, PLUS, MINUS),
                       (TokenType.ID, SEMICOLON, TokenType.NUM, OPEN_PARENTHESIS, OPEN_CURLY_BRACKET,
                        CLOSED_CURLY_BRACKET, k.BREAK.value, k.IF.value, k.ENDIF.value, k.ELSE.value, k.FOR.value,
                        k.RETURN.value, PLUS, MINUS))
    Selection_stmt = (auto(), (k.IF.value,),
                      (TokenType.ID, SEMICOLON, TokenType.NUM, OPEN_PARENTHESIS, OPEN_CURLY_BRACKET,
                       CLOSED_CURLY_BRACKET, k.BREAK.value, k.IF.value, k.ENDIF.value, k.ELSE.value, k.FOR.value,
                       k.RETURN.value, PLUS, MINUS))
    Else_stmt = (auto(), (k.ENDIF.value, k.ELSE.value),
                 (TokenType.ID, SEMICOLON, TokenType.NUM, OPEN_PARENTHESIS, OPEN_CURLY_BRACKET, CLOSED_CURLY_BRACKET,
                  k.BREAK.value, k.IF.value, k.ENDIF.value, k.ELSE.value, k.FOR.value, k.RETURN.value, PLUS, MINUS))
    Iteration_stmt = (auto(), (k.FOR.value,),
                      (TokenType.ID, SEMICOLON, TokenType.NUM, OPEN_PARENTHESIS, OPEN_CURLY_BRACKET,
                       CLOSED_CURLY_BRACKET, k.BREAK.value, k.IF.value, k.ENDIF.value, k.ELSE.value, k.FOR.value,
                       k.RETURN.value, PLUS, MINUS))
    Return_stmt = (auto(), (k.RETURN.value,),
                   (TokenType.ID, SEMICOLON, TokenType.NUM, OPEN_PARENTHESIS, OPEN_CURLY_BRACKET, CLOSED_CURLY_BRACKET,
                    k.BREAK.value, k.IF.value, k.ENDIF.value, k.ELSE.value, k.FOR.value, k.RETURN.value, PLUS, MINUS))
    Return_stmt_prime = (auto(), (TokenType.ID, COMMA, TokenType.NUM, OPEN_PARENTHESIS, PLUS, MINUS),
                         (TokenType.ID, SEMICOLON, TokenType.NUM, OPEN_PARENTHESIS, OPEN_CURLY_BRACKET,
                          CLOSED_CURLY_BRACKET, k.BREAK.value, k.IF.value, k.ENDIF.value, k.ELSE.value, k.FOR.value,
                          k.RETURN.value, PLUS, MINUS))
    Expression = (auto(), (TokenType.ID, TokenType.NUM, OPEN_PARENTHESIS, PLUS, MINUS),
                  (SEMICOLON, CLOSED_BRACKET, CLOSED_PARENTHESIS, COMMA))
    B = (auto(), (OPEN_BRACKET, OPEN_PARENTHESIS, EQUAL, k.RETURN.value, LESS_THAN, EQUALITY_OPERATOR, PLUS, MINUS,
                  MULTIPLY_OPERATOR, EPSILON),
         (SEMICOLON, CLOSED_BRACKET, CLOSED_PARENTHESIS, COMMA))
    H = (auto(), (EQUAL, LESS_THAN, EQUALITY_OPERATOR, PLUS, MINUS, MULTIPLY_OPERATOR, EPSILON),
         (SEMICOLON, CLOSED_BRACKET, CLOSED_PARENTHESIS, COMMA))
    Simple_expression_zegond = (auto(), (TokenType.NUM, OPEN_PARENTHESIS, PLUS, MINUS),
                                (SEMICOLON, CLOSED_BRACKET, CLOSED_PARENTHESIS, COMMA))
    Simple_expression_prime = (auto(), (OPEN_PARENTHESIS, LESS_THAN, EQUALITY_OPERATOR, PLUS, MINUS, MULTIPLY_OPERATOR,
                                        EPSILON), (SEMICOLON, CLOSED_BRACKET, CLOSED_PARENTHESIS, COMMA))
    C = (auto(), (LESS_THAN, EQUALITY_OPERATOR, EPSILON), (SEMICOLON, CLOSED_BRACKET, CLOSED_PARENTHESIS, COMMA))
    RELOP = (auto(), (LESS_THAN, EQUALITY_OPERATOR), (TokenType.ID, TokenType.NUM, OPEN_CURLY_BRACKET, PLUS, MINUS))
    Additive_expression = (auto(), (TokenType.ID, TokenType.NUM, OPEN_PARENTHESIS, MINUS, PLUS),
                           (SEMICOLON, CLOSED_BRACKET, CLOSED_CURLY_BRACKET, COMMA))
    Additive_expression_prime = (auto(), (OPEN_PARENTHESIS, PLUS, MINUS, MULTIPLY_OPERATOR, EPSILON),
                                 (SEMICOLON, CLOSED_BRACKET, CLOSED_PARENTHESIS, COMMA, LESS_THAN, EQUALITY_OPERATOR))
    Additive_expression_zegond = (auto(), (TokenType.NUM, OPEN_PARENTHESIS, MINUS, PLUS),
                                  (SEMICOLON, CLOSED_BRACKET, CLOSED_PARENTHESIS, COMMA, LESS_THAN, EQUALITY_OPERATOR))
    D = (auto(), (PLUS, MINUS, EPSILON),
         (SEMICOLON, CLOSED_BRACKET, CLOSED_PARENTHESIS, COMMA, LESS_THAN, EQUALITY_OPERATOR))
    Addop = (auto(), (PLUS, MINUS), (TokenType.ID, TokenType.NUM, OPEN_PARENTHESIS, PLUS, MINUS))
    Term = (auto(), (TokenType.ID, TokenType.NUM, OPEN_PARENTHESIS, PLUS, MINUS),
            (SEMICOLON, CLOSED_BRACKET, CLOSED_PARENTHESIS, COMMA, LESS_THAN, EQUALITY_OPERATOR, PLUS, MINUS))
    Term_prime = (auto(), (OPEN_PARENTHESIS, MULTIPLY_OPERATOR, EPSILON),
                  (SEMICOLON, CLOSED_BRACKET, CLOSED_PARENTHESIS, COMMA, LESS_THAN, EQUALITY_OPERATOR, PLUS, MINUS))
    Term_zegond = (auto(), (TokenType.NUM, OPEN_PARENTHESIS, PLUS, MINUS),
                   (SEMICOLON, CLOSED_BRACKET, CLOSED_PARENTHESIS, COMMA, LESS_THAN, EQUALITY_OPERATOR, PLUS, MINUS))
    G = (auto(), (MULTIPLY_OPERATOR, EPSILON),
         (SEMICOLON, CLOSED_BRACKET, CLOSED_PARENTHESIS, COMMA, LESS_THAN, EQUALITY_OPERATOR, PLUS, MINUS))
    Signed_factor = (auto(), (TokenType.ID, TokenType.NUM, OPEN_PARENTHESIS, PLUS, MINUS),
                     (SEMICOLON, CLOSED_BRACKET, CLOSED_PARENTHESIS, COMMA, LESS_THAN, EQUALITY_OPERATOR, PLUS, MINUS,
                      MULTIPLY_OPERATOR))
    Signed_factor_prime = (auto(), (OPEN_PARENTHESIS, EPSILON),
                           (SEMICOLON, CLOSED_BRACKET, CLOSED_PARENTHESIS, COMMA, LESS_THAN, EQUALITY_OPERATOR, PLUS,
                            MINUS, MULTIPLY_OPERATOR))
    Signed_factor_zegond = (auto(), (TokenType.NUM, OPEN_PARENTHESIS, PLUS, MINUS),
                            (SEMICOLON, CLOSED_BRACKET, CLOSED_PARENTHESIS, COMMA, LESS_THAN, EQUALITY_OPERATOR, PLUS,
                             MINUS, MULTIPLY_OPERATOR))
    Factor = (auto(), (TokenType.ID, TokenType.NUM, OPEN_PARENTHESIS),
              (SEMICOLON, CLOSED_BRACKET, CLOSED_PARENTHESIS, COMMA, LESS_THAN, EQUALITY_OPERATOR, PLUS, MINUS,
               MULTIPLY_OPERATOR))
    Var_call_prime = (auto(), (OPEN_BRACKET, OPEN_PARENTHESIS, EPSILON),
                      (SEMICOLON, CLOSED_BRACKET, CLOSED_PARENTHESIS, COMMA, LESS_THAN, EQUALITY_OPERATOR, PLUS, MINUS,
                       MULTIPLY_OPERATOR))
    Var_prime = (auto(), (OPEN_BRACKET, EPSILON),
                 (SEMICOLON, CLOSED_BRACKET, CLOSED_PARENTHESIS, COMMA, LESS_THAN, EQUALITY_OPERATOR, PLUS, MINUS,
                  MULTIPLY_OPERATOR))
    Factor_prime = (auto(), (OPEN_PARENTHESIS, EPSILON),
                    (SEMICOLON, CLOSED_BRACKET, CLOSED_PARENTHESIS, COMMA, LESS_THAN, EQUALITY_OPERATOR, PLUS, MINUS,
                     MULTIPLY_OPERATOR))
    Factor_zegond = (auto(), (TokenType.NUM, OPEN_PARENTHESIS),
                     (SEMICOLON, CLOSED_BRACKET, CLOSED_PARENTHESIS, COMMA, LESS_THAN, EQUALITY_OPERATOR, PLUS, MINUS,
                      MULTIPLY_OPERATOR))
    Args = (auto(), (TokenType.ID, TokenType.NUM, OPEN_PARENTHESIS, PLUS, MINUS, EPSILON), (CLOSED_PARENTHESIS,))
    Arg_list = (auto(), (TokenType.ID, TokenType.NUM, OPEN_PARENTHESIS, MINUS, PLUS), (CLOSED_PARENTHESIS,))
    Arg_list_prime = (auto(), (COMMA, EPSILON), (CLOSED_PARENTHESIS,))
