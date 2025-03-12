from .node import TrieNode

#
# Hashmap Trie Node Implementation
# 
class HashTrieNode(TrieNode):  
    #
    # Default constructor
    #
    def __init__(self, char: str | None, weight: int | None):
        self.char = char
        self.weight = weight
        self.children: dict[str, HashTrieNode] = {}
      
    #
    # String method
    #
    def __str__(self):
        return f"HashTrieNode{self.__repr__()}"