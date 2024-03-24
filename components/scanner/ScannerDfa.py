import re

from components.scanner.State import *


class ScannerDfa:

    def __init__(self):
        self.current_state = State.START

    states = {
        State.START: {
            Pattern.EOF: State.EOF_FINAL,
            Pattern.DIGIT: State.NUM_CANDIDATE,
            Pattern.SLASH: State.SLASH_VISITED,
            Pattern.STAR: State.STAR_VISITED,
            Pattern.EQUAL: State.EQUAL_VISITED,
            Pattern.SYMBOLS: State.SYMBOL_FINAL_NO_LOOKAHEAD,
            Pattern.WHITESPACE: State.WHITESPACE_FINAL,
            Pattern.LETTER: State.ID_CANDIDATE,
        },
        State.NUM_CANDIDATE: {
            Pattern.DIGIT: State.NUM_CANDIDATE,
            Pattern.LETTER: LexicalError.INVALID_NUMBER,
            Pattern.ALL_VALID: State.NUM_FINAL,
        },
        State.ID_CANDIDATE: {
            Pattern.LETTER_DIGIT: State.ID_CANDIDATE,
            Pattern.ALL_VALID: State.ID_FINAL
        },
        State.STAR_VISITED: {
            Pattern.SLASH: LexicalError.UNMATCHED_COMMENT,
            Pattern.ALL_VALID: State.SYMBOL_FINAL_LOOKAHEAD_NOT_MATCHED
        },
        State.EQUAL_VISITED: {
            Pattern.EQUAL: State.SYMBOL_FINAL_LOOKAHEAD_MATCHED,
            Pattern.ALL_VALID: State.SYMBOL_FINAL_LOOKAHEAD_NOT_MATCHED
        },
        State.SLASH_VISITED: {
            Pattern.SLASH: State.LINECOMMENT_OPENED,
            Pattern.STAR: State.BLOCKCOMMENT_OPENED,
        },
        State.LINECOMMENT_OPENED: {
            Pattern.NEWLINE: State.LINECOMMENT_FINAL,
            Pattern.EOF: State.LINECOMMENT_FINAL,
            Pattern.ALL: State.LINECOMMENT_OPENED
        },
        State.BLOCKCOMMENT_OPENED: {
            Pattern.STAR: State.BLOCKCOMMENT_END_CANDIDATE,
            Pattern.EOF: LexicalError.UNCLOSED_COMMENT,
            Pattern.ALL: State.BLOCKCOMMENT_OPENED
        },
        State.BLOCKCOMMENT_END_CANDIDATE: {
            Pattern.STAR: State.BLOCKCOMMENT_END_CANDIDATE,
            Pattern.SLASH: State.BLOCKCOMMENT_FINAL,
            Pattern.ALL: State.BLOCKCOMMENT_OPENED
        }
    }

    def read_char(self, char):
        for pattern, next_state in ScannerDfa.states[self.current_state].items():
            if re.match(pattern, char, re.DOTALL):
                self.current_state = next_state
                break
        else: self.current_state = LexicalError.INVALID_INPUT
