from enum import Enum, auto


class Keywords(Enum):
    IF = 'if'
    ELSE = 'else'
    VOID = 'void'
    INT = 'int'
    FOR = 'for'
    BREAK = 'break'
    RETURN = 'return'
    ENDIF = 'endif'


KEYWORDS = [keyword.value for keyword in Keywords]
EOF_VALUE = "$"


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
    WHITESPACE = r'[ \n\r\t\v\f]'
    SYMBOLS = r'[;:,<=\[\]\(\)\{\}\+\-\*]'
    STAR = r'\*'
    EQUAL = r'='
    SLASH = r'/'
    NEWLINE = r'\n'
    EOF = r'\Z'
    ALL_VALID = '|'.join((LETTER, DIGIT, SYMBOLS, SLASH, WHITESPACE, EOF))
    ALL = r'.'


class State(Enum):

    def __init__(self, id, token_type=None, is_lookahead=False):
        self.token_type = token_type
        self.is_lookahead = is_lookahead

    START = (auto())

    # Num states
    # State which shows we see first number
    NUM_CANDIDATE = (auto())
    # When we see something except number, and we should return visited number as token
    NUM_FINAL = (auto(), TokenType.NUM, True)

    # Letter states
    # State which shows we see first letter
    ID_CANDIDATE = (auto())
    # when see except number and letter we should return visited id as token
    ID_FINAL = (auto(), TokenType.ID, True)

    # Symbol states
    # When visit symbol except '=' we should return it as token
    SYMBOL_FINAL_NO_LOOKAHEAD = (auto(), TokenType.SYMBOL)
    STAR_VISITED = (auto())
    EQUAL_VISITED = (auto())
    SYMBOL_FINAL_LOOKAHEAD_MATCHED = (auto(), TokenType.SYMBOL)
    SYMBOL_FINAL_LOOKAHEAD_NOT_MATCHED = (auto(), TokenType.SYMBOL, True)

    # Comment states
    SLASH_VISITED = (auto())
    LINECOMMENT_OPENED = (auto())
    LINECOMMENT_FINAL = (auto(), TokenType.COMMENT)
    BLOCKCOMMENT_OPENED = (auto())
    BLOCKCOMMENT_END_CANDIDATE = (auto())
    BLOCKCOMMENT_FINAL = (auto(), TokenType.COMMENT)

    # Whitespace state
    WHITESPACE_FINAL = (auto(), TokenType.WHITESPACE)

    # EOF state
    EOF_FINAL = (auto(), TokenType.EOF)


class LexicalError(Enum):
    INVALID_INPUT = "Invalid input"
    INVALID_NUMBER = "Invalid number"
    UNMATCHED_COMMENT = "Unmatched comment"
    UNCLOSED_COMMENT = "Unclosed comment"
