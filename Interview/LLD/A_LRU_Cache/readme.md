# LRU Cache

# Designing a LRU Cache

## Requirements
1. The LRU cache should support the following operations:
- put(key, value): Insert a key-value pair into the cache. If the cache is at capacity, remove the least recently used item before inserting the new item.
- get(key): Get the value associated with the given key. If the key exists in the cache, move it to the front of the cache (most recently used) and return its value. If the key does not exist, return -1.
2. The cache should have a fixed capacity, specified during initialization.
3. The cache should be thread-safe, allowing concurrent access from multiple threads.
4. The cache should be efficient in terms of time complexity for both put and get operations, ideally O(1).

## Classes, Interfaces and Enumerations
1. The **Node** class represents a node in the doubly linked list, containing the key, value, and references to the previous and next nodes.
2. The **LRUCache** class implements the LRU cache functionality using a combination of a hash map (cache) and a doubly linked list (head and tail).
3. The get method retrieves the value associated with a given key. If the key exists in the cache, it is moved to the head of the linked list (most recently used) and its value is returned. If the key does not exist, null is returned.
4. The put method inserts a key-value pair into the cache. If the key already exists, its value is updated, and the node is moved to the head of the linked list. If the key does not exist and the cache is at capacity, the least recently used item (at the tail of the linked list) is removed, and the new item is inserted at the head.
5. The addToHead, removeNode, moveToHead, and removeTail methods are helper methods to manipulate the doubly linked list.
6. The synchronized keyword is used on the get and put methods to ensure thread safety, allowing concurrent access from multiple threads.
7. The **LRUCacheDemo** class demonstrates the usage of the LRU cache by creating an instance of LRUCache with a capacity of 3, performing various put and get operations, and printing the results.

## **Key Design Considerations and SOLID Principles:**  
> - **Single Responsibility:**  
>   Each class has a single responsibility. For example, `Node` is solely responsible for storing key-value pairs along with its pointers, and `LRUCache` handles the cache functionality.  
> - **Open/Closed:**  
>   The design is open for extension (if, for example, a different eviction strategy is needed) but closed for modification.  
> - **Liskov Substitution:**  
>   The helper methods in `LRUCache` can be replaced or extended if needed, without affecting the public contract of `get` and `put`.  
> - **Interface Segregation:**  
>   The `LRUCache` class exposes only the necessary public methods (`get`, `put`) while internal operations are encapsulated.  
> - **Dependency Inversion:**  
>   The high-level cache operations depend on abstractions (the node structure and helper methods) rather than on concrete implementations.

## Directory Structure

```
lrucache/
├── lru_cache.py
├── lru_cache_demo.py
└── node.py
```

## Summary of the Design Steps and SOLID Application

1. **Clarify Requirements and Identify Core Use Cases:**
   - The cache must support O(1) `get` and `put` operations.
   - It evicts the least recently used item when capacity is exceeded.
   - It must be thread-safe (in a production system, synchronization would be added).

2. **Identify Key Entities:**
   - **Node:** Represents an element in the doubly linked list with key, value, and pointers.
   - **LRUCache:** Implements the cache logic using a hash map and a doubly linked list.

3. **Define Classes and Their Attributes:**
   - `Node` stores the key, value, and links to neighboring nodes.
   - `LRUCache` stores the cache capacity, a dictionary for key lookup, and dummy head/tail nodes for list management.

4. **Determine Core Methods Based on Use Cases:**
   - Public methods: `get(key)` and `put(key, value)`.
   - Private helper methods: `_add_to_head`, `_remove_node`, `_move_to_head`, and `_remove_tail`.

5. **Define Relationships Between Classes:**
   - **Composition:** `LRUCache` uses `Node` objects to form a doubly linked list.
   - **Aggregation:** The cache holds nodes in a dictionary for fast access.

6. **Implement Necessary Methods:**
   - `get` and `put` operations are implemented to provide O(1) access.
   - Helper methods manage the doubly linked list to maintain order of use.

7. **Exception Handling and Edge Cases:**
   - The implementation checks for key existence and handles over-capacity scenarios.
   - In a fully concurrent environment, synchronization (e.g., threading locks) would be added to `get` and `put`.

8. **Follow Good Coding Practices:**
   - Meaningful method names and separation of concerns are maintained.
   - The design is modular and easy to extend or modify.

9. **Apply Design Patterns and SOLID Principles:**
   - **Single Responsibility:** Each class and method has a distinct responsibility.
   - **Open/Closed:** The design is ready to be extended with additional features (e.g., enhanced thread safety) without modifying existing code.
   - **Liskov Substitution & Interface Segregation:** Public operations expose only what is necessary for the cache functionality.
   - **Dependency Inversion:** High-level cache methods depend on abstract operations defined by the helper methods.