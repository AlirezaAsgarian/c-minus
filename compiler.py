# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from components.Scanner import Scanner
from components.ScannerDfa import ScannerDfa
from components.State import State, Pattern, TokenType
import re


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    filePath = "/home/alireza/PycharmProjects/c-minus/samples_p1/T01/input.txt"
    scanner = Scanner(filePath)
    for i in range(0, 1000) :
        token = scanner.get_next_token()
        if (token.token_type != TokenType.WHITESPACE):
            print(i)
            print(token.token_type,end="")
            print(token.lexim)
        if token == "$":
            break

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
