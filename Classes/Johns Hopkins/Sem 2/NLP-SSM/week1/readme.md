# Week 1

## Lecture 1: Introduction to NLP

## Lecture 2: Language Modeling

### Sparsity Problem in n-grams

Considering the occurrences of some words can be rare, which causes probabilities to be assigned zero when there are no occurrences of such n-gram in the training dataset. (i.e.,If we have never seen an event in the training dataset, then our model assigns zero probability to that event.)

One way to deal with the sparsity problem is smoothing. We can add a small delta to the count of every word in the vocabulary. In this way, every word that can come next has at least some small probability. This helps with solving a nominator sparsity problem.

### Perplexity

**Perplexity** can be best understood as the reciprocal of the geometric mean of the number of real choices that we have when deciding which token to pick next. Let’s look at a number of cases:

- In the best case scenario, the model always perfectly estimates the probability of the target token as 1. In this case the perplexity of the model is 1.

- In the worst case scenario, the model always predicts the probability of the target token as 0. In this situation, the perplexity is positive infinity.

- At the baseline, the model predicts a uniform distribution over all the available tokens of the vocabulary. In this case, the perplexity equals the number of unique tokens of the vocabulary. In fact, if we were to store the sequence without any compression, this would be the best we could do for encoding it. Hence, this provides a nontrivial upper bound that any useful model must beat.
