from dataclasses import dataclass

from components.ScannerDfa import *
from components.State import *


class Scanner:

    def __init__(self, source_file):
        self.file_reader = FileReader(source_file)
        self.symbols = KEYWORDS[:]
        self.errors = []

    def read_token(self):
        lineno = self.file_reader.lineno
        dfa = ScannerDfa()
        current_token = ""
        while True:
            char = self.file_reader.read_one_char()
            current_token += char
            dfa.read_char(char)

            dfa_state = dfa.current_state

            if type(dfa_state) is LexicalError:
                error = dfa_state
                invalid_chars = current_token
                if error is LexicalError.UNCLOSED_COMMENT:
                    if len(invalid_chars) > 7:
                        invalid_chars = invalid_chars[:7] + "..."
                return Error(lineno, invalid_chars, error.value)

            elif dfa_state.token_type is not None:
                if dfa_state.is_lookahead:
                    current_token = current_token[:-1]
                    self.file_reader.back_one_char()

                token = Token(lineno, dfa_state.token_type, current_token)

                if dfa_state.token_type == TokenType.ID:
                    if current_token in KEYWORDS:
                        token.token_type = TokenType.KEYWORD
                    elif current_token not in self.symbols:
                        self.symbols.append(current_token)

                return token

    def get_next_token(self):
        while True:
            token_or_error = self.read_token()
            if type(token_or_error) is Error:
                self.errors.append(token_or_error)
            else:
                return token_or_error

    def handle_panic_mode(self, prev_state, text):
        pass


class FileReader:

    def __init__(self, file):
        self.file = file
        self.content = file.read()
        self.ptr = 0
        self.lineno = 1

    def read_one_char(self):
        if self.ptr >= len(self.content): return ''
        char = self.content[self.ptr]
        self.ptr += 1
        if char == '\n': self.lineno += 1
        return char

    def back_one_char(self):
        self.ptr -= 1
        self.lineno -= self.content[self.ptr] == '\n'


@dataclass
class Token:
    lineno: int
    token_type: TokenType
    lexeme: str


@dataclass
class Error:
    lineno: int
    buffer: str
    message: str
