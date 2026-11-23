# LeetCode pilot identity and constraint evidence

Observed 2026-11-23 18:12:39 UTC. The existing identity records already agree with the eight official problem pages. Notes source revision `5b040f280bbad62df1e1a9172a0f2ca067afc504` supplies archive evidence. No curriculum status changed during this review.

## Pilot teaching inputs

| ID | Constraint evidence | Approach and acceptance |
| --- | --- | --- |
| 1 | The input has 2–10,000 integers. Input values and target range from −10⁹ to 10⁹. There is one valid pair of distinct positions and either order is acceptable. [Two Sum](https://leetcode.com/problems/two-sum/) | Review the existing enumeration, complement lookup, and sorting with index recovery. Keep the duplicate-value case where two distinct positions form the answer. |
| 3 | The string may be empty or as long as 100,000 characters. Its alphabet includes English letters, digits, symbols and spaces. [Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/) | Compare incremental set eviction with jumping the left bound using last-seen positions. Exercise repeated characters both inside and outside the active window. |
| 20 | The input contains 1–10,000 bracket characters from the three supported bracket pairs. [Valid Parentheses](https://leetcode.com/problems/valid-parentheses/) | Teach a stack of unmatched openings. Check wrong nesting, an unmatched close and an unfinished stack. |
| 64 | A rectangular grid has 1–200 rows and columns and nonnegative cell weights of at most 200. Legal moves are right or down. [Minimum Path Sum](https://leetcode.com/problems/minimum-path-sum/) | Compare a memoized top-down grid with bottom-up dynamic programming using row storage. Use a one-column case and assert the caller's matrix stays intact. |
| 98 | The input has 1–10,000 nodes with values that fit signed 32-bit integers. The search-tree ordering is strict and applies throughout each subtree. [Validate Binary Search Tree](https://leetcode.com/problems/validate-binary-search-tree/) | Compare bound propagation with iterative in-order traversal. Check a descendant that violates an ancestor's bound, duplicates, signed extremes and deep skew. Document Python recursion behavior at the published size limit. |
| 127 | Words are 1–10 lowercase English letters long, all of equal length. The list includes up to 5,000 distinct words and the start differs from the target. [Word Ladder](https://leetcode.com/problems/word-ladder/) | Compare single-source breadth-first search with two-frontier search. Check target absence, target present but unreachable, and the off-by-one distinction between transformations and path length in words. |
| 146 | Capacity is 1–3,000, keys range from 0–10,000 and values from 0–100,000. The input can include up to 200,000 operations. Access and update require average constant time. [LRU Cache](https://leetcode.com/problems/lru-cache/) | Teach hash lookup plus explicit recency ordering. Check overwrite updates recency, a successful read affects the next eviction, and capacity one. A standard-library ordered map provides an implementation comparison. |
| 175 | `Person.personId` identifies people and `Address.addressId` identifies address rows. A person can have no matching address and result order is unconstrained. The address schema also permits multiple rows for one person. [Combine Two Tables](https://leetcode.com/problems/combine-two-tables/) | Teach a left outer join and verify null extension and result multiplicity using SQL. The archive source map has no candidate for ID 175, so this pilot needs a new implementation. |

## Archive provenance

All 366 mapped archive paths were checked against the recorded SHA-256 digests. Nine existing solver variants cover pilot IDs 1, 3, 20, 64, 98, 127 and 146, including two records each for IDs 1 and 98. Retain the exact paths, digests and dated solver identity claims in the source-map records. Refer to those archive variants as prior evidence when writing original lessons.

| Current archive disposition | Records |
| --- | ---: |
| Pending reconciliation | 188 |
| Statement only | 77 |
| Link only | 42 |
| Practice materials | 31 |
| Out of range | 14 |
| Solver variants | 9 |
| Archive support | 4 |
| Empty | 1 |

The pending records still require individual identity review. Leave conflicting or incomplete evidence unresolved until it can be corroborated. No company association was verified by this review.
