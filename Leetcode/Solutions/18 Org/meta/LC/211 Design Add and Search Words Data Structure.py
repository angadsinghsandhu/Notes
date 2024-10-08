# DESIGN ADD AND SEARCH WORDS DATA STRUCTURE

# Problem number: 211
# Difficulty: Medium
# Tags: Trie, Design, Depth-First Search
# Link: https://leetcode.com/problems/design-add-and-search-words-data-structure/

from typing import Dict

class TrieNode:
    def __init__(self):
        # Dictionary to store children nodes
        self.children: Dict[str, TrieNode] = {}
        # Boolean to mark the end of a word
        self.is_end_of_word: bool = False

class WordDictionary:
    """
    This problem requires designing a data structure that supports adding new words 
    and searching for words, which may contain the wildcard character '.' that can 
    match any letter. We will use a Trie (Prefix Tree) data structure to efficiently 
    store words and handle the search operation.

    The addWord method inserts a word into the Trie.
    The search method supports searching for words with '.' as a wildcard.
    """

    def __init__(self):
        # Initialize the root of the Trie
        self.root = TrieNode()

    def addWord(self, word: str) -> None:
        """
        Adds a word to the Trie.
        
        T.C. : O(n), where n is the length of the word
        S.C. : O(n), where n is the length of the word (for new nodes created)
        """
        node = self.root
        for char in word:
            # Create a new TrieNode if the character does not exist
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        # Mark the end of the word
        node.is_end_of_word = True

    def search(self, word: str) -> bool:
        """
        Searches for a word in the Trie, allowing for the '.' wildcard character.
        
        T.C. : O(m), where m is the number of characters in the word, and may involve
               traversing all children nodes in the worst case.
        S.C. : O(m), due to recursion stack space
        """
        def dfs(node: TrieNode, i: int) -> bool:
            if i == len(word):
                # If we've reached the end of the word, check if it's a valid end
                return node.is_end_of_word
            
            char = word[i]
            
            if char == '.':
                # If the character is '.', check all possible child nodes
                for child in node.children.values():
                    if dfs(child, i + 1):
                        return True
                return False
            else:
                # If it's a regular character, proceed only if the character exists in children
                if char not in node.children:
                    return False
                return dfs(node.children[char], i + 1)

        # Start DFS from the root node
        return dfs(self.root, 0)


# Best Method: Using a Trie structure is optimal for both adding words and searching with wildcards.
# Trie supports efficient word insertion and search in O(n) time, where n is the length of the word.

# Sample Usage for Testing
wordDictionary = WordDictionary()
wordDictionary.addWord("bad")
wordDictionary.addWord("dad")
wordDictionary.addWord("mad")
print(wordDictionary.search("pad"))  # Output: False
print(wordDictionary.search("bad"))  # Output: True
print(wordDictionary.search(".ad"))  # Output: True
print(wordDictionary.search("b.."))  # Output: True
