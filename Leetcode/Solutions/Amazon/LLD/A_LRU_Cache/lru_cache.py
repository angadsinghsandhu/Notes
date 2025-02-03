# ================================================================
# File: lrucache/lru_cache.py
# Description:
#   The LRUCache class implements the LRU cache functionality.
#   - It uses a hash map for O(1) lookup and a doubly linked list for maintaining access order.
#   - The class supports get and put operations, moving accessed items to the head.
#   - When the cache exceeds its capacity, it removes the least recently used item (from the tail).
#   - Thread-safety can be ensured by adding synchronization mechanisms if required.
#
# Steps Covered:
# 1. Clarify Requirements and Identify Core Use Cases.
# 2. Identify Key Entities.
# 3. Define Classes and Their Attributes.
# 4. Determine Core Methods Based on Use Cases.
# 7. Exception Handling and Edge Cases.
# 9. Apply Design Patterns and SOLID principles.
# ================================================================

from node import Node

class LRUCache:
    def __init__(self, capacity):
        # Step 3: Initialize the capacity and cache data structure.
        self.capacity = capacity
        self.cache = {}  # Hash map to store key -> Node mappings.
        
        # Create dummy head and tail nodes for the doubly linked list.
        self.head = Node(None, None)
        self.tail = Node(None, None)
        self.head.next = self.tail
        self.tail.prev = self.head

    def get(self, key):
        # Step 4: Get operation - if key exists, move it to the head and return its value.
        if key in self.cache:
            node = self.cache[key]
            self._move_to_head(node)
            return node.value
        return None  # If the key doesn't exist, return None (could be -1 as per requirement).

    def put(self, key, value):
        # Step 4: Put operation - update or insert the key-value pair.
        if key in self.cache:
            node = self.cache[key]
            node.value = value  # Update the value.
            self._move_to_head(node)
        else:
            node = Node(key, value)
            self.cache[key] = node
            self._add_to_head(node)
            if len(self.cache) > self.capacity:
                # Cache is over capacity; remove the least recently used item.
                removed_node = self._remove_tail()
                del self.cache[removed_node.key]

    def _add_to_head(self, node):
        # Helper method to add a node right after the dummy head.
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node

    def _remove_node(self, node):
        # Helper method to remove a node from the linked list.
        node.prev.next = node.next
        node.next.prev = node.prev

    def _move_to_head(self, node):
        # Helper method to move a node to the head of the linked list.
        self._remove_node(node)
        self._add_to_head(node)

    def _remove_tail(self):
        # Helper method to remove the node before the dummy tail (least recently used).
        node = self.tail.prev
        self._remove_node(node)
        return node