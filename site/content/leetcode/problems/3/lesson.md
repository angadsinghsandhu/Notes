# Longest Substring Without Repeating Characters

Find the greatest length of a contiguous stretch of `s` in which each character occurs once. The string can contain up to 100,000 characters, and can include letters, digits, symbols, and spaces. A space participates just like any other character. An empty string returns zero. [Official problem and constraints](https://leetcode.com/problems/longest-substring-without-repeating-characters/)

## Find a window worth keeping

Use inclusive indices `left` and `right` for the current window. At each step, advance `right` by one and find the smallest `left` that makes the new window distinct. That gives the longest eligible stretch ending at `right`. Record its length, `right - left + 1`, if it improves the best so far.

- `cabbde` returns 3. At the second `b`, the set approach removes `c`, `a`, and the first `b`. The index approach gets to the same boundary in one jump. Both `cab` and `bde` reach length 3.
- `abba` returns 2. When the last `a` arrives, the window holds the second `b`. The first `a` is already outside it, so the boundary stays at index 2 and the new window is `ba`.
- `" !1! 2"` returns 4. The final stretch `"1! 2"` includes a symbol, a space, and two digits.
- `""` returns 0. There is no character to admit, so the initial best is the answer.

## Evict one character at a time

Keep a set of the characters currently in the window. Before admitting the incoming character, check the set. While it still contains a copy, remove the character at `left` and advance `left`. Once the copy has gone, insert the incoming character and update the best length.

The set mirrors the window before each step. Every starting index through the earlier copy would leave both copies in the new window. Removing from the left through that copy is therefore both necessary and sufficient. The other characters in the window were already distinct, and an earlier start than the old boundary would retain a duplicate from the previous prefix. The resulting window is the longest distinct suffix of the current prefix.

## Jump past the last occurrence

Keep a dictionary from character to the most recent index where it was seen. When the incoming character's previous index is at least `left`, set `left` to that index plus one. Then record the current index and update the best length. An unseen character has no earlier copy, and a previous index smaller than `left` has already been excluded.

The dictionary describes the processed prefix before every step. Since the current window is distinct, a repeated character inside it occurs exactly once there. Moving past that occurrence removes the only new duplicate and preserves the longest possible suffix. With a stale previous index, jumping would move `left` backwards and could bring a duplicate back into the window, as in `abba`.

For both approaches, a global optimum ends at some index visited by the scan. Since each step considers the longest valid window ending at that index, tracking the maximum finds the optimum.

## Compare cost and trace the boundaries

For a string of length `n` containing `u` distinct characters, both approaches take expected `O(n)` time with hash-based lookups and use at most `O(u)` auxiliary space. Each character enters the set once and leaves at most once. The dictionary does constant expected work per character and may keep entries for characters that have already left the window. The set holds only the active characters.

The highlights show the active window. During an eviction or jump, the incoming character is still outside the window. The next frame admits it and reports the best length. The final frame keeps the last window visible and reports the answer, which may come from an earlier window. Tracing copies the input and the highlighted indices per frame, so the walkthroughs use short inputs.

The archive records a solver for this identity. Both annotated implementations here are new. The evidence checker scans backwards from each endpoint to recover its longest distinct suffix independently.
