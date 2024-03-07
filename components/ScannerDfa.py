import re

from components.State import State, Pattern


class ScannerDfa:
    nextState = {
        State.INITIAL_STATE: {
            Pattern.DIGIT: State.VISIT_NUM_STATE,
            Pattern.COMMENT_SLASH_SYMBOL: State.VISIT_SLASH_COMMENT_STATE,
            Pattern.SYMBOL_WITHOUT_EQUAL: State.FINAL_VISIT_EXCEPT_EQUAL_SYMBOL_STATE,
            Pattern.EQUAL: State.VISIT_EQUAL_SYMBOL_STATE,
            Pattern.WHITESPACE: State.FINAL_WHITESPACE_STATE,
            Pattern.LETTER: State.VISIT_LETTER_ID_STATE,
            Pattern.EOF : State.FINAL_EOF_STATE
        },
        State.VISIT_NUM_STATE: {
            # Todo : Add error handling state for number like 123d
            Pattern.NOT_DIGIT: State.FINAL_NUM_STATE,
            Pattern.DIGIT: State.VISIT_NUM_STATE
        },
        State.VISIT_LETTER_ID_STATE: {
            Pattern.LETTER_DIGIT: State.VISIT_LETTER_ID_STATE,
            Pattern.NOT_LETTER_DIGIT: State.FINAL_ID_STATE
        },
        State.VISIT_EQUAL_SYMBOL_STATE: {
            Pattern.EQUAL: State.FINAL_VISIT_DOUBLE_EQUAL_SYMOBL_STATE,
            Pattern.NOT_EQUAL: State.FINAL_NOT_VISIT_SECOND_EQUAL_SYMBOL_STATE
        },
        State.VISIT_SLASH_COMMENT_STATE: {
            Pattern.COMMENT_STAR_SYMBOL: State.VISIT_STAR_AFTER_SLASH_COMMENT_STATE
        },
        State.VISIT_STAR_AFTER_SLASH_COMMENT_STATE: {
            # Todo: Add Handling EOF here
            Pattern.COMMENT_STAR_SYMBOL: State.VISIT_SECOND_STAR_AFTER_SLASH_COMMENT_STATE,
            Pattern.NOT_EOF: State.VISIT_STAR_AFTER_SLASH_COMMENT_STATE
        },
        State.VISIT_SECOND_STAR_AFTER_SLASH_COMMENT_STATE: {
            Pattern.COMMENT_SLASH_SYMBOL: State.FINAL_SLASH_STAR_COMMENT_STATE,
            Pattern.NOT_COMMENT_SLASH_SYMBOL: State.VISIT_STAR_AFTER_SLASH_COMMENT_STATE
        }
    }

    @staticmethod
    def get_next_state(current, next_char):
        state = ScannerDfa.nextState.get(current)
        if state is None:
            raise "Unexpected State called in get next state method !!!"
        for pattern, next_state in state.items():
            if re.findall(pattern, next_char):
                return next_state
        # Todo: Add error handling
        return "error"
