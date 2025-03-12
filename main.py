#
# Program 3: Autocomplete
#
# Course: CS 351, Spring 2025
# System: MacOS using VS Code
# Author: Kaito Sekiya
# 
# File: main.py
#
# This is the autocomplete program implemented as a CLI program.
#
# Usage: main.py [-h] [--k K] [--f filename]
# Example: python main.py
#          python main.py -k 10
#          python main.py -k 2 -f tiny.txt
# 
# Defailt: python main.py -k 5 -f wiktionary.txt

import curses
from argparse import ArgumentParser, ArgumentTypeError, Namespace
from time import sleep
from os import path

from tries.hash_trie import HashTrie as Trie
# from tries.dynamic_trie import DynamicTrie as Trie
# from tries.static_trie import StaticTrie as Trie

WELCOME_MESSAGE = "Welcome to Autocomplete CLUI! Starting..."
HEADER_MESSAGE = "Autocomplete CLUI:"
ENTER_MESSAGE = "Enter text (or $ to quit): "
GOODBYE_MESSAGE = "Thank you for using Autocomplete CLUI! Terminating..."

DATA_PATH = "data"
  
#
# Parses the command line arguments for the program
#
def get_args() -> Namespace:
    #
    # Validates that the given file exists and is a file
    #
    def existing_valid_file(arg: str) -> str:
        if not path.isfile(path.join(DATA_PATH, arg)):
            raise ArgumentTypeError(f"{arg} does not exist or is not a file.")
        return arg
    
    #
    # Validates that the given value is a positive integer
    #
    def positive_int(arg: str) -> int:
        try:
            value = int(arg) 
        except ValueError:
            raise ArgumentTypeError(f"{arg} is not an integer")
        
        if value <= 0:
            raise ArgumentTypeError(f"{value} is not a positive integer")
        return value

    parser = ArgumentParser()
    parser.add_argument("--f", type=existing_valid_file, default="wiktionary.txt", help="The required filename to build a trie with.")
    parser.add_argument("--k", type=positive_int, default=5, help="An optional integer parameter to select the top k matches.")

    return parser.parse_args()

#
# Reads the data from the file at a given file path
#
def read_data(file_path: str) -> list[str]:
    with open(file_path, "r") as f_txt:
        f_txt.readline()

        return [
            line.strip().split('\t') for line in f_txt.readlines()
        ]

#
# Handles the interactive command line autocomplete functionality.
# It dynamically displays and updates suggested words based on user input.
# Allows navigation using arrow keys and autocompletion with the TAB key.
#
def autocomplete(stdscr: curses.window, args: Namespace, trie: Trie) -> None:
    # Make cursor invisible
    curses.curs_set(0)
    
    text = ""
    selected_word = 0
    
    while True:
        # Clear CLUI from prior contetn
        stdscr.clear()
        # Write the welcome message on the 1st line and then the input line on the 2nd line
        stdscr.addstr(0, 0, HEADER_MESSAGE)
        stdscr.addstr(2, 0, ENTER_MESSAGE + text)

        # Get the last word (or prefix) from the text
        prefix = text.split(" ")[-1]
        # Get the top k matches
        matches = trie.get_top_k_matches(prefix, args.k)
        
        # Print the top matches
        for i, (suffix, weight) in enumerate(matches):
            if i == selected_word:
                # Add '>' and reverse the color for the selected one
                stdscr.addstr(i + 3, 0, f"> {prefix}{suffix}, {weight}", curses.A_REVERSE)
            else:
                # Otherwise, nothing fancy
                stdscr.addstr(i + 3, 0, f"  {prefix}{suffix}, {weight}")
        
        # Update the CLUI
        stdscr.refresh()
        # Get the last character
        key = stdscr.getch()
        
        if key == ord("$"):
            # Exit the autocomplete CLUI
            break
        elif key == curses.KEY_BACKSPACE or key == 127:
            # Delete the last character
            text = text[:-1]
            selected_word = 0
        elif key == curses.KEY_UP:
            # Select the word above
            selected_word = (selected_word - 1) % len(matches[:5])
        elif key == curses.KEY_DOWN:
            # Select the word below
            selected_word = (selected_word + 1) % len(matches[:5])
        elif key == 9: 
            # Autocomplete the word if TAB is pressed and matches exist
            if matches:
                text = text + matches[selected_word][0] + " "
                selected_word = 0
        elif 32 <= key < 127:
            # Append the text with ASCII characters from 32 to 126 only
            text += chr(key)
            selected_word = 0

#
# The controlling unit of the program. 
# It initializes the Trie with words from the specified file.
# Then, it starts an interactive autocomplete Command Line User Interface (CLUI).
#
def main() -> None:
    args = get_args()

    trie = Trie.from_list(
        read_data(path.join(DATA_PATH, args.f))
    )

    print(WELCOME_MESSAGE)
    sleep(2)

    curses.wrapper(autocomplete, args, trie)

    print(GOODBYE_MESSAGE)
    sleep(2)
    
# Just calls main function
if __name__=="__main__":
    main()