# Word Ladder

Return the number of words in the shortest ladder from `beginWord` to `endWord`, including both endpoints. Each move changes exactly one letter. Every word after the start must occur in `wordList`. Return 0 if the ladder is impossible. The endpoints differ, and all words are the same length of 1 to 10 lowercase English letters. The dictionary contains 1 to 5,000 distinct words. [Official problem and constraints](https://leetcode.com/problems/word-ladder/)

## Work through the inputs

- Change `mint` to `mist` with `["mind", "mild", "mile"]`. The target is a single edit away, but the dictionary excludes it, so the answer is 0.
- Start at `mare` with `["care", "cane", "tone", "tune", "mare"]`. You can reach `care` and `cane`. The target `tune` is listed and is connected to `tone`, but no listed word joins those two components. The answer is 0.
- Change `i` to `a` with `["a"]`. The one edit gives a ladder of **two** words.
- Start at `aaa` and aim for `bbb` with `["aba", "aab", "abb", "baa", "bba", "bbb"]`. The three changed positions require at least three edits. Both `aaa → aab → abb → bbb` and `aaa → baa → bba → bbb` achieve that in four words.

## Find neighbors as you need them

Treat the start and dictionary words as vertices. Words that differ in one position share an edge, and every edge costs one edit. Build neighbors by trying each alternative letter in each position. A set lookup tells you whether the resulting word is available. Both searches check target membership before taking a step.

## Search from the start with a queue

Put the start in the queue with length 1. Remove the first word, and append each newly discovered neighbor with its parent's length plus one. Remove a neighbor from the remaining-word set when you append it. This prevents two parents in the same layer from adding the same word. Discard the start from that set as well, since it might already be in the dictionary.

The queue processes words in order of increasing ladder length. Every word added from the current layer has length one greater, and all known words at the current length are ahead of it. This also proves that a word's first discovery has minimum length. When the target reaches the front, its stored length is the answer. An empty queue means every word reachable from the start has been considered.

The queue trace highlights the front item about to be processed. In the competing-paths example, `baa` adds `bba` and `aba` adds `abb`. Later visits can reach the same neighbors, and each appears in the queue only once.

## Search from both ends

Keep one frontier for each endpoint, with the number of edits to each word reached from that side. Start both distances at 0. At each step expand the smaller frontier by one whole layer. On a tie, keep the current side. Swapping sides means swapping their distance maps too. If an edge reaches a word in the other map, add the two recorded distances, one edit for the connecting edge, and one more to count the words.

Why can the search return at its first connecting edge? Before that layer, the two distance maps cover every word within their current radii, say `s` and `t`. The maps have no common word. A path of at most `s + t` edits would have a word within both radii, so it would already have connected the maps. An edge from the active frontier to the other map gives a path of at most `s + t + 1` edits, which reaches the shortest possible length. If a frontier empties before a connection, that side has exhausted its reachable component.

The trace puts the active frontier before the divider and the opposite frontier after it. In the competing-paths example the start discovers three neighbors, so the next expansion begins from `bbb`. Its two neighbors still form the smaller frontier. The edge from `abb` to `aab` connects the sides with distances 1 and 1. That is three edits and four words.

## Compare the work

Let `N` be the dictionary size, `L` the word length and `A = 26` the alphabet size. Each expanded word produces `L(A − 1)` candidates. In Python, constructing and hashing a candidate string takes `O(L)`, so the search work is `O(A L²)` per expanded word. Both approaches take `O(N A L²)` worst-case time, including set construction. Expanding the smaller frontier can reduce the number of words examined. The dictionary and graph shape determine how much it saves.

Both solutions use `O(N)` extra entries and up to `O(N L)` extra space when accounting for the strings retained by the search. The queue tracks one copy of each discovered word and its ladder length. The two-frontier version keeps two distance maps so it can recognize and count a connecting edge. Neither implementation changes the input list. These bounds describe the searches with tracing off. The annotations copy queue or frontier snapshots for dictionaries of up to 32 words and sort displayed frontiers for stable playback.

The source map credits the archived solver as provenance. The explanations and annotated implementations here were written for the curriculum.
