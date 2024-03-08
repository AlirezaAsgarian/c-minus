from dataclasses import dataclass

from components.ScannerDfa import ScannerDfa
from components.State import State, TokenType, KEYWORDS


class Scanner :


    def __init__(self, filepath):
        self.current_state = State.INITIAL_STATE
        self.buffer = ""
        self.source_file = open(filepath, "r")


    def eval_next_char(self, next_char):
        prev_state = self.current_state
        self.current_state = ScannerDfa.get_next_state(prev_state, next_char)

        if self.current_state == 'error':
            text = self.buffer
            self.reset()
            return self.handle_panic_mode(prev_state, text)

        self.buffer = self.buffer + next_char
        if self.current_state.is_final:  # State is final
            result_state = self.current_state
            if result_state.is_lookahead:
                result = self.buffer[:-1]
                self.move_file_cursor_to_previous_char()
            else:
                result = self.buffer
            self.reset()

            if(result_state.token_type == TokenType.ID and KEYWORDS.__contains__(result)):
                return Token(TokenType.KEYWORD, result)

            return Token(result_state.token_type, result)
        return None

    def move_file_cursor_to_previous_char(self):
        self.source_file.seek(self.source_file.tell() - 1)

    def get_next_token(self):
        while True:
            next_char = self.source_file.read(1)
            token = self.eval_next_char(next_char)
            if token == '': # Instead of EOF returns empty string
                return "$"
            if token is not None:
                return token

    def reset(self):
        self.current_state = State.INITIAL_STATE
        self.buffer = ""

    def handle_panic_mode(self, prev_state, text):
        pass

@dataclass
class Token:
    token_type: TokenType
    lexim: str

