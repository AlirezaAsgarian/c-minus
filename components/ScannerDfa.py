import re

from components.State import *


class ScannerDfa:
    nextState = {
        State.INITIAL_STATE: {
            Pattern.DIGIT: State.NUMBER_CANDIDATE,
            Pattern.COMMENT_SLASH_SYMBOL: State.SLASH_VISITED,
            Pattern.STAR: State.STAR_VISITED,
            Pattern.EQUAL: State.EQUAL_VISITED,
            Pattern.SYMBOLS_EXCEPT_EQUAL: State.SYMBOL_FINAL_NO_LOOKAHEAD,
            Pattern.WHITESPACE: State.WHITESPACE_FINAL,
            Pattern.LETTER: State.ID_CANDIDATE,
            Pattern.EOF: State.FINAL_EOF_STATE,
            Pattern.ALL: LexicalError.INVALID_INPUT
        },
        State.NUMBER_CANDIDATE: {
            Pattern.DIGIT: State.NUMBER_CANDIDATE,
            Pattern.LETTER: LexicalError.INVALID_NUMBER,
            Pattern.ALL: State.FINAL_NUM_STATE,
        },
        State.ID_CANDIDATE: {
            Pattern.LETTER_DIGIT: State.ID_CANDIDATE,
            Pattern.ALL: State.ID_FINAL
        },
        State.STAR_VISITED: {
            Pattern.COMMENT_SLASH_SYMBOL: LexicalError.UNMATCHED_COMMENT,
            Pattern.ALL: State.SYMBOL_FINAL_LOOKAHEAD_NOT_MATCHED
        },
        State.EQUAL_VISITED: {
            Pattern.EQUAL: State.SYMBOL_FINAL_LOOKAHEAD_MATCHED,
            Pattern.ALL: State.SYMBOL_FINAL_LOOKAHEAD_NOT_MATCHED
        },
        State.SLASH_VISITED: {
            Pattern.COMMENT_SLASH_SYMBOL: State.LINECOMMENT_OPENNED,
            Pattern.COMMENT_STAR_SYMBOL: State.BLOCKCOMMENT_OPENNED,
            Pattern.ALL: LexicalError.INVALID_INPUT
        },
        State.LINECOMMENT_OPENNED: {
            Pattern.NEWLINE: State.LINECOMMENT_FINAL,
            Pattern.EOF: State.LINECOMMENT_FINAL,
            Pattern.ALL: State.LINECOMMENT_OPENNED
        },
        State.BLOCKCOMMENT_OPENNED: {
            Pattern.COMMENT_STAR_SYMBOL: State.BLOCKCOMMENT_END_CANDIDATE,
            r'\$': LexicalError.UNCLOSED_COMMENT,
            Pattern.ALL: State.BLOCKCOMMENT_OPENNED
        },
        State.BLOCKCOMMENT_END_CANDIDATE: {
            Pattern.COMMENT_STAR_SYMBOL: State.BLOCKCOMMENT_END_CANDIDATE,
            Pattern.COMMENT_SLASH_SYMBOL: State.BLOCKCOMMENT_FINAL,
            Pattern.ALL: State.BLOCKCOMMENT_OPENNED
        }
    }

    @staticmethod
    def get_next_state(current, next_char):
        # print("A '"+next_char+"'")
        state = ScannerDfa.nextState.get(current)
        if state is None:
            raise "Unexpected State called in get next state method !!!"
        for pattern, next_state in state.items():
            if re.findall(pattern, next_char, re.DOTALL):
                return next_state
        raise AssertionError
