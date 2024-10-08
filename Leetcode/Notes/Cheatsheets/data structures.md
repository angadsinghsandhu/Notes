# Guide to Essential Data Structures in Python for Competitive Programming

Below is an extended guide that includes explanations of when to use each structure, key patterns that indicate their use, and the types of LeetCode problems where they are often employed.

1. Arrays (Lists in Python)

	•	Description: Arrays are fixed-size structures where elements are stored in contiguous memory. They provide O(1) access to elements by index but have O(n) complexity for insertion and deletion in the middle of the array.
	•	When to Use: Use arrays when you need random access to elements or need to store a static list of items.
	•	Key Patterns:
	•	Static data, requiring random access.
	•	Problems with prefix sums, sliding windows.
	•	LeetCode Problem Types:
	•	Sliding Window Maximum (Problem #239)
	•	Two Sum (Problem #1)

Python Implementation:

arr = [1, 2, 3]
arr.append(4)  # Append
arr.pop()      # Pop
arr[1]         # Access element

Time Complexity:

	•	Access: O(1)
	•	Insert/Delete: O(n)

2. Stacks (Using list or deque)

	•	Description: A stack follows the Last In, First Out (LIFO) principle. It is useful for maintaining the state of operations.
	•	When to Use: Use when you need to handle matching pairs (e.g., parentheses), backtracking, or reversing order.
	•	Key Patterns:
	•	Parentheses matching.
	•	Reversing sequences.
	•	Backtracking.
	•	LeetCode Problem Types:
	•	Valid Parentheses (Problem #20)
	•	Daily Temperatures (Problem #739)

Python Implementation:

stack = []
stack.append(1)  # Push
stack.pop()      # Pop

Time Complexity:

	•	Push/Pop: O(1)

3. Queues (Using collections.deque)

	•	Description: A queue follows the First In, First Out (FIFO) principle. It is used when processing elements in the order they arrive.
	•	When to Use: Ideal for problems involving breadth-first search (BFS), task scheduling, or any scenario requiring processing in the order of arrival.
	•	Key Patterns:
	•	BFS traversal.
	•	Order-preserving task scheduling.
	•	LeetCode Problem Types:
	•	Binary Tree Level Order Traversal (Problem #102)
	•	Sliding Window Maximum (Problem #239)

Python Implementation:

from collections import deque
queue = deque()
queue.append(1)       # Enqueue
queue.popleft()       # Dequeue

Time Complexity:

	•	Enqueue/Dequeue: O(1)

4. Priority Queue (Min Heap using heapq)

	•	Description: A priority queue allows elements to be inserted and removed based on priority. By default, heapq in Python implements a min-heap.
	•	When to Use: Use in problems where you need to dynamically extract the minimum (or maximum) element, such as in Dijkstra’s or Prim’s algorithm.
	•	Key Patterns:
	•	Kth smallest or largest element.
	•	Greedy algorithms.
	•	Real-time stream of data.
	•	LeetCode Problem Types:
	•	Kth Largest Element in an Array (Problem #215)
	•	Merge K Sorted Lists (Problem #23)

Python Implementation:

import heapq

min_heap = []
heapq.heappush(min_heap, 3)
heapq.heappop(min_heap)  # Extract min

Time Complexity:

	•	Insert: O(log n)
	•	Pop: O(log n)

5. Max Heap (Using heapq for Max Heap)

	•	Description: Python’s heapq module only supports min-heaps, but you can simulate a max-heap by pushing negative values.
	•	When to Use: Use in problems where you need to extract the maximum element dynamically.
	•	Key Patterns:
	•	Extracting the largest element.
	•	Managing large data streams.
	•	LeetCode Problem Types:
	•	K Closest Points to Origin (Problem #973)
	•	Sliding Window Maximum (Problem #239)

Python Implementation:

import heapq

max_heap = []
heapq.heappush(max_heap, -3)  # Push negated value to simulate max heap
heapq.heappop(max_heap)       # Extract max (-1 * popped value)

Time Complexity:

	•	Insert: O(log n)
	•	Pop: O(log n)

6. Linked List

	•	Description: Linked lists are sequential structures where each element points to the next. They allow for efficient insertions and deletions at any point in the list.
	•	When to Use: Use when you need dynamic resizing and frequent insertions/deletions.
	•	Key Patterns:
	•	Reversing lists.
	•	Merging sorted lists.
	•	Implementing LRU caches.
	•	LeetCode Problem Types:
	•	Reverse Linked List (Problem #206)
	•	Merge Two Sorted Lists (Problem #21)

Python Implementation:

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        current = self.head
        while current.next:
            current = current.next
        current.next = new_node

Time Complexity:

	•	Access: O(n)
	•	Insert/Delete: O(1)

7. Hash Tables (Dictionaries in Python)

	•	Description: A hash table allows fast lookups, insertions, and deletions by mapping keys to values.
	•	When to Use: Use when you need to count frequencies, perform lookups, or implement caching.
	•	Key Patterns:
	•	Frequency counting.
	•	Two-sum like problems.
	•	Caching.
	•	LeetCode Problem Types:
	•	Two Sum (Problem #1)
	•	Longest Substring Without Repeating Characters (Problem #3)

Python Implementation:

hash_map = {}
hash_map['key'] = 'value'
hash_map.pop('key')  # Remove key

Time Complexity:

	•	Insert/Access/Delete: O(1) (amortized)

8. Binary Search Trees (BST)

	•	Description: A Binary Search Tree (BST) is a tree structure where each node has at most two children, and for every node, the left child is smaller, and the right child is larger.
	•	When to Use: Use when you need to maintain a dynamic set of sorted elements or perform range queries.
	•	Key Patterns:
	•	Dynamic sets.
	•	Searching and inserting in sorted data.
	•	LeetCode Problem Types:
	•	Validate Binary Search Tree (Problem #98)
	•	Kth Smallest Element in a BST (Problem #230)

Python Implementation (using sortedcontainers.SortedDict):

from sortedcontainers import SortedDict
bst = SortedDict()
bst[10] = 'value'
del bst[10]

Time Complexity:

	•	Insert/Access/Delete: O(log n)

9. Segment Tree

	•	Description: Segment trees allow for efficient range queries and updates on an array of data, often used when you need to perform sum, minimum, or maximum queries.
	•	When to Use: Use when you need to query and update ranges of data efficiently.
	•	Key Patterns:
	•	Range sum or range min/max queries.
	•	Point updates.
	•	LeetCode Problem Types:
	•	Range Sum Query - Mutable (Problem #307)

Python Implementation:

class SegmentTree:
    def __init__(self, arr):
        self.n = len(arr)
        self.tree = [0] * (2 * self.n)
        for i in range(self.n):
            self.tree[self.n + i] = arr[i]
        for i in range(self.n - 1, 0, -1):
            self.tree[i] = self.tree[2 * i] + self.tree[2 * i + 1]

    def update(self, pos, value):
        pos += self.n
        self.tree[pos] = value
        while pos > 1:
            pos //= 2
            self.tree[pos] = self.tree[2 * pos] + self.tree[2 * pos + 1]

    def sum_range(self, left, right):
        res = 0
        left += self.n
        right += self.n
        while left < right:
            if left % 2:
                res += self.tree[left]
                left += 1
            if right % 2:
                right -= 1
                res += self.tree[right]
            left //= 2
            right //= 2
        return res

Time Complexity:

	•	Build: O(n)
	•	Update: O(log n)
	•	Query: O(log n)

10. Union-Find (Disjoint Set)

	•	Description: Union-Find is used to keep track of a partition of a set into disjoint subsets and supports union and find operations.
	•	When to Use: Use in problems requiring dynamic connectivity, detecting cycles, or solving minimum spanning trees.
	•	Key Patterns:
	•	Dynamic connectivity.
	•	Detecting cycles in graphs.
	•	LeetCode Problem Types:
	•	Number of Connected Components in an Undirected Graph (Problem #323)
	•	Redundant Connection (Problem #684)

Python Implementation:

class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [1] * n

    def find(self, u):
        if self.parent[u] != u:
            self.parent[u] = self.find(self.parent[u])
        return self.parent[u]

    def union(self, u, v):
        root_u = self.find(u)
        root_v = self.find(v)
        if root_u != root_v:
            if self.rank[root_u] > self.rank[root_v]:
                self.parent[root_v] = root_u
            elif self.rank[root_u] < self.rank[root_v]:
                self.parent[root_u] = root_v
            else:
                self.parent[root_v] = root_u
                self.rank[root_u] += 1

Time Complexity:

	•	Find/Union: O(α(n)), where α is the inverse Ackermann function

11. Tries (Prefix Trees)

	•	Description: Tries are tree-like structures used to store strings where each node represents a character.
	•	When to Use: Use in problems involving prefix matching or searching a collection of strings.
	•	Key Patterns:
	•	Autocomplete systems.
	•	Prefix search.
	•	LeetCode Problem Types:
	•	Implement Trie (Prefix Tree) (Problem #208)
	•	Word Search II (Problem #212)

Python Implementation:

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    def search(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end_of_word

Time Complexity:

	•	Insert/Search: O(m), where m is the length of the word

12. Deque (Double-Ended Queue using collections.deque)

	•	Description: Deque supports adding and removing elements from both ends efficiently.
	•	When to Use: Use in problems involving sliding windows or managing sequences from both ends.
	•	Key Patterns:
	•	Sliding window problems.
	•	Maintaining monotonic sequences.
	•	LeetCode Problem Types:
	•	Sliding Window Maximum (Problem #239)

Python Implementation:

from collections import deque
dq = deque()
dq.append(1)
dq.appendleft(2)
dq.pop()
dq.popleft()

Time Complexity:

	•	Append/Pop: O(1)

13. Balanced Trees (Using SortedDict)

	•	Description: A self-balancing binary search tree like AVL or Red-Black Tree is used when you need to maintain a dynamic sorted dataset.
	•	When to Use: Use when you need dynamic sorted data or range queries with balancing.
	•	Key Patterns:
	•	Maintaining a sorted set of data.
	•	Range queries.
	•	LeetCode Problem Types:
	•	Kth Largest Element in a Stream (Problem #703)

Python Implementation:

from sortedcontainers import SortedDict
bst = SortedDict()
bst[10] = 'value'
del bst[10]

Time Complexity:

	•	Insert/Delete/Access: O(log n)

By understanding when to apply each of these data structures and their associated time and space complexities, you can better tackle a wide variety of competitive coding problems on platforms like LeetCode.