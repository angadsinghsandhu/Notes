# LRU Cache

Build a fixed-capacity cache for integer keys and values. `get(key)` returns the stored value, or `-1` for a miss. `put(key, value)` inserts or updates an entry. A hit or a write makes the affected key the most recently used. An insertion that exceeds capacity removes the least recently used key. Each operation must take `O(1)` average time. Capacity is 1–3,000, keys are 0–10,000, values are 0–100,000, and the input has at most 200,000 operations. [Official problem and constraints](https://leetcode.com/problems/lru-cache/)

The lesson input separates `capacity` from `operations`. The output has one slot per operation. Each write contributes `null`, and each read contributes its return value.

## Work through the inputs

- At capacity two, write `1=10` and `2=20`, then overwrite key `1` with `11`. The recency order becomes `[2=20, 1=11]`. Writing `3=30` evicts key `2`. A read of `2` misses and keeps the order intact. A read of `1` returns `11`.
- At capacity two, writing `0=0` and `1=5` initially makes key `0` the oldest. Reading `0` returns `0` and moves it to the newest end. Writing `2=6` now evicts key `1`.
- At capacity one, a read of `4` first misses. Write `4=40` and overwrite it with `41`. Writing `5=50` evicts key `4`, so the next reads of `4` and `5` return `-1` and `50`.

## Pair a hash map with a doubly linked list

The map finds the node for any key in average constant time. The list tracks when each key was last used. A sentinel closes the list into a circle, with the oldest entry immediately after it and the newest immediately before it. An empty cache links the sentinel to itself in both directions.

On a hit, detach the node and insert it just before the sentinel. On a write, update the existing node and move it, or create a new node at that position. If the write goes over capacity, detach the node immediately after the sentinel and delete the matching key from the map. The sentinel makes these pointer operations the same for a middle entry, the oldest entry, and the only entry.

Each trace frame shows the cache after one operation, from oldest on the left to newest on the right. The highlight marks the key just used. A miss leaves the cache as it was and highlights nothing. The `put` helper reports an evicted key for the trace, and the lesson adapter records `null` for the write itself.

## Why it works

After each operation, every cached key has exactly one node and the map points to it. From the sentinel's next node to its previous node, the nodes are in increasing order of the time they were last read successfully or written. Initially the map and list contain no cached entries. A miss changes neither structure. A hit or overwrite moves exactly one node to the newest end, preserving the relative order of all others. An insertion adds a new node there, so the oldest entry is the first node if capacity is exceeded. Removing it from both structures restores the size bound and preserves the map and order invariants.

Without trace capture, each `get` or `put` uses a constant number of map operations and pointer updates, giving `O(1)` average time per operation and `O(capacity)` cache space. The lesson adapter also collects the operation results. Capturing a frame copies up to `capacity` entries, so playback is limited to short example streams. The independent checker records the time of each successful access and selects the least recent entry by its timestamp.
