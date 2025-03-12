from .trie import Trie
from .nodes.hash_node import HashTrieNode
  
#
# Hashmap Trie Implementation
# 
class HashTrie(Trie):  
    #
    # Default constructor
    #
    def __init__(self):
        self.root = HashTrieNode.root()
      
    #
    # Inserts a given word into the trie with a given weight
    #
    def insert(self, word: str, weight: int) -> None:
        curr_node = self.root

        for char in word:
            if char not in curr_node.children:
                curr_node.children[char] = HashTrieNode(char, None)

            curr_node = curr_node.children[char]

        curr_node.weight = weight

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
    
    #
    # Returns the trie node of the last character in a given prefix if it exists
    #
    def get_prefix_node(self, prefix: str) -> HashTrieNode: 
        curr_node = self.root

        for char in prefix:
            if char not in curr_node.children:
                return None

            curr_node = curr_node.children[char]

        return curr_node

    #
    # Unpacks the trie as a list of the weight and term pairs
    #
    def unpack(self) -> list[tuple[str, int]]:
        #
        # Recursively (DFS) unpacks the trie
        #
        def dfs(root: HashTrieNode, items: list[tuple[str, int]], prefix: str):
            if root.weight != None:
                items.append((prefix, root.weight))

            for char, child in root.children.items():
                dfs(child, items, prefix + char)
        
        items: list[tuple[str, int]] = []

        dfs(self.root, items, "")
        return items