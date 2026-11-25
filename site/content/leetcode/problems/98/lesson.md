# Validate Binary Search Tree

Return whether the given binary tree has strict search-tree ordering. For each node, every value in its left subtree must be smaller, and every value in its right subtree must be larger. Equal values invalidate the tree. The input has 1 to 10,000 nodes with values from −2³¹ to 2³¹ − 1. [Official problem and constraints](https://leetcode.com/problems/validate-binary-search-tree/)

## Work through the inputs

- Put 4 and 15 below root 10, then put 11 to the right of 4. The comparison at 4 allows 11. The comparison at 10 rules it out because 11 is still in 10's left subtree.
- Give root 8 a right child with value 8. The right child must be strictly larger, so this tree fails.
- Put the smallest signed 32-bit integer to the left of 0 and the largest to the right. Both endpoints are ordinary node values, so this tree passes.
- Put 4, 3, 2 and 1 along a chain of left children. The tree passes even though every node has at most one child.

The examples store each node in a row with its value, left child index and right child index. Row 0 is the root. A child index of `null` means that child is absent. The algorithms can read each child directly from its row, as they would from a node's child references.

## Pass bounds down from the root

Start with no lower or upper limit. Each node must fit inside the open interval set by its ancestors. When you go left, keep the lower bound and use the current node to set the upper bound. When you go right, keep the upper bound and use the current node to set the lower bound. In Python, `None` marks an absent bound, leaving both signed extremes available as values.

The root begins with no ancestral restrictions. After a value passes its own test, it can only tighten the bound it replaces. The two recursive calls therefore pass exactly the restrictions each child's ancestors impose. An absent child satisfies its constraints vacuously. The recursion succeeds precisely when every visited value fits and both subtrees pass.

The trace checks a node before descending. In the first example the visit to 4 inherits an upper bound of 10, then its right child inherits the open interval `(4, 10)`. The check at 11 fails and ends the traversal.

## Check inorder values with an explicit stack

Inorder visits the left subtree, then the node, then its right subtree. Push nodes while following left links so you can return to them once their left subtrees are done. Pop the next node, compare its value with the immediately preceding value, then follow its right link. Only the preceding value needs to be saved.

In a valid search tree, each left subtree's values come before its parent in inorder and are all smaller. The right subtree's values come later and are all larger. Applying the same reasoning inside each subtree gives strictly increasing order for the whole traversal. Conversely, if all consecutive values increase, transitivity makes every earlier value smaller than every later value. Every descendant in a left subtree appears earlier than its ancestor and every descendant in a right subtree appears later. That recovers the full search-tree rule.

The first example visits 4, then 11, then 10. At 10 the preceding value is 11, which exposes the failure. Equal consecutive values fail the same comparison in the duplicate example.

## Compare runtime and stack use

For `n` nodes and height `h`, both approaches take `O(n)` time in the worst case with tracing off. Recursive bound propagation uses `O(h)` call frames. Iterative inorder uses up to `O(h)` explicit stack space. A left chain can fill that stack with `n` nodes, while a right chain needs only one pending node at a time. Both implementations preserve the input.

A tree can have 10,000 nodes and still be shallow enough for recursion if it is balanced. A 10,000-node chain requires roughly 10,000 nested calls, which exceeds the recursion limit in the pinned Python runner and raises `RecursionError`. Use iterative inorder when the input can reach the full published depth. The explicit stack leaves the interpreter's recursion limit alone. [Python recursion-limit documentation](https://docs.python.org/3.12/library/sys.html#sys.getrecursionlimit)

The trace highlights one comparison at a time, including the one that rejects an invalid tree. Frames include the whole input tree, so the annotations emit on trees of up to 32 nodes. The bounded harness also runs 10,000-node trees with trace emission disabled by that size check.

The source map records the two archived solver variants as provenance. This lesson and its annotated implementations were authored for the curriculum.
