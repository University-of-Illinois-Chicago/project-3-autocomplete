from .trie import Trie
from .nodes.static_node import StaticTrieNode
  
#
# Static Trie Implementation
# 
class StaticTrie(Trie):  
    #
    # Default constructor
    #
    def __init__(self):
        self.root = StaticTrieNode.root()
      
    #
    # Inserts a given word into the trie with a given weight
    #
    def insert(self, word: str, weight: int) -> None:
        curr_node = self.root

        for char in word:
            index = ord(char)

            if curr_node.children[index] == None:
                curr_node.children[index] = StaticTrieNode(char, None)

            curr_node = curr_node.children[index]

        curr_node.weight = weight

    #
    # Returns true if a given word exists in the trie, and false otherwise
    #
    def contains(self, word: str) -> bool:
        curr_node = self.root

        for char in word:
            index = ord(char)

            if curr_node.children[index] == None:
                return False
            
            curr_node = curr_node.children[index]

        return curr_node.weight != None
    
    #
    # Returns the trie node of the last character in a given prefix if it exists
    #
    def get_prefix_node(self, prefix: str) -> StaticTrieNode: 
        curr_node = self.root

        for char in prefix:
            index = ord(char)

            if curr_node.children[index] == None:
                return None 
            
            curr_node = curr_node.children[index]
        
        return curr_node

    #
    # Unpacks the trie as a list of the weight and term pairs
    #
    def unpack(self) -> list[tuple[str, int]]:
        #
        # Recursively (DFS) unpacks the trie
        #
        def dfs(root: StaticTrieNode, items: list[tuple[str, int]], prefix: str):
            if root.weight != None:
                items.append((prefix, root.weight))
            
            for i, child in enumerate(root.children):
                if child != None:
                    dfs(child, items, prefix + chr(i))

        items: list[tuple[str, int]] = []

        dfs(self.root, items, "")
        return items