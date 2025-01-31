# TODO: revisit [IMP]

# File: Leetcode/Solutions/Amazon/146_LRU_Cache.py

"""
Problem Number: 146
Problem Name: LRU Cache
Difficulty: Medium
Tags: Design, Hash Table, Linked List
Company (Frequency): Amazon (103)
Leetcode Link: https://leetcode.com/problems/lru-cache/description/

DESCRIPTION

Design a data structure that follows the constraints of a Least Recently Used (LRU) cache.

Implement the `LRUCache` class:

- `LRUCache(int capacity)` Initializes the LRU cache with a positive size `capacity`.
- `int get(int key)` Returns the value of the key if it exists, otherwise returns -1.
- `void put(int key, int value)` Updates the value of the key if it exists. Otherwise, adds the key-value pair to the cache. If the number of keys exceeds the capacity, the least recently used key is evicted.

Both `get` and `put` must run in \(O(1)\) average time complexity.
"""

from collections import OrderedDict

class LRUCache:
    """
    Approach:
    - Use an OrderedDict to maintain the order of key usage.
    - For `get`, move the accessed key to the end to mark it as recently used.
    - For `put`, update the key-value pair and move it to the end. If the capacity is exceeded, remove the least recently used key (first item in the OrderedDict).

    Time Complexity:
    - `get`: O(1)
    - `put`: O(1)

    Space Complexity: O(capacity)
    """

    def __init__(self, capacity: int):
        self.cache = OrderedDict()
        self.capacity = capacity

    def get(self, key: int) -> int:
        """
        Retrieve the value for the key if it exists, and mark it as recently used.
        """
        if key in self.cache:
            self.cache.move_to_end(key)  # Mark as recently used
            return self.cache[key]
        return -1

    def put(self, key: int, value: int) -> None:
        """
        Insert or update the key-value pair. Evict the least recently used key if capacity is exceeded.
        """
        if key in self.cache:
            self.cache.move_to_end(key)  # Mark as recently used
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)  # Remove least recently used item

# Sample Test Case
if __name__ == "__main__":
    lRUCache = LRUCache(2)
    lRUCache.put(1, 1)  # cache is {1=1}
    lRUCache.put(2, 2)  # cache is {1=1, 2=2}
    print(lRUCache.get(1))  # return 1
    lRUCache.put(3, 3)  # LRU key was 2, evicts key 2, cache is {1=1, 3=3}
    print(lRUCache.get(2))  # returns -1 (not found)
    lRUCache.put(4, 4)  # LRU key was 1, evicts key 1, cache is {4=4, 3=3}
    print(lRUCache.get(1))  # return -1 (not found)
    print(lRUCache.get(3))  # return 3
    print(lRUCache.get(4))  # return 4