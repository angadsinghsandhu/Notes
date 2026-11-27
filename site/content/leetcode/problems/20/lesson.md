# Valid Parentheses

Given a string `s` of 1 to 10,000 characters drawn from `()[]{}`, return whether every opening bracket is closed by its matching type in nesting order. An opening can enclose other pairs, and complete pairs can sit next to one another. [Official problem and constraints](https://leetcode.com/problems/valid-parentheses/)

## Work through the inputs

- `(()` returns `false`. The last character closes the inner pair, leaving one opening at the end.
- `]()` returns `false`. The first bracket has no opening before it.
- `([)]` returns `false`. When `)` arrives, the still-open `[` is inside the `(`, so it has to close first.
- `{[()]}` returns `true`. Each closing bracket removes the most recent unmatched opening, and the stack ends empty.

## Keep a stack of unmatched openings

Read left to right. Push each opening bracket onto a list. At a closing bracket, get its required opening from the lookup table and inspect the end of the list. Reject if the list is empty or its last element has the wrong type. Otherwise pop that element. After reading the whole string, accept if the list is empty.

The trace shows the stack after each push or pop. The highlight marks the current top, the last item in the list. On rejection the stack stays as it was just before the mismatched closing bracket. The final frame for `(()` still shows the outer `(`, which explains why a successful pop alone is insufficient.

## Why it works

After each accepted prefix, the stack contains exactly its unmatched openings in encounter order. Initially there are none. Reading an opening appends the newest one. A closing bracket must close that newest opening first. Closing an earlier one would cross the newest pair, and encountering a closer with no openings gives it no legal partner. A matching top can safely be removed, preserving the invariant. If the scan reaches the end, all brackets are paired exactly when the stack is empty.

With tracing off, each character takes constant amortized work, so the scan takes `O(n)` time and uses `O(d)` auxiliary space for maximum stack depth `d`. In the worst case every character is an opening and `d = n`. The trace copies the current stack to preserve each snapshot, so producing it takes additional work proportional to the total number of stack entries displayed across all frames. The checked-in examples are short enough to keep those snapshots bounded.

The archive has a solver for this same identity. The annotated implementation here is new and is checked by independently canceling adjacent matching pairs.
