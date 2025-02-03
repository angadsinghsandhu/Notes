# ================================================================
# File: lrucache/lru_cache_demo.py
# Description:
#   The LRUCacheDemo class demonstrates the usage of the LRUCache.
#   - It creates an instance of LRUCache with a capacity of 3.
#   - It performs various put and get operations and prints the outcomes.
#
# Steps Covered:
# 1. Clarify Requirements and Identify Core Use Cases.
# 6. Implement Necessary Methods.
# 8. Follow Good Coding Practices.
# ================================================================

from lru_cache import LRUCache

class LRUCacheDemo:
    @staticmethod
    def run():
        cache = LRUCache(3)

        # Step 6: Populate the cache with key-value pairs.
        cache.put(1, "Value 1")
        cache.put(2, "Value 2")
        cache.put(3, "Value 3")

        # Access keys to demonstrate cache behavior.
        print(cache.get(1))  # Output: "Value 1" (and moves key 1 to the head)
        print(cache.get(2))  # Output: "Value 2" (and moves key 2 to the head)

        # Inserting a new key should evict the least recently used (which is key 3).
        cache.put(4, "Value 4")

        print(cache.get(3))  # Output: None (key 3 has been evicted)
        print(cache.get(4))  # Output: "Value 4"

        # Update an existing key.
        cache.put(2, "Updated Value 2")
        print(cache.get(1))  # Output: "Value 1"
        print(cache.get(2))  # Output: "Updated Value 2"

if __name__ == "__main__":
    LRUCacheDemo.run()