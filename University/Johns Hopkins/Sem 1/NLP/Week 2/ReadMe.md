# Week 2: Lecture 4-6

## Lecture 4

Given P(A|B), adding more to the left always decreases probability, i.e. P(A, Z|B) <= A(A|B).

Given P(A|B), adding more to the right could increase or decrease probability, i.e. P(A|B, Z) <> A(A|B). This has **Lower Bias, Higher Variance**.

**Back-off** is when we reduce variables from the *right side* of the `|` pipe operator. This makes it possibe for us to estimate probabilities and get a rough estimte. Back-off **reduces our Variance but incease the Bias** of our probability estimation.

**Chain Rule** is when we reduce variables to the *left side* of the `|` pipe operator. This makes it possibe for us to break down larger estimates into smaller probabilities.

P(A, B, C, D|Z) = P(A|B, C, D, Z) \* P(B|C, D, Z) \* P(C|D, Z) \* P(D|Z)

Now we can use Chain Rule + Backoff (now that chain rule sends probs to the right of `|`) to simplify the above equation even further:

P(A, B, C, D|Z) = P(A|Z) \* P(B|Z) \* P(C|Z) \* P(D|Z)

if P(A, B, C, D|Z) remain unchanged after backing off we can say that A is **Conditionally Independent** of B, c, and D.
