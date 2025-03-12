import heapq
from abc import abstractmethod

from .nodes.node import TrieNode

#
# Trie Abstraction
# 
class Trie:  
    #
    # Default constructor
    #
    @abstractmethod
    def __init__(self):
        pass
  
    #
    # Named constructor to build a trie from a given list of weights and terms
    # 
    @classmethod
    def from_list(cls, items: list[str]):
        trie = cls()

        for weight, term in items:
            trie.insert(term, int(weight))

        return trie
      
    #
    # Named constructor to build a trie from a given node
    # 
    @classmethod
    def from_node(cls, node: TrieNode):
        trie = cls()
        trie.root = node

        return trie
      
    #
    # Representation method
    #
    def __repr__(self):
        return str(self.unpack())
    
    #
    # String method
    #
    def __str__(self):
        return f"Trie({self.__repr__()})"
      
    #
    # Inserts a given word into the trie with a given weight
    #
    @abstractmethod
    def insert(self, word: str, weight: int) -> None:
        pass

    #
    # Returns true if a given word exists in the trie, and false otherwise
    #
    @abstractmethod
    def contains(self, word: str) -> bool:
        pass
    
    #
    # Returns the Trie node of the last character in a given prefix if it exists
    #
    @abstractmethod
    def get_prefix_node(self, prefix: str) -> TrieNode: 
        pass

    #
    # Unpacks the trie as a list of the weight and term pairs
    #
    @abstractmethod
    def unpack(self) -> list[tuple[str, int]]:
        pass
    
    #
    # Returns a top k matches from the trie for the given prefix
    #
    def get_top_k_matches(self, prefix: str, k: int) -> list[tuple[str, int]]:
        #
        # Using heapq.nlargest
        # O(n + k*log n)
        #
        top_k_matches = heapq.nlargest(
            k, 
            self.from_node(self.get_prefix_node(prefix)).unpack(), 
            key=lambda item: -item[1]
        )

        #
        # Using heapq.heapify and heapq.heappop
        # O(n + k*log n) 
        # 
        pq = [
            (-weight, char) for char, weight in self.from_node(self.get_prefix_node(prefix)).unpack()
        ] 
        heapq.heapify(pq) 

        top_k_matches = [
            (char, -weight) for weight, char in [heapq.heappop(pq) for _ in range(k)]
        ]

        #
        # Using sorted
        # O(n*log n)
        # 
        top_k_matches = sorted(
            self.from_node(self.get_prefix_node(prefix)).unpack(),
            key=lambda item: item[1],
            reverse=True
        )[:k]
    
        return top_k_matches