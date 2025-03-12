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
# Usage: main.py [-h] filename
# Example: python main.py tiny.txt
#

from argparse import ArgumentParser, ArgumentTypeError, Namespace
from os import path

from tries.hash_trie import HashTrie as Trie
# from tries.dynamic_trie import DynamicTrie as Trie
# from tries.static_trie import StaticTrie as Trie

WELCOME_MESSAGE = "Autocomplete CLI:"
GOODBYE_MESSAGE = "\nThank you for using Autocomplete CLI! Terminating..."

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
    parser.add_argument("filename", type=existing_valid_file, help="The required filename to build a trie with.")
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
# The controlling unit of the program. It prints majority of the text 
# and calls the helper functions for the Autocomplete algorithm functionality.
#
def main() -> None:
    args = get_args()

    print(WELCOME_MESSAGE)

    trie = Trie.from_list(
        read_data(path.join(DATA_PATH, args.filename))
    )

    while True:
        prefix = input("\nEnter a prefix (or # to quit): ")
        
        if prefix == "#":
            break

        matches = trie.get_top_k_matches(prefix, args.k)

        print(f">> {prefix}")
        for suffix, weight in matches:
            print(f"\t{prefix}{suffix}, {weight}")

    print(GOODBYE_MESSAGE)
    

# Just calls main function
if __name__=="__main__":
    main()