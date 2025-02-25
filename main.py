#
# Program 3: Autocomplete
#
# Course: CS 351, Spring 2025
# System: MacOS using VS Code
# Author: Kaito Sekiya
# 
# File: main.py
#
# Description TODO.
# 
# Usage: main.py [-h] filename
# Example: python main.py tiny.txt
#

from argparse import ArgumentParser, ArgumentTypeError, Namespace
from os import path

WELCOME_MESSAGE = "Autocomplete CLI:"
GOODBYE_MESSAGE = "\nThank you for using Autocomplete CLI! Terminating..."

DATA_PATH = "data"

##################################################################  
#
# Trie Node implementation
# 
class TrieNode:
    ##################################################################  
    #
    # Default constructor
    #
    def __init__(self, char: str | None, weight: int | None):
        self.char = char
        self.weight = weight
        self.children: dict[str, TrieNode] = {}

    ##################################################################  
    #
    # Named constructor for a root node without character and weight
    # 
    @classmethod
    def root(cls):
        return cls(char=None, weight=None)
    
    ##################################################################  
    #
    # Representation method
    #
    def __repr__(self):
        return f"({self.char}, {self.weight})"
    
    ##################################################################  
    #
    # String method
    #
    def __str__(self):
        return f"TrieNode{self.__repr__()}"

##################################################################  
#
# Trie implementation
# 
class Trie:
    ##################################################################  
    #
    # Default constructor
    #
    def __init__(self):
        self.root = TrieNode.root()

    ##################################################################  
    #
    # Named constructor to build a trie from a given list of weights and terms
    # 
    @classmethod
    def from_list(cls, items: list[str]):
        root = cls()

        for weight, term in items:
            root.insert(term, int(weight))

        return root
    
    ##################################################################  
    #
    # Representation method
    #
    def __repr__(self):
        return str(self.unpack())
    
    ##################################################################  
    #
    # String method
    #
    def __str__(self):
        return f"Trie({self.__repr__()})"
    
    ##################################################################  
    #
    # Inserts a given word into the trie with a given weight
    #
    def insert(self, word: str, weight: int) -> None:
        curr_node = self.root

        for char in word:
            if char not in curr_node.children:
                curr_node.children[char] = TrieNode(char, weight=None)

            curr_node = curr_node.children[char]

        curr_node.weight = weight

    ##################################################################  
    #
    # Returns true if a given word exists in the trie, and false otherwise
    #
    def contains(self, word: str) -> bool:
        curr_node = self.root

        for char in word:
            if char not in curr_node.children:
                return False

            curr_node = curr_node.children[char]

        return curr_node.weight != None
    
    ##################################################################  
    #
    # Returns the Trie node of the last character in a given prefix if it exists
    #
    def get_prefix_node(self, prefix: str) -> TrieNode | None: 
        curr_node = self.root

        for char in prefix:
            if char not in curr_node.children:
                return None

            curr_node = curr_node.children[char]

        return curr_node

    ##################################################################  
    #
    # Unpacks the trie as a list of the weight and term pairs
    #
    def unpack(self) -> list[tuple[str, int]]:
        ##################################################################  
        #
        # Recursively unpacks the trie
        #
        def _unpack(root: TrieNode, term: str, items: list[tuple[str, int]]):
            if root.weight != None:
                items.append((term, root.weight))

            for char, node in root.children.items():
                _unpack(node, term + char, items)
        
        items: list[tuple[str, int]] = []

        for char, node in self.root.children.items():
            _unpack(node, char, items)

        return items

##################################################################  
#
# get_args
#
# Parses the command line arguments for the program
#
def get_args() -> Namespace:
    ##################################################################  
    #
    # existing_valid_file
    #
    # Validates that the given file exists and is a file
    #
    def existing_valid_file(arg: str) -> str:
        if not path.isfile(path.join(DATA_PATH, arg)):
            raise ArgumentTypeError(f"{arg} does not exist or is not a file.")
        return arg

    parser = ArgumentParser()
    parser.add_argument("filename", type=existing_valid_file, help="The required filename to build a trie with.")

    return parser.parse_args()

##################################################################  
#
# read_data
#
# Reads the data from the file at a given file path
#
def read_data(file_path: str) -> list[str]:
    with open(file_path, "r") as f_txt:
        f_txt.readline()

        return [
            line.strip().split('\t') for line in f_txt.readlines()
        ]
        
##################################################################  
#
# main
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

    

    print(GOODBYE_MESSAGE)
    

# Just calls main function
if __name__=="__main__":
    main()