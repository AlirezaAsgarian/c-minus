# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from components.ScannerDfa import ScannerDfa
from components.State import State, Pattern


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    dict = {"j": {
        "q" : 44,
        "c" : 33
    },
    "k" : {
        "f": 44
    }}
    print(ScannerDfa.get_next_state(ScannerDfa.get_next_state(State.INITIAL_STATE, '/'), '*'))
    print_hi('PyCharm')
    print(State.FINAL_ID_STATE.tokenType)
    import re

    # Define a Regex pattern to match the character 'a'
    pattern = Pattern.NOT_EOF

    # Text to search for a match
    text = chr(3)

    # Use re.findall() to find all occurrences of the pattern in the text
    matches = re.findall(pattern, text)

    if matches:
        print(f"Found the character '{pattern}' in the text.")
    else:
        print(f"Did not find the character '{pattern}' in the text.")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
