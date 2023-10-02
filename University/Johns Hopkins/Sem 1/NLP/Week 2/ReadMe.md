# Week 2: Lecture 4-6

## Lecture 4a

Given P(A|B), adding more to the left always decreases probability, i.e. P(A, Z|B) <= A(A|B).

Given P(A|B), adding more to the right could increase or decrease probability, i.e. P(A|B, Z) <> A(A|B). This has **Lower Bias, Higher Variance**.

**Back-off** is when we reduce variables from the *right side* of the `|` pipe operator. This makes it possibe for us to estimate probabilities and get a rough estimte. Back-off **reduces our Variance but incease the Bias** of our probability estimation.

**Chain Rule** is when we reduce variables to the *left side* of the `|` pipe operator. This makes it possibe for us to break down larger estimates into smaller probabilities.

P(A, B, C, D|Z) = P(A|B, C, D, Z) \* P(B|C, D, Z) \* P(C|D, Z) \* P(D|Z)

Now we can use Chain Rule + Backoff (now that chain rule sends probs to the right of `|`) to simplify the above equation even further:

P(A, B, C, D|Z) = P(A|Z) \* P(B|Z) \* P(C|Z) \* P(D|Z)

if P(A, B, C, D|Z) remain unchanged after backing off we can say that A is **Conditionally Independent** of B, c, and D.

## Lecture 4b

$$Bayes theorum: P(A|B) = { P(A) * P(B|A) \over P(B) }$$

Definitions:

- P(A|B): Posterior
- P(A): Prior (Passed into a Noisy Channel Model) (Also forms our language model)
- P(B|A): Likelihood (Given by a Noisy Channel)
- P(B): Normalization Factor

$P(B)$ can be estimated over all joint probability:

$$ P(B) = P(B, A_1) + P(B, A_2) + P(B, A_3) $$

if A_1 + A_2 + A_3 = the entire set of priori, if there is only 1 A that we know:

$$ P(B) = P(B, A) + P(B, \not A) $$

Bayes theorum can be uses for:

- Converting between P(A|B) and P(B|A)
- Updating Priori P(A) to P(A|B) given new evidence P(B)

$$ P(sentence=x|labguage=english) = P_{english}(sentence=x) $$

**Noisy Channel** Maps A to B and a **Decoder** creates the most likely reconstruction of A from B.

Given Posterori ration becomes skewed towards the outcome that is favoured by the likelihood ratio as priori ratio remains the same.

## Extraa Reading: Probability Basics
