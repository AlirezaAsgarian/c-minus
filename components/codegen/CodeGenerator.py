from dataclasses import dataclass
from enum import Enum, auto
from typing import List

from components.scanner.State import TokenType


class SymbolTable:
    def __init__(self, starting_offset):
        self.offset = starting_offset  # can be optimized when popping from stack
        self.table_stack = []

    def add_symbol(self, symbol, size=None):
        self.table_stack[-1][symbol] = Variable(self.offset, size)
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
DATA = 512


class CodeGenerator:

    def __init__(self):
        self.codes = []
        self.global_table = SymbolTable(DATA)
        self.global_table.push_empty_stack()
        self.function_table: SymbolTable = None
        self.semantic_stack = []
        self.append_code((Code.ASSIGN, constant(0), direct(SP)))
        self.append_code((Code.ASSIGN, constant(0), direct(FP)))

    def append_code(self, code):
        self.codes.append(code)

    def append_code_push(self, value):
        if value is not None: self.append_code((Code.ASSIGN, value, indirect(SP)))
        self.append_code((Code.ADD, direct(SP), constant(4), direct(SP)))

    def append_code_pop(self):
        self.append_code((Code.SUB, direct(SP), constant(4), direct(SP)))

    def get_symbol(self, symbol):
        in_function = self.function_table.get_symbol(symbol)
        if in_function is not None: return in_function
        return self.global_table.get_symbol(symbol)

    def codegen(self, action, token):
        if action == Action.push_id:
            self.semantic_stack.append(token)

        elif action == Action.begin_function:
            self.function_table = SymbolTable(0)

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
                pass
            if self.function_table is None:
                self.global_table.add_symbol(symbol_name)
            else:
                self.function_table.add_symbol(symbol_name)
                self.append_code_push(None)

        elif action == Action.declare_array:
            symbol_size = self.semantic_stack.pop().lexeme
            symbol_name = self.semantic_stack.pop().lexeme
            symbol_type = self.semantic_stack.pop().lexeme
            if symbol_type != "int":
                pass
            (self.global_table if self.function_table is None else self.function_table).add_symbol(symbol_name, symbol_size)

        elif action == Action.assign:
            symbol_name = self.semantic_stack.pop().lexeme
            symbol = self.get_symbol(symbol_name)
            self.append_code((Code.ADD, direct(FP), constant(symbol.address), direct(TEMP)))
            self.append_code_pop()
            self.append_code((Code.ASSIGN, indirect(SP), indirect(TEMP)))

        elif action == Action.push_stack:
            token = self.semantic_stack.pop()
            if token.token_type == TokenType.NUM:
                self.append_code_push(constant(token.lexeme))
            elif token.token_type == TokenType.ID:
                symbol = self.function_table.get_symbol(token.lexeme)
                if symbol is not None:
                    self.append_code((Code.ADD, direct(FP), constant(symbol.address), direct(TEMP)))
                    self.append_code_push(indirect(TEMP))
                else:
                    symbol = self.global_table.get_symbol(token.lexeme)
                    self.append_code_push(direct(symbol.address))

        elif action == Action.multiply:
            self.append_code_pop()
            self.append_code((Code.SUB, direct(SP), constant(4), direct(TEMP)))
            self.append_code((Code.MULT, indirect(SP), indirect(TEMP), indirect(TEMP)))
        elif action == Action.addsub:
            op = self.semantic_stack.pop().lexeme
            self.append_code_pop()
            self.append_code((Code.SUB, direct(SP), constant(4), direct(TEMP)))
            self.append_code(((Code.ADD if op == "+" else Code.SUB), indirect(TEMP), indirect(SP), indirect(TEMP)))


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


@dataclass
class Function:
    return_type: str
    address: int
    parameters: List[str]


class Action(Enum):
    push_id = auto()
    begin_function = auto()
    end_function = auto()
    open_block = auto()
    close_block = auto()
    declare_int = auto()
    declare_array = auto()
    push_stack = auto()
    assign = auto()
    multiply = auto()
    addsub = auto()


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
