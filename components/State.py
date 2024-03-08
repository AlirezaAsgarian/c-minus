from dataclasses import dataclass
from enum import Enum
from string import ascii_letters, digits, whitespace, printable
from typing import List, Union, Optional

KEYWORDS = ['break', 'continue', 'void', 'else', 'if', 'return', 'while', 'main']

class TokenType(Enum):
    NUM = 0
    ID = 1
    KEYWORD = 2
    SYMBOL = 3
    COMMENT = 4
    WHITESPACE = 5
    EOF = 6


class Pattern:
    LETTER = r'[A-z]'
    DIGIT = r'[0-9]'
    LETTER_DIGIT = r'[0-9A-z]'
    NOT_LETTER_DIGIT = r'[^0-9A-z]'
    NOT_DIGIT = r'[^0-9]'
    WHITESPACE = r'[\s' + whitespace + ']'
    SYMBOL_WITHOUT_EQUAL = r'[;:,\[\]\(\)\{\}\+\-\*<]'
    EQUAL = r'='
    NOT_EQUAL = r'[^=]'
    COMMENT_SLASH_SYMBOL = r'/'
    NOT_COMMENT_SLASH_SYMBOL = r'[^/]'
    COMMENT_STAR_SYMBOL = r'[*]'
    ALL = r'.'
    EOF = r'^$'
    NOT_EOF = r'[^' + chr(3) + ']'

# If you have two similar constructor for enums in python it consider them as one enum not two, so we should add a
# id for each them. for this purpose we use counter
counter = iter(range(1000000))


class State(Enum):

    def __init__(self, id, is_final, is_lookahead, token_type=None):
        self.is_final = is_final
        self.is_lookahead = is_lookahead
        self.token_type = token_type

    INITIAL_STATE = (next(counter), False, False)

    # Num states
    # State which shows we see first number
    VISIT_NUM_STATE = (next(counter), False, False)
    # When see something except number and we should return visited number as token
    FINAL_NUM_STATE = (next(counter), True, True, TokenType.NUM)

    # Letter states
    # State which shows we see first letter
    VISIT_LETTER_ID_STATE = (next(counter), False, False)
    # when see except number and letter we should return visited id as token
    FINAL_ID_STATE = (next(counter), True, True, TokenType.ID)

    # Symbol states
    # When visit symbol except '=' we should returns it as token
    FINAL_VISIT_EXCEPT_EQUAL_SYMBOL_STATE = (next(counter), True, False, TokenType.SYMBOL)
    VISIT_EQUAL_SYMBOL_STATE = (next(counter), False, False)
    FINAL_VISIT_DOUBLE_EQUAL_SYMOBL_STATE = (next(counter), True, False, TokenType.SYMBOL)
    FINAL_NOT_VISIT_SECOND_EQUAL_SYMBOL_STATE = (next(counter), True, True, TokenType.SYMBOL)

    # Comment states
    VISIT_SLASH_COMMENT_STATE = (next(counter), False, False)
    VISIT_STAR_AFTER_SLASH_COMMENT_STATE = (next(counter), False, False)
    VISIT_SECOND_STAR_AFTER_SLASH_COMMENT_STATE = (next(counter), False, False)
    FINAL_SLASH_STAR_COMMENT_STATE = (next(counter), True, False, TokenType.COMMENT)

    # Whitespace state
    FINAL_WHITESPACE_STATE = (next(counter), True, False, TokenType.WHITESPACE)

    # EOF state
    FINAL_EOF_STATE = (next(counter), True, False, TokenType.EOF)

