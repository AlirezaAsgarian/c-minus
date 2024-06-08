from dataclasses import dataclass
from enum import Enum, auto
from typing import List

from components.scanner.State import TokenType


class SymbolTable:
    def __init__(self):
        self.size = 0
        self.table = {}

    def add_symbol(self, symbol, size=None):
        self.table[symbol] = Variable(self.size, size)
        self.size += 4 if size is None else 4 * size

    def get_symbol(self, symbol):
        return self.table[symbol]

    def has_symbol(self, symbol):
        return symbol in self.table


SP = 500
FP = 504


class CodeGenerator:

    def __init__(self):
        self.codes = []
        self.table_stack = [SymbolTable()]
        self.function_table = {}
        self.semantic_stack = []
        self.append_code((Code.ASSIGN, constant(0), direct(SP)))

    def add_symbol(self, symbol, size=None):
        self.table_stack[-1].add_symbol(symbol, size)

    def get_symbol(self, symbol):
        for table in self.table_stack[::-1]:
            if table.has_symbol(symbol):
                return table.get_symbol(symbol)

    def append_code(self, code):
        self.codes.append(code)

    def append_code_push(self, value):
        self.append_code((Code.ASSIGN, constant(value), indirect(SP)))
        self.append_code((Code.ADD, direct(SP), constant(4), direct(SP)))

    def codegen(self, action, token):
        if action == Action.push_id:
            self.semantic_stack.append(token.lexeme)

        elif action == Action.open_block:
            self.table_stack.append(SymbolTable())

        elif action == Action.close_block:
            self.table_stack.pop()

        elif action == Action.declare_int:
            symbol_name = self.semantic_stack.pop()
            symbol_type = self.semantic_stack.pop()
            if symbol_type != "int":
                pass
            self.add_symbol(symbol_name)
            print([x.table for x in self.table_stack])

        elif action == Action.declare_array:
            symbol_size = self.semantic_stack.pop()
            symbol_name = self.semantic_stack.pop()
            symbol_type = self.semantic_stack.pop()
            if symbol_type != "int":
                pass
            self.add_symbol(symbol_name, symbol_size)

        elif action == Action.assign:
            value = self.semantic_stack.pop()
            symbol_name = self.semantic_stack.pop()
            symbol = self.get_symbol(symbol_name)
            print(symbol, value)

        elif action == Action.push_stack:
            if token.token_type == TokenType.NUM:
                self.append_code_push(token.lexeme)


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
    open_block = auto()
    close_block = auto()
    declare_int = auto()
    declare_array = auto()
    assign = auto()
    push_stack = auto()


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
