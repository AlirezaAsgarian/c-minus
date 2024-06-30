from dataclasses import dataclass
from enum import Enum, auto
from typing import List

from components.scanner.State import TokenType


class SymbolTable:
    def __init__(self, starting_offset):
        self.offset = starting_offset  # can be optimized when popping from stack
        self.table_stack = []

    def add_symbol(self, symbol, size=None, is_param=False):
        self.table_stack[-1][symbol] = Variable(self.offset, size, is_param)
        self.offset += 4 if size is None else 4 * size

    def get_symbol(self, symbol):
        for table in self.table_stack[::-1]:
            if symbol in table:
                return table[symbol]
        return None

    def push_empty_stack(self):
        self.table_stack.append({})

    def pop_stack(self):
        self.table_stack.pop()


SP = 500
FP = 504
TEMP = 508
DATA = 0
STACK_START = TEMP + 4

class CodeGenerator:

    def __init__(self):
        self.codes = []
        self.global_table = SymbolTable(DATA)
        self.global_table.push_empty_stack()
        self.function_table: SymbolTable = None
        self.semantic_stack = []
        self.functions = {"output": Function("void", None, [["input", "int"]])}
        self.current_function = None
        self.return_block_lineno = None
        self.loop_blocks = []
        self.semantic_errors = []
        self.append_code((Code.ASSIGN, constant(STACK_START), direct(SP)))
        self.append_code((Code.ASSIGN, constant(STACK_START), direct(FP)))

    def append_code(self, code):
        self.codes.append(code)

    def set_code_push(self, lineno, value):
        if value is not None:
            self.codes[lineno] = (Code.ASSIGN, value, indirect(SP))
            lineno += 1
        self.codes[lineno] = (Code.ADD, direct(SP), constant(4), direct(SP))

    def append_code_push(self, value):
        lineno = len(self.codes)
        if value is not None: self.append_code(())
        self.append_code(())
        self.set_code_push(lineno, value)

    def append_code_pop(self):
        self.append_code((Code.SUB, direct(SP), constant(4), direct(SP)))

    def codegen(self, action, token, input_lineno):

        if action == Action.push_id:
            self.semantic_stack.append(token)

        elif action == Action.register_function:
            function_name = self.semantic_stack.pop().lexeme
            return_type = self.semantic_stack.pop().lexeme
            self.current_function = function_name
            lineno = len(self.codes)
            self.functions[function_name] = Function(return_type, lineno, [])

        elif action == Action.add_function_param:
            param_name = self.semantic_stack.pop().lexeme
            param_type = self.semantic_stack.pop().lexeme
            self.functions[self.current_function].parameters.append([param_name, param_type])

        elif action == Action.param_type_to_array:
            self.functions[self.current_function].parameters[-1][1] = "array"

        elif action == Action.return_code_block:
            self.return_block_lineno = len(self.codes)
            self.codes.append((Code.SUB, direct(FP), constant(4), direct(SP)))
            self.codes.append((Code.ASSIGN, indirect(SP), direct(FP)))
            self.append_code_pop()
            self.codes.append((Code.ASSIGN, indirect(SP), direct(TEMP)))
            self.codes.append((Code.JP, indirect(TEMP)))

        elif action == Action.function_return:
            self.codes.append((Code.JP, self.return_block_lineno))

        elif action == Action.set_function_return_value:
            self.append_code_pop()
            self.semantic_stack.pop()
            self.codes.append((Code.SUB, direct(FP), constant(12), direct(TEMP)))
            self.codes.append((Code.ASSIGN, indirect(SP), indirect(TEMP)))

        elif action == Action.call_main:
            fixlineno = self.semantic_stack.pop()
            lineno = len(self.codes)
            self.set_code_push(fixlineno, constant(lineno))
            self.codes[fixlineno + 4] = (Code.ASSIGN, direct(SP), direct(FP),)
            self.codes[fixlineno + 5] = (Code.JP, self.functions["main"].address)

        elif action == Action.call_function:
            args = []
            while self.semantic_stack[-1] != "args_begin":
                args.append(self.semantic_stack.pop())
            args.reverse()
            self.semantic_stack.pop()
            fixlineno = self.semantic_stack.pop()
            function_name = self.semantic_stack.pop().lexeme
            function = self.functions[function_name]
            if len(args) != len(function.parameters):
                self.error_argn_mismatch(input_lineno, function_name)
            function_parameter_types = [x[1] for x in function.parameters]
            for i, got, expected in zip(range(len(args)), args, function_parameter_types):
                if got != expected:
                    self.error_parameter_type_mismatch(input_lineno, function_name, i, got, expected)
            if function_name == "output":
                self.codes[fixlineno] = (Code.ASSIGN, direct(0), direct(0))
                self.codes[fixlineno + 1] = (Code.ASSIGN, direct(0), direct(0))
                self.codes[fixlineno + 2] = (Code.ASSIGN, direct(0), direct(0))
                self.append_code_pop()
                self.append_code((Code.PRINT, indirect(SP)))
                self.append_code_pop()
                self.semantic_stack.append("int")
                return
            self.set_code_push(fixlineno, None)
            self.codes.append((Code.SUB, direct(SP), constant(4 * len(function.parameters)), direct(FP)))
            self.codes.append((Code.JP, function.address))
            lineno = len(self.codes)
            self.set_code_push(fixlineno + 1, constant(lineno))
            if function.return_type == "void":
                self.append_code_pop()
            self.semantic_stack.append("int")

        elif action == Action.begin_function:
            self.function_table = SymbolTable(0)
            self.function_table.push_empty_stack()
            for param_name, param_type in self.functions[self.current_function].parameters:
                self.function_table.add_symbol(param_name, 1 if param_type == "array" else None, True)

        elif action == Action.end_function:
            self.function_table = None

        elif action == Action.open_block:
            self.function_table.push_empty_stack()

        elif action == Action.close_block:
            self.function_table.pop_stack()

        elif action == Action.declare_int:
            symbol_name = self.semantic_stack.pop().lexeme
            symbol_type = self.semantic_stack.pop().lexeme
            if symbol_type != "int":
                self.error_void_symbol_type(input_lineno, symbol_name)
            if self.function_table is None:
                self.global_table.add_symbol(symbol_name)
            else:
                self.function_table.add_symbol(symbol_name)
                self.append_code_push(None)

        elif action == Action.declare_array:
            symbol_size = int(self.semantic_stack.pop().lexeme)
            symbol_name = self.semantic_stack.pop().lexeme
            symbol_type = self.semantic_stack.pop().lexeme
            if symbol_type != "int":
                pass
            (self.global_table if self.function_table is None else self.function_table).add_symbol(symbol_name,
                                                                                                   symbol_size)
            self.append_code((Code.ADD, direct(SP), constant(symbol_size * 4), direct(SP)))

        elif action == Action.assign:
            rhs_type = self.semantic_stack.pop()
            symbol_name = self.semantic_stack.pop().lexeme
            symbol = self.function_table.get_symbol(symbol_name)
            self.append_code_pop()
            if symbol is not None:
                self.append_code((Code.ADD, direct(FP), constant(symbol.address), direct(TEMP)))
                self.append_code((Code.ASSIGN, indirect(SP), indirect(TEMP)))
            else:
                symbol = self.global_table.get_symbol(symbol_name)
                if symbol is not None:
                    self.append_code((Code.ASSIGN, indirect(SP), direct(symbol.address)))
                else:
                    self.error_symbol_not_defined(input_lineno, symbol_name)
                    self.semantic_stack.append("int")
                    return
            lhs_type = "int" if symbol.size is None else "array"
            if rhs_type != lhs_type:
                self.error_operator_type_mismatch(input_lineno, lhs_type, rhs_type)
            self.append_code_push(None)
            self.semantic_stack.append(rhs_type)

        elif action == Action.push_stack:
            token = self.semantic_stack.pop()
            if token.token_type == TokenType.NUM:
                self.append_code_push(constant(token.lexeme))
                self.semantic_stack.append("int")
            elif token.token_type == TokenType.ID:
                symbol = self.function_table.get_symbol(token.lexeme)
                if symbol is not None:
                    self.append_code((Code.ADD, direct(FP), constant(symbol.address), direct(TEMP)))
                    self.append_code_push(indirect(TEMP) if symbol.size is None or symbol.is_param else direct(TEMP))
                else:
                    symbol = self.global_table.get_symbol(token.lexeme)
                    if symbol is not None:
                        self.append_code_push(direct(symbol.address) if symbol.size is None else constant(symbol.address))
                    else:
                        self.error_symbol_not_defined(input_lineno, token.lexeme)
                        self.semantic_stack.append("int")
                        return
                self.semantic_stack.append("int" if symbol.size is None else "array")

        elif action == Action.pop_stack:
            self.append_code_pop()
            self.semantic_stack.pop()

        elif action == Action.addsubmultrelop:
            snd_type = self.semantic_stack.pop()
            op = self.semantic_stack.pop().lexeme
            idx_type = self.semantic_stack.pop()
            if idx_type != snd_type:
                self.error_operator_type_mismatch(input_lineno, "array", "int")
            self.append_code_pop()
            self.append_code((Code.SUB, direct(SP), constant(4), direct(TEMP)))
            op_code = {"+": Code.ADD, "-": Code.SUB, "*": Code.MULT, "<": Code.LT, "==": Code.EQ}[op]
            self.append_code((op_code, indirect(TEMP), indirect(SP), indirect(TEMP)))
            self.semantic_stack.append("int")

        elif action == Action.negate:
            idx_type = self.semantic_stack.pop()
            if idx_type != "int":
                self.error_operator_type_mismatch(input_lineno, "array", "int")
            self.append_code_pop()
            self.append_code((Code.SUB, constant(0), indirect(SP), indirect(SP)))
            self.append_code_push(None)
            self.semantic_stack.append("int")

        elif action == Action.placeholder_line:
            self.append_code(())

        elif action == Action.push_lineno:
            lineno = len(self.codes)
            self.semantic_stack.append(lineno)

        elif action == Action.jpf_from_skipped1:
            fixlineno = self.semantic_stack.pop()
            lineno = len(self.codes)
            self.codes[fixlineno] = (Code.JPF, indirect(SP), lineno)

        elif action == Action.jpf_from_skipped2:
            fixlineno = self.semantic_stack.pop(-2)
            lineno = len(self.codes)
            self.codes[fixlineno] = (Code.JPF, indirect(SP), lineno)

        elif action == Action.jp_from_skipped1:
            fixlineno = self.semantic_stack.pop()
            lineno = len(self.codes)
            self.codes[fixlineno] = (Code.JP, lineno)

        elif action == Action.jp_from_skipped2:
            fixlineno = self.semantic_stack.pop(-2)
            lineno = len(self.codes)
            self.codes[fixlineno] = (Code.JP, lineno)

        elif action == Action.jp_to_skipped4:
            label = self.semantic_stack.pop(-4)
            self.append_code((Code.JP, label))

        elif action == Action.jp_to_skipped1:
            label = self.semantic_stack.pop()
            self.append_code((Code.JP, label))

        elif action == Action.push_fp_value:
            self.append_code_push(direct(FP))

        elif action == Action.push_array_index_address:
            idx_type = self.semantic_stack.pop()
            if idx_type != "int":
                self.error_operator_type_mismatch(input_lineno, "array", "int")
            token = self.semantic_stack.pop()
            symbol = self.function_table.get_symbol(token.lexeme)
            self.append_code_pop()
            self.append_code((Code.MULT, indirect(SP), constant(4), indirect(SP)))
            if symbol is not None:
                self.append_code((Code.ADD, direct(FP), constant(symbol.address), direct(TEMP)))
                self.append_code((Code.ADD,
                                  (indirect if symbol.is_param else direct)(TEMP), indirect(SP), direct(TEMP)))
                self.append_code_push(direct(TEMP))
            else:
                symbol = self.global_table.get_symbol(token.lexeme)
                self.append_code((Code.ADD, constant(symbol.address), indirect(SP), direct(TEMP)))
                self.append_code_push(direct(TEMP))
            self.semantic_stack.append("int")

        elif action == Action.array_assign:
            rhs_type = self.semantic_stack.pop()
            self.semantic_stack.pop()
            if rhs_type != "int":
                self.error_operator_type_mismatch(input_lineno, "array", "int")
            self.append_code_pop()
            self.append_code_pop()
            self.append_code((Code.ASSIGN, indirect(SP), direct(TEMP)))
            self.append_code_push(None)
            self.append_code((Code.ASSIGN, indirect(SP), indirect(TEMP)))
            self.append_code((Code.ASSIGN, indirect(SP), direct(TEMP)))
            self.append_code_pop()
            self.append_code_push(direct(TEMP))
            self.semantic_stack.append("int")

        elif action == Action.push_address_value:
            self.append_code_pop()
            self.append_code((Code.ASSIGN, indirect(SP), direct(TEMP)))
            self.append_code_push(indirect(TEMP))

        elif action == Action.loop_begin:
            self.loop_blocks.append([])

        elif action == Action.break_statement:
            if not self.loop_blocks:
                self.error_break_outside_loop(input_lineno)
                return
            lineno = len(self.codes)
            self.loop_blocks[-1].append(lineno)
            self.append_code(())

        elif action == Action.loop_end:
            lineno = len(self.codes)
            for break_stat_line in self.loop_blocks[-1]:
                self.codes[break_stat_line] = (Code.JP, lineno)
            self.loop_blocks.pop()

        elif action == Action.push_args_begin:
            self.semantic_stack.append("args_begin")

        elif action == Action.pop_from_semantic:
            self.semantic_stack.pop()

    def error_symbol_not_defined(self, lineno, symbol_name):
        self.semantic_errors.append((lineno, "'%s' is not defined." % symbol_name))

    def error_argn_mismatch(self, lineno, function_name):
        self.semantic_errors.append((lineno, "Mismatch in numbers of arguments of '%s'." % function_name))

    def error_void_symbol_type(self, lineno, symbol_name):
        self.semantic_errors.append((lineno, "Illegal type of void for '%s'." % symbol_name))

    def error_break_outside_loop(self, lineno):
        self.semantic_errors.append((lineno, "No 'for' found for 'break'."))

    def error_parameter_type_mismatch(self, lineno, function_name, argno, got, expected):
        self.semantic_errors.append((lineno,
                                     "Mismatch in type of argument %s of '%s'. Expected '%s' but got '%s' instead."
                                     % (argno + 1, function_name, expected, got)))

    def error_operator_type_mismatch(self, lineno, got, expected):
        self.semantic_errors.append((lineno, "Type mismatch in operands, Got %s instead of %s." % (got, expected)))


def constant(value):
    return f"#{value}"


def direct(value):
    return value


def indirect(value):
    return f"@{value}"


@dataclass
class Variable:
    address: int
    size: int
    is_param: bool


@dataclass
class Function:
    return_type: str
    address: int
    parameters: List[List[str]]


class Action(Enum):
    push_id = auto()
    begin_function = auto()
    end_function = auto()
    open_block = auto()
    close_block = auto()
    declare_int = auto()
    declare_array = auto()
    push_stack = auto()
    pop_stack = auto()
    assign = auto()
    addsubmultrelop = auto()
    negate = auto()
    push_lineno = auto()
    placeholder_line = auto()
    jpf_from_skipped1 = auto()
    jpf_from_skipped2 = auto()
    jp_from_skipped1 = auto()
    jp_from_skipped2 = auto()
    jp_to_skipped1 = auto()
    jp_to_skipped4 = auto()
    register_function = auto()
    add_function_param = auto()
    param_type_to_array = auto()
    call_function = auto()
    call_main = auto()
    push_fp_value = auto()
    return_code_block = auto()
    function_return = auto()
    set_function_return_value = auto()
    push_array_index_address = auto()
    push_address_value = auto()
    array_assign = auto()
    loop_begin = auto()
    loop_end = auto()
    break_statement = auto()
    push_args_begin = auto()
    pop_from_semantic = auto()


class Code(Enum):
    ADD = auto()
    MULT = auto()
    SUB = auto()
    EQ = auto()
    LT = auto()
    ASSIGN = auto()
    JPF = auto()
    JP = auto()
    PRINT = auto()
