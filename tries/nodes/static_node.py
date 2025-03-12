from .node import TrieNode

#
# Static List Trie Node Implementation
# 
class StaticTrieNode(TrieNode):  
    #
    # Default constructor
    #
    def __init__(self, char: str | None, weight: int | None):
        self.char = char
        self.weight = weight
        self.children: list[StaticTrieNode] = [None] * 128
      
    #
    # String method
    #
    def __str__(self):
        return f"StaticTrieNode{self.__repr__()}"