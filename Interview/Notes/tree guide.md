# 🌳 Tree Cheatsheet for Coding Interviews

## Introduction

A **tree** is a fundamental abstract data type that represents a hierarchical structure. It consists of a set of connected **nodes**, where each node can have multiple children but only one parent, except for the **root** node, which has no parent. Trees are a special type of graph: they are **undirected**, **connected**, and **acyclic** (no cycles).

For interviews, you'll most often encounter **binary trees** (max two children) and **binary search trees (BSTs)**. They are excellent for representing hierarchical data like file systems, JSON objects, and HTML documents.

---

## Key Terminology

- **Neighbor**: The parent or a child of a node.
- **Ancestor**: A node that can be reached by repeatedly moving from a node to its parent.
- **Descendant**: A node in a given node's subtree.
- **Degree**: The number of children a node has.
- **Level / Depth**: The number of edges on the path from the root to a node. The root is at level 0.
- **Width**: The number of nodes at a particular level.
- **Distance**: The number of edges along the shortest path between two nodes.

---

## Binary Trees

A binary tree is a tree where each node has at most two children, referred to as the **left child** and the **right child**.

### Types of Binary Trees

- **Complete Binary Tree**: A binary tree where every level, except possibly the last, is completely filled. All nodes in the last level are as far left as possible.
- **Balanced Binary Tree**: A binary tree where the height of the left and right subtrees of any node differs by no more than 1. This property is crucial for ensuring efficient operations.

---

## Tree Traversals 🚶‍♂️

Traversing a tree means visiting every node exactly once. There are two main approaches: Depth-First Search (DFS) and Breadth-First Search (BFS).

### Depth-First Search (DFS)

DFS explores as far as possible down each branch before backtracking. It's commonly implemented using recursion.

#### **1. Pre-order Traversal (Root → Left → Right)**

This traversal visits the current node first, then recursively traverses the left subtree, and finally recursively traverses the right subtree.

- **Example Result**: `1, 7, 2, 6, 5, 11, 9, 9, 5`
- **Python Code**:

    ```python
    def preOrder(tree, array=[]):
        if tree is not None:
            array.append(tree.value)
            preOrder(tree.left, array)
            preOrder(tree.right, array)
        return array
    ```

#### **2. In-order Traversal (Left → Root → Right)**

This traversal recursively traverses the left subtree, visits the current node, and then recursively traverses the right subtree.

- **Example Result**: `2, 7, 5, 6, 11, 1, 9, 5, 9`
- **Key Property**: An in-order traversal of a BST yields its elements in sorted order.
- **Python Code**:

    ```python
    def inOrder(tree, array=[]):
        if tree is not None:
            inOrder(tree.left, array)
            array.append(tree.value)
            inOrder(tree.right, array)
        return array
    ```

#### **3. Post-order Traversal (Left → Right → Root)**

This traversal recursively traverses the left subtree, then the right subtree, and finally visits the current node.

- **Example Result**: `2, 5, 11, 6, 7, 5, 9, 9, 1`
- **Python Code**:

    ```python
    def postOrder(tree, array=[]):
        if tree is not None:
            postOrder(tree.left, array)
            postOrder(tree.right, array)
            array.append(tree.value)
        return array
    ```

### Breadth-First Search (BFS) / Level-Order Traversal

BFS explores nodes level by level, from left to right. It is typically implemented with a **queue**.

- **Example Result**: `[[0], [1,7], [2,6,8,3], [4,5]]`
- **Python Code**:

    ```python
    def levelOrder(root: TreeNode) -> list[list[int]]:
        if root is None:
            return []
        
        results = []
        queue = [root]

        while queue:
            level_size = len(queue)
            current_level = []
            for _ in range(level_size):
                node = queue.pop(0)
                current_level.append(node.val)
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
            results.append(current_level)
            
        return results
    ```

---

## Binary Search Tree (BST) 🔍

A Binary Search Tree is a binary tree with a special property: for every node, all values in its left subtree are less than the node's value, and all values in its right subtree are greater than the node's value (`left < root < right`).

When a question involves a BST, the interviewer usually expects a solution faster than `O(n)`.

### Performance

For a **balanced** BST:

| Operation | Big-O Time |
| :-------- | :--------- |
| Access    | `O(log n)` |
| Search    | `O(log n)` |
| Insert    | `O(log n)` |
| Remove    | `O(log n)` |

**Space Complexity**: The space complexity for traversal is `O(h)` where `h` is the tree's height. For a balanced tree, this is `O(log n)`. For a completely skewed tree (like a linked list), it degrades to `O(n)`.

---

## Interview Corner 💡

### Things to Look Out For

- Be proficient in writing traversals **recursively** and **iteratively**. Interviewers may ask for the iterative approach if you solve the recursive one quickly.
- Remember that an in-order traversal alone is insufficient to uniquely serialize a tree; you also need a pre-order or post-order traversal.

### Common Routines

Be familiar with these common tree algorithms:

- [ ] Insert a value
- [ ] Delete a value
- [ ] Count the number of nodes
- [ ] Check if a value exists
- [ ] Calculate the height of the tree
- [ ] Determine if a binary tree is a valid BST
- [ ] Find the minimum or maximum value in a BST

### Corner Cases to Consider

- An empty tree (`root is None`).
- A tree with a single node.
- A tree with two nodes.
- A very skewed tree (behaves like a linked list).

### Key Techniques

- **Recursion**: This is the most natural approach for tree problems. Always define your **base case**, which is usually when a node is `None`. Sometimes your recursive helper function may need to return multiple values.
- **Traversing by Level**: When asked to traverse level by level, use **Breadth-First Search (BFS)** with a queue.
- **Summation of Nodes**: If a problem involves summing node values, always clarify whether values can be negative.
