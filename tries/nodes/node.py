from abc import abstractmethod

#
# Trie Node Abstraction
# 
class TrieNode:  
    #
    # Default constructor
    #
    @abstractmethod
    def __init__(self, char: str | None, weight: int | None):
        pass
  
    #
    # Named constructor for a root node without character and weight
    # 
    @classmethod
    def root(cls):
        return cls(char=None, weight=None)
      
    #
    # Representation method
    #
    def __repr__(self):
        return f"({self.char}, {self.weight})"
      
    #
    # String method
    #
    @abstractmethod
    def __str__(self):
        pass