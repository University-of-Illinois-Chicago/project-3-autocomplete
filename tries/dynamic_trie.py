from .trie import Trie
from .nodes.dynamic_node import DynamicTrieNode
  
#
# Dynamic Trie Implementation
# 
class DynamicTrie(Trie):  
    #
    # Default constructor
    #
    def __init__(self):
        self.root = DynamicTrieNode.root()
      
    #
    # Inserts a given word into the trie with a given weight
    #
    def insert(self, word: str, weight: int) -> None:
        curr_node = self.root

        for char in word:
            child = next((child for child in curr_node.children if child.char == char), None)

            if child == None:
                child = DynamicTrieNode(char, None)
                curr_node.children.append(child) 

            curr_node = child

        curr_node.weight = weight

    #
    # Returns true if a given word exists in the trie, and false otherwise
    #
    def contains(self, word: str) -> bool:
        curr_node = self.root

        for char in word:
            curr_node = next((child for child in curr_node.children if child.char == char), None)

            if curr_node == None:
                return False
            
        return curr_node.weight != None
    
    #
    # Returns the trie node of the last character in a given prefix if it exists
    #
    def get_prefix_node(self, prefix: str) -> DynamicTrieNode: 
        curr_node = self.root

        for char in prefix:
            curr_node = next((child for child in curr_node.children if child.char == char), None)

            if curr_node == None:
                return None 

        return curr_node

    #
    # Unpacks the trie as a list of the weight and term pairs
    #
    def unpack(self) -> list[tuple[str, int]]:
        #
        # Recursively (DFS) unpacks the trie
        #
        def dfs(root: DynamicTrieNode, items: list[tuple[str, int]], prefix: str):
            if root.weight is not None:
                items.append((prefix, root.weight))

            for child in root.children:
                dfs(child, items, prefix + child.char)

        items: list[tuple[str, int]] = []

        if self.root != None:
            dfs(self.root, items, "")
        
        return items