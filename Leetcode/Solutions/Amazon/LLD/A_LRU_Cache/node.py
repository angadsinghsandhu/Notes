# ================================================================
# File: lrucache/node.py
# Description:
#   The Node class represents a node in the doubly linked list used by the LRUCache.
#   - It contains the key, value, and pointers to the previous and next nodes.
#
# Steps Covered:
# 2. Identify Key Entities.
# 3. Define Classes and Their Attributes.
# ================================================================

class Node:
    def __init__(self, key, value):
        self.key = key        # Key for the cache entry.
        self.value = value    # Value for the cache entry.
        self.prev = None      # Pointer to the previous node in the list.
        self.next = None      # Pointer to the next node in the list.