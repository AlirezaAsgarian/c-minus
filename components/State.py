from enum import Enum
from string import whitespace

KEYWORDS = ['if', 'else', 'void', 'int', 'for', 'break', 'return', 'endif']


class TokenType(Enum):
    NUM = 0
    ID = 1
    KEYWORD = 2
    SYMBOL = 3
    COMMENT = 4
    WHITESPACE = 5
    EOF = 6


class Pattern:
    LETTER = r'[a-zA-Z]'
    DIGIT = r'[0-9]'
    LETTER_DIGIT = r'[0-9a-zA-Z]'
    NOT_LETTER_DIGIT = r'[^0-9A-z]'
    NOT_DIGIT = r'[^0-9]'
    WHITESPACE = r'[\s' + whitespace + ']'
    SYMBOLS_EXCEPT_EQUAL = r'[;:,\[\]\(\)\{\}\+\-\*<]'
    STAR = r'\*'
    EQUAL = r'='
    NOT_EQUAL = r'[^=]'
    COMMENT_SLASH_SYMBOL = r'/'
    NOT_COMMENT_SLASH_SYMBOL = r'[^/]'
    COMMENT_STAR_SYMBOL = r'[*]'
    ALL = r'.'
    NEWLINE = r'\n'
    EOF = r'^$'
    NOT_EOF = r'[^' + chr(3) + ']'


# If you have two similar constructor for enums in python it consider them as one enum not two, so we should add a
# id for each them. for this purpose we use counter
counter = iter(range(1000000))


# use auto() ?
class State(Enum):

    def __init__(self, id, is_final, is_lookahead, token_type=None):
        self.is_final = is_final
        self.is_lookahead = is_lookahead
        self.token_type = token_type

    INITIAL_STATE = (next(counter), False, False)

    # Num states
    # State which shows we see first number
    NUMBER_CANDIDATE = (next(counter), False, False)
    # When see something except number and we should return visited number as token
    FINAL_NUM_STATE = (next(counter), True, True, TokenType.NUM)

    # Letter states
    # State which shows we see first letter
    ID_CANDIDATE = (next(counter), False, False)
    # when see except number and letter we should return visited id as token
    ID_FINAL = (next(counter), True, True, TokenType.ID)

    # Symbol states
    # When visit symbol except '=' we should returns it as token
    SYMBOL_FINAL_NO_LOOKAHEAD = (next(counter), True, False, TokenType.SYMBOL)
    STAR_VISITED = (next(counter), False, False)
    EQUAL_VISITED = (next(counter), False, False)
    SYMBOL_FINAL_LOOKAHEAD_MATCHED = (next(counter), True, False, TokenType.SYMBOL)
    SYMBOL_FINAL_LOOKAHEAD_NOT_MATCHED = (next(counter), True, True, TokenType.SYMBOL)

    # Comment states
    SLASH_VISITED = (next(counter), False, False)
    LINECOMMENT_OPENNED = (next(counter), False, False)
    LINECOMMENT_FINAL = (next(counter), True, False, TokenType.COMMENT)
    BLOCKCOMMENT_OPENNED = (next(counter), False, False)
    BLOCKCOMMENT_END_CANDIDATE = (next(counter), False, False)
    BLOCKCOMMENT_FINAL = (next(counter), True, False, TokenType.COMMENT)

    # Whitespace state
    WHITESPACE_FINAL = (next(counter), True, False, TokenType.WHITESPACE)

    # EOF state
    FINAL_EOF_STATE = (next(counter), True, False, TokenType.EOF)


class LexicalError(Enum):
    INVALID_INPUT = "Invalid input"
    INVALID_NUMBER = "Invalid number"
    UNMATCHED_COMMENT = "Unmatched comment"
    UNCLOSED_COMMENT = "Unclosed comment"
