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
from heapq import nlargest
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
        trie = cls()

        for weight, term in items:
            trie.insert(term, int(weight))

        return trie
    
    ##################################################################  
    #
    # Named constructor to build a trie from a given node
    # 
    @classmethod
    def from_node(cls, node: TrieNode):
        trie = cls()
        trie.root = node

        return trie
    
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
    def get_prefix_trie(self, prefix: str) -> "Trie": 
        curr_node = self.root

        for char in prefix:
            if char not in curr_node.children:
                return None

            curr_node = curr_node.children[char]

        return self.from_node(curr_node)

    ##################################################################  
    #
    # Unpacks the trie as a list of the weight and term pairs
    #
    def unpack(self) -> list[tuple[str, int]]:
        ##################################################################  
        #
        # Recursively unpacks the trie
        #
        def _unpack(root: TrieNode, items: list[tuple[str, int]], term: str):
            if root.weight != None:
                items.append((term, root.weight))

            for char, node in root.children.items():
                _unpack(node, items, term + char)
        
        items: list[tuple[str, int]] = []
        term = self.root.char or ""

        for char, node in self.root.children.items():
            _unpack(node, items, term + char)

        return items
    
    ##################################################################  
    #
    # get_profile
    #
    # Returns a top k matches from the trie for the given prefix
    #
    def get_top_k_matches(self, prefix: str, k: int) -> list[tuple[str, int]]:
        return nlargest(
            k, 
            self.get_prefix_trie(prefix).unpack(), 
            key=lambda item: item[1]
        )

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
    
    ##################################################################  
    #
    # positive_int
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