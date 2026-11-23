# Two Sum

Given an integer list `nums` and an integer `target`, find the two positions whose values add up to `target`. Return their zero-based indices. The positions must be distinct, and either order is valid. These implementations return the smaller index first so the examples and checks can use a single representation.

The list has between 2 and 10,000 entries. Each value and the target are between `-10^9` and `10^9`, inclusive. Exactly one unordered pair of positions works. [Official problem and constraints](https://leetcode.com/problems/two-sum/description/)

## Prerequisites

You should be comfortable with zero-based indexing and nested loops. The sorted approach uses ascending order and a pair of inward-moving pointers. The hash approach uses dictionary lookup and insertion.

## Work through the inputs

- `nums = [-4, 8, 1, 6]`, `target = 2` gives `[0, 3]`. The negative number raises the required partner to `6`.
- `nums = [6, 1, 6]`, `target = 12` gives `[0, 2]`. Both values are `6`, each from its own position. A single occurrence of `6` cannot meet this target by itself.
- `nums = [3, 3, -4, 8, 6]`, `target = 2` gives `[2, 4]`. The repeated value is irrelevant to the answer, but it exposes how the hash table handles a second occurrence.

When a condition refers to two values, start with the pair of positions. Once you fix one value `x`, the required other value is determined by `target - x`. This observation leads to sorted elimination and to direct complement lookup.

## Enumerate pairs

For each left index, try the positions strictly to its right. Stopping at the first match is valid because the problem guarantees uniqueness. The array stays in its original order, and the trace highlights the two indices participating in each addition. On the negative-value example, index `0` first tries `1` and `2` before finding `3`.

Every valid answer has one smaller index and one larger index. The loops visit each possible pair in that orientation exactly once, so a match must be discovered. An inner loop starting at the left index would allow a false self-match.

In the worst case the loops check `n(n - 1)/2` pairs, giving `O(n²)` time and `O(1)` auxiliary space. The input is read-only and the loops use constant stack space.

## Sort indexed values and converge

Sort `(value, original index)` records and place one pointer at either end. Compare the sum at those pointers with the target. If the sum is too small, move the left pointer right. If it is too large, move the right pointer left. On equality, read the stored original indices from the two records.

The invariant is that both indices of the answer still belong to the active interval. If the endpoint sum is too small, the current left value plus any other remaining value is at most that sum. No remaining partner can make the left value work, so discarding it preserves the invariant. If the endpoint sum is too large, the current right value plus any other remaining value is at least that sum. The right endpoint can be discarded. The interval shrinks each time, and the two records are at distinct positions when equality holds.

For `[-4, 8, 1, 6]` the endpoint values are initially `-4` and `8`. Their sum is too large, so removing `8` leaves the matching endpoint `6`. For `[6, 1, 6]`, the initial sum is too small. Advancing past `1` leaves two records for `6` with different original indices. The table trace shows the sorted rows once they are available and moves the highlights after each discard.

Sorting costs `O(n log n)` time and the pointer scan costs `O(n)`. The sorted records and the sort's temporary memory use `O(n)` auxiliary space. Sorting a separate list preserves the input. The scan is iterative.

## Look up the missing value

Traverse the original list once. Before recording the current value `x`, look up `target - x` in a dictionary keyed by value. Each entry stores the latest index where that value has appeared. If the lookup succeeds, return that earlier index and the current index.

Before each lookup, every distinct value from the already processed prefix has an entry, and every stored index belongs to that prefix. A successful lookup therefore supplies a distinct earlier index with the correct value. If the unique pair is at `i < j`, the value at `i` has an entry by the time the scan reaches `j`. A later overwrite of that value before `j` would create a second valid pair with `j`, which the contract rules out.

The lookup for the first `6` in `[6, 1, 6]` sees an empty dictionary. The second `6` can look up that earlier entry. Recording the current value first could make it match itself when the target is twice that value. When checking the result of a dictionary lookup, index `0` is a valid hit, so test for a missing entry explicitly. In the repeated-nonpartner example, the trace replaces the index stored for `3` and highlights the updated entry.

Assuming expected constant-time hash lookups and amortized constant-time inserts, the scan takes expected `O(n)` time. The worst-case dictionary size is `O(n)`. The input is read-only and the scan is iterative. The complexity bounds for all three approaches describe solving without a trace callback. A recorded trace copies display state for each step, which increases execution time and storage. The packaged traces use small inputs so each one includes every comparison, pointer move, or hash update it reports.

## Compare the approaches

| Approach            | Time                    | Extra space | When to choose it                                                                                                                    |
| ------------------- | ----------------------- | ----------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| Pair enumeration    | `O(n²)` worst case      | `O(1)`      | Use it for tiny inputs or as a simple reference check. It is the only approach here with constant extra space on the unsorted input. |
| Sorted two pointers | `O(n log n)` worst case | `O(n)`      | Choose it when you want a worst-case time bound independent of hashing. Carry the original indices in a separate copy.               |
| Complement hash map | `O(n)` expected         | `O(n)`      | Choose it for a single scan of unsorted data when you can afford a dictionary of previously seen values.                             |

## Continue studying

In the **All LeetCode targets** learning path, Two Sum sits in **Hash maps and sliding windows**. The next planned lesson, **#3 Longest Substring Without Repeating Characters**, uses stored positions to track repeats as a window moves through the input.

- Try the two-pointer scan directly on already-sorted input and return one-based positions using constant extra space. [#167 Two Sum II](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/)
- Fix one value and look for a pair summing to its negation. The output is distinct value triples, so the scan must handle repeated values differently. [#15 3Sum](https://leetcode.com/problems/3sum/)

## Archive provenance

The two mapped archive files contain pair enumeration and complement lookup variants. They were read without executing them and remain available as source evidence. The lesson uses independently written implementations. Company associations remain unverified.
