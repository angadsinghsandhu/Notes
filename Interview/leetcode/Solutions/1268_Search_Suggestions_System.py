# TODO: revisit

# File: Leetcode/Solutions/1268_Search_Suggestions_System.py

"""
Problem Number: 1268
Problem Name: Search Suggestions System
Difficulty: Medium
Tags: Array, String, Trie
Company (Frequency): Amazon (15), Google (10), Microsoft (8)
Leetcode Link: https://leetcode.com/problems/search-suggestions-system/description/

DESCRIPTION

You are given an array of strings `products` and a string `searchWord`.

Design a system that suggests at most three product names from `products` after each character of `searchWord` is typed. Suggested products should have a common prefix with `searchWord`. If there are more than three products with a common prefix, return the three lexicographically minimum products.

Return a list of lists of the suggested products after each character of `searchWord` is typed.

---

#### Example 1:
**Input:**
```plaintext
products = ["mobile","mouse","moneypot","monitor","mousepad"], searchWord = "mouse"
```

**Output:**
```plaintext
[
    ["mobile","moneypot","monitor"],
    ["mobile","moneypot","monitor"],
    ["mouse","mousepad"],
    ["mouse","mousepad"],
    ["mouse","mousepad"]
]
```

**Explanation:**  
- After typing `m` and `mo`, all products match, and the system suggests `["mobile","moneypot","monitor"]`.
- After typing `mou`, `mous`, and `mouse`, the system suggests `["mouse","mousepad"]`.

#### Constraints:
- `1 <= products.length <= 1000`
- `1 <= products[i].length <= 3000`
- `1 <= sum(products[i].length) <= 2 * 10^4`
- All the strings of `products` are unique.
- `products[i]` consists of lowercase English letters.
- `1 <= searchWord.length <= 1000`
- `searchWord` consists of lowercase English letters.
"""

from typing import List

class Solution:
    """
    Thought Process:
    - The problem involves suggesting products based on the prefix of the search word.
    - A brute-force approach involves filtering the products list for each prefix and sorting the results.
    - An optimized approach uses sorting and binary search to efficiently find the suggested products.

    Input:
        products: List[str] - A list of product names.
        searchWord: str - The search word being typed.

    Output:
        List[List[str]] - A list of suggested products after each character of `searchWord` is typed.
    """

    def brute_force_solution(self, products: List[str], searchWord: str) -> List[List[str]]:
        """
        Approach:
        - For each prefix of `searchWord`, filter the `products` list to find products that start with the prefix.
        - Sort the filtered list and return the top 3 results.

        T.C.: O(n * m * log n) - Filtering and sorting for each prefix.
        S.C.: O(n) - Storing the filtered results.
        """
        suggestions = []
        for i in range(1, len(searchWord) + 1):
            prefix = searchWord[:i]
            filtered = [product for product in products if product.startswith(prefix)]
            filtered.sort()
            suggestions.append(filtered[:3])
        return suggestions

    def optimized_solution(self, products: List[str], searchWord: str) -> List[List[str]]:
        """
        Approach:
        - Sort the `products` list lexicographically.
        - Use binary search to efficiently find the range of products that match the current prefix.
        - Return the top 3 products in that range.

        T.C.: O(n log n + m log n) - Sorting and binary search for each prefix.
        S.C.: O(n + m) - Storing the sorted products. where n is the number of products and m is the length of the search word.
        """
        products.sort()
        suggestions = []
        prefix = ""
        for ch in searchWord:
            prefix += ch
            # Find the starting index of the prefix using binary search
            left, right = 0, len(products)
            while left < right:
                mid = (left + right) // 2
                if products[mid] < prefix:
                    left = mid + 1
                else:
                    right = mid
            # Collect up to 3 products that match the prefix
            current_suggestions = []
            for i in range(left, min(left + 3, len(products))):
                if products[i].startswith(prefix):
                    current_suggestions.append(products[i])
            suggestions.append(current_suggestions)
        return suggestions

# Run and print sample test cases
if __name__ == "__main__":
    solution = Solution()

    # Test case 1
    products1 = ["mobile", "mouse", "moneypot", "monitor", "mousepad"]
    searchWord1 = "mouse"
    print(solution.brute_force_solution(products1, searchWord1))  # Output: [["mobile","moneypot","monitor"],["mobile","moneypot","monitor"],["mouse","mousepad"],["mouse","mousepad"],["mouse","mousepad"]]
    print(solution.optimized_solution(products1, searchWord1))    # Output: [["mobile","moneypot","monitor"],["mobile","moneypot","monitor"],["mouse","mousepad"],["mouse","mousepad"],["mouse","mousepad"]]

    # Test case 2
    products2 = ["havana"]
    searchWord2 = "havana"
    print(solution.brute_force_solution(products2, searchWord2))  # Output: [["havana"],["havana"],["havana"],["havana"],["havana"],["havana"]]
    print(solution.optimized_solution(products2, searchWord2))    # Output: [["havana"],["havana"],["havana"],["havana"],["havana"],["havana"]]

    # Test case 2
    products3 = ["mobile", "house", "list", "mouseball", "mousepad", "happyness", "tokens", "blasted"]
    searchWord3 = "mouse"
    print(solution.optimized_solution(products3, searchWord3))