# Week 2: Lecture 4-5

## Lecture 4a

**Probability Notation**: $p(A|B)$ (signifies prob of A given B). p measures total probability of a set of outcomes (an “event”).

Properties of P (axioms):

1. $p(\emptyset) = 0$
2. $p(X) \leq p(Y) \text{ for any set } X \subseteq Y = 0$
3. $p(X \text{ and } Y) = p(X) + p(Y) \ \text{if} \ p(X \text{ or } Y) = 0$ (mutully exclusive)
4. $p(X \ and \ \neg Y) + p(X \ and \ Y) = p(X)$

Adding to conditions:

- Given P(A|B), adding more to the left always **decreases** probability, i.e. P(A, Z|B) <= A(A|B).

- Given P(A|B), adding more to the right could increase or decrease probability, i.e. $P(A|B, Z) >< P(A|B)$. This has **Lower Bias, Higher Variance**.

**Back-off** is when we reduce variables from the *right side* of the `|` pipe operator. This makes it possibe for us to estimate probabilities and get a rough estimte. Back-off **reduces our Variance but incease the Bias** of our probability estimation.

**Chain Rule** is when we reduce variables to the *left side* of the `|` pipe operator. This makes it possibe for us to break down larger estimates into smaller probabilities.

$$P(A, B, C, D|Z) = P(A|B, C, D, Z) * \\ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ P(B|C, D, Z) *\\ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ P(C|D, Z) *\\ \ \ \ \  \ \ \ \ \ \ \ \ \ \ \ \  P(D|Z)$$

Now we can use Chain Rule + Backoff (now that chain rule sends probs to the right of `|`) to simplify the above equation even further:

$$P(A, B, C, D|Z) = P(A|Z) * \\ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ P(B|Z) *\\ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ P(C|Z) *\\ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \  P(D|Z)$$

if P(A, B, C, D|Z) remain unchanged after backing off we can say that A is **Conditionally Independent** of B, C, and D.

### Modeling Language

Given that we want to model language:

$$
P(sentence=X) = \text{Probability of X being English}\\
Q(sentence=X) = \text{Probability of X being Polish}
$$

Sentence (sequence to tokens) = {$BOS, w_1, w_2, w_3, w_4, w_5..., w_n, EOS$}

uisng Chain rule to expand probability o sentence being English

$$
P(w_1, w_2, w_3,...) = P(w_1)*
