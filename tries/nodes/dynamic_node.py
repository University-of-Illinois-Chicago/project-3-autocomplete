from .node import TrieNode

#
# Dynamic List Trie Node Implementation
# 
class DynamicTrieNode(TrieNode):  
    #
    # Default constructor
    #
    def __init__(self, char: str | None, weight: int | None):
        self.char = char
        self.weight = weight
        self.children: list[DynamicTrieNode] = []
      
    #
    # String method
    #
    def __str__(self):
        return f"DynamicTrieNode{self.__repr__()}"