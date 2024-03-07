from components.ScannerDfa import ScannerDfa
from components.State import State


class Scanner :


    def __init__(self, filepath):
        self.current_state = State.INITIAL_STATE
        self.buffer = ""
        self.source_file = open(filepath, "r")


    def eval_next_char(self, next_char):
        self.current_state = ScannerDfa.get_next_state(self.current_state, next_char)
        self.buffer = self.buffer + next_char
        if self.current_state.is_final:  # State is final
            if self.current_state.is_lookahead:
                result = self.buffer[:-1]
                self.source_file.seek(self.source_file.tell() - 1)
            else:
                result = self.buffer
            self.reset()
            return result
        return None



    def get_next_token(self):
        while(True):
            next_char = self.source_file.read(1)
            token = self.eval_next_char(next_char)
            if token is not None:
                return token



    def reset(self):
        self.current_state = State.INITIAL_STATE
        self.buffer = ""

