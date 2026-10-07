---
title: "10. Evaluation Metrics"
---
# 10. Evaluation Metrics

---

## Key Concepts

### 10.1 Classification Metrics

#### Confusion Matrix

```
                    Predicted
                 Pos       Neg
Actual Pos  [   TP    |   FN   ]
Actual Neg  [   FP    |   TN   ]

TP (True Positive):  Correctly predicted positive
TN (True Negative):  Correctly predicted negative
FP (False Positive): Incorrectly predicted positive (Type I error)
FN (False Negative): Incorrectly predicted negative (Type II error)
```

**Multi-class Extension:**
```
              Predicted
           A    B    C
Actual A [ 50   5    2 ]
Actual B [  3  45    7 ]
Actual C [  1   4   40 ]

Diagonal = correct predictions
Off-diagonal = errors (which class confused with which)
```

#### Accuracy

```
Accuracy = (TP + TN) / (TP + TN + FP + FN)
         = Correct / Total

Pros:
- Simple, intuitive
- Good for balanced classes

Cons:
- Misleading for imbalanced data
- 99% accuracy means nothing if 99% is one class
```

#### Precision

```
Precision = TP / (TP + FP)

"Of all predicted positives, how many are actually positive?"

High precision = Few false positives
Low precision = Many false alarms

Use when FP is costly:
- Spam detection (don't block real email)
- Recommendation (don't annoy users)
- Search results (show relevant items)
```

#### Recall (Sensitivity, True Positive Rate)

```
Recall = TP / (TP + FN)

"Of all actual positives, how many did we correctly identify?"

High recall = Few missed positives
Low recall = Many missed cases

Use when FN is costly:
- Disease detection (don't miss cancer)
- Fraud detection (don't miss fraud)
- Security threats (don't miss attacks)
```

#### Specificity (True Negative Rate)

```
Specificity = TN / (TN + FP)

"Of all actual negatives, how many did we correctly identify?"

Complement of False Positive Rate:
FPR = 1 - Specificity = FP / (FP + TN)
```

#### F1 Score

```
F1 = 2 * (Precision * Recall) / (Precision + Recall)
   = 2 * TP / (2*TP + FP + FN)

Harmonic mean of precision and recall
- Range: [0, 1]
- F1 = 1 only if both P and R are 1
- Penalizes extreme imbalance between P and R
```

**Why Harmonic Mean?**
```
Arithmetic mean: (0.9 + 0.1) / 2 = 0.5
Harmonic mean:   2 * 0.9 * 0.1 / (0.9 + 0.1) = 0.18

Harmonic mean penalizes when either is low
Can't game F1 by maximizing only one
```

#### F-beta Score

```
F_β = (1 + β²) * (P * R) / (β² * P + R)

β controls precision vs recall trade-off:
- β = 1: F1 (equal weight)
- β = 2: F2 (recall 2x more important)
- β = 0.5: F0.5 (precision 2x more important)
```


#### Multi-class Averaging

```
Macro-average: Average metric across classes (equal weight)
Micro-average: Aggregate TP, FP, FN, then compute metric
Weighted-average: Weight by class frequency

Example with 3 classes:
Class A: P=0.9, R=0.8, support=100
Class B: P=0.7, R=0.6, support=50
Class C: P=0.5, R=0.4, support=10

Macro-P = (0.9 + 0.7 + 0.5) / 3 = 0.70
Weighted-P = (0.9*100 + 0.7*50 + 0.5*10) / 160 = 0.84
```

| Averaging | When to Use |
|-----------|-------------|
| Macro | All classes equally important |
| Micro | Overall performance matters |
| Weighted | Account for class imbalance |

#### ROC Curve and AUC

```
ROC: Receiver Operating Characteristic
Plot TPR vs FPR at different thresholds

TPR (y-axis) = TP / (TP + FN) = Recall
FPR (x-axis) = FP / (FP + TN) = 1 - Specificity

TPR
 1 |        ___________
   |       /
   |      /
   |     /
   |    /
   |   /  (better)
   |  /
   | / 
 0 |/________________
   0               1  FPR
```

**AUC (Area Under Curve):**
```
AUC = 0.5: Random classifier (diagonal line)
AUC = 1.0: Perfect classifier
AUC < 0.5: Worse than random (flip predictions)

Interpretation:
AUC = P(score(positive) > score(negative))
Probability that random positive ranks higher than random negative
```

**Pros and Cons:**
```
Pros:
- Threshold-independent
- Works for ranking
- Single number summary

Cons:
- Can be misleading for imbalanced data
- Treats FP and FN equally
- May not reflect operational threshold
```

#### Precision-Recall Curve and PR-AUC

```
Plot Precision vs Recall at different thresholds

Precision
 1 |\_
   |  \_
   |    \_
   |      \_
   |        \_
   |          \_
 0 |____________\_
   0            1  Recall
```

**When to Use PR vs ROC:**
```
ROC-AUC: Balanced datasets, care about both classes
PR-AUC: Imbalanced datasets, care about positive class

Example: 1% positive, 99% negative
- ROC-AUC can be high even with many FPs
- PR-AUC better reflects performance on minority class
```

#### Log Loss (Cross-Entropy)

```
Log Loss = -(1/n) * sum(y*log(p) + (1-y)*log(1-p))

Measures quality of probability predictions
- Penalizes confident wrong predictions heavily
- Range: [0, ∞), lower is better
- Used for model training and evaluation
```

---

### 10.2 Regression Metrics

#### Mean Squared Error (MSE)

```
MSE = (1/n) * sum((y_i - ŷ_i)²)

Properties:
- Penalizes large errors heavily (squared)
- Sensitive to outliers
- Units: squared units of y
- Always non-negative
- Differentiable (good for optimization)
```

#### Root Mean Squared Error (RMSE)

```
RMSE = sqrt(MSE) = sqrt((1/n) * sum((y_i - ŷ_i)²))

Properties:
- Same units as y (interpretable)
- Still sensitive to outliers
- Most common regression metric
```

#### Mean Absolute Error (MAE)

```
MAE = (1/n) * sum(|y_i - ŷ_i|)

Properties:
- Robust to outliers
- Same units as y
- Not differentiable at 0
- Median is optimal predictor (vs mean for MSE)
```

#### MSE vs MAE

```
Example: Errors = [1, 1, 1, 10]

MSE = (1 + 1 + 1 + 100) / 4 = 25.75
MAE = (1 + 1 + 1 + 10) / 4 = 3.25

MSE heavily penalizes the outlier (10)
MAE treats all errors more equally
```

| Aspect | MSE/RMSE | MAE |
|--------|----------|-----|
| Outlier sensitivity | High | Low |
| Differentiability | Yes | No (at 0) |
| Optimal predictor | Mean | Median |
| Gradient | Proportional to error | Constant |

#### R² (Coefficient of Determination)

```
R² = 1 - SS_res / SS_tot
   = 1 - sum((y - ŷ)²) / sum((y - ȳ)²)

Where:
- SS_res = residual sum of squares
- SS_tot = total sum of squares
- ȳ = mean of y
```

**Interpretation:**
```
R² = 1.0: Perfect prediction
R² = 0.0: Same as predicting mean
R² < 0:   Worse than predicting mean (possible!)

"Proportion of variance explained by the model"
```

#### Adjusted R²

```
Adjusted R² = 1 - (1 - R²) * (n - 1) / (n - p - 1)

Where p = number of predictors

Penalizes adding features that don't improve fit
Use for model comparison with different feature counts
```

#### Mean Absolute Percentage Error (MAPE)

```
MAPE = (100/n) * sum(|y - ŷ| / |y|)

Properties:
- Scale-independent (percentage)
- Undefined when y = 0
- Asymmetric (over-predictions penalized less)
```

#### Symmetric MAPE (sMAPE)

```
sMAPE = (100/n) * sum(|y - ŷ| / ((|y| + |ŷ|) / 2))

Addresses asymmetry of MAPE
Range: [0%, 200%]
```


---

### 10.3 Ranking Metrics

#### Precision@K and Recall@K

```
Precision@K = (relevant items in top K) / K
Recall@K = (relevant items in top K) / (total relevant items)

Example: 5 relevant items, top 10 results have 3 relevant
Precision@10 = 3/10 = 0.3
Recall@10 = 3/5 = 0.6
```

#### Mean Average Precision (MAP)

```
AP = (1/R) * sum_{k=1}^n (P@k * rel(k))

Where:
- R = total relevant items
- rel(k) = 1 if item at k is relevant, 0 otherwise
- P@k = precision at position k

MAP = average AP across all queries
```

**Example:**
```
Ranked list: [R, N, R, N, R]  (R=relevant, N=not relevant)
Relevant items: 3

P@1 = 1/1 = 1.0 (relevant)
P@2 = 1/2 = 0.5 (not relevant, no contribution)
P@3 = 2/3 = 0.67 (relevant)
P@4 = 2/4 = 0.5 (not relevant, no contribution)
P@5 = 3/5 = 0.6 (relevant)

AP = (1.0 + 0.67 + 0.6) / 3 = 0.76
```

#### Mean Reciprocal Rank (MRR)

```
RR = 1 / rank of first relevant item
MRR = average RR across queries

Example:
Query 1: first relevant at position 3 → RR = 1/3
Query 2: first relevant at position 1 → RR = 1/1
Query 3: first relevant at position 2 → RR = 1/2

MRR = (1/3 + 1 + 1/2) / 3 = 0.61
```

**Use Case:** When only first relevant result matters (e.g., question answering)

#### Normalized Discounted Cumulative Gain (NDCG)

```
DCG@K = sum_{i=1}^K (2^{rel_i} - 1) / log_2(i + 1)

NDCG@K = DCG@K / IDCG@K

Where IDCG = DCG of ideal ranking (perfect order)
```

**Example:**
```
Relevance scores: [3, 2, 3, 0, 1, 2]
Predicted ranking: positions 1-6

DCG@6 = (2³-1)/log₂(2) + (2²-1)/log₂(3) + (2³-1)/log₂(4) + ...
      = 7/1 + 3/1.58 + 7/2 + 0/2.32 + 1/2.58 + 3/2.81
      = 7 + 1.89 + 3.5 + 0 + 0.39 + 1.07 = 13.85

Ideal ranking: [3, 3, 2, 2, 1, 0]
IDCG@6 = 7/1 + 7/1.58 + 3/2 + 3/2.32 + 1/2.58 + 0 = 15.77

NDCG@6 = 13.85 / 15.77 = 0.88
```

**Properties:**
```
- Range: [0, 1]
- Handles graded relevance (not just binary)
- Position-aware (higher positions weighted more)
- Standard for search and recommendation
```

#### Ranking Metrics Comparison

| Metric | Relevance | Position Weight | Use Case |
|--------|-----------|-----------------|----------|
| P@K | Binary | Equal | Top-K quality |
| MAP | Binary | Decreasing | Information retrieval |
| MRR | Binary | First only | QA, navigation |
| NDCG | Graded | Logarithmic | Search, recommendations |

---

### 10.4 NLP-Specific Metrics

#### BLEU (Bilingual Evaluation Understudy)

```
Used for: Machine translation, text generation

BLEU = BP * exp(sum_{n=1}^N w_n * log(p_n))

Where:
- p_n = modified n-gram precision
- BP = brevity penalty (penalizes short outputs)
- w_n = weights (typically uniform: 1/N)
```

**Modified Precision:**
```
Clip n-gram counts by reference maximum

Reference: "the cat sat on the mat"
Candidate: "the the the the"

Unigram "the" appears 4 times in candidate
But only 2 times in reference
Clipped count = 2

Modified precision = 2/4 = 0.5
```

**Brevity Penalty:**
```
BP = 1                    if c > r
   = exp(1 - r/c)         if c <= r

Where c = candidate length, r = reference length
Penalizes outputs shorter than reference
```

#### ROUGE (Recall-Oriented Understudy for Gisting Evaluation)

```
Used for: Summarization

ROUGE-N: N-gram recall
ROUGE-N = (matching n-grams) / (n-grams in reference)

ROUGE-L: Longest Common Subsequence
ROUGE-L = LCS(candidate, reference) / len(reference)
```

**ROUGE vs BLEU:**
```
BLEU: Precision-focused (penalizes extra words)
ROUGE: Recall-focused (penalizes missing words)

BLEU: Translation (output should match reference)
ROUGE: Summarization (capture key content)
```

#### Perplexity

```
Used for: Language models

PPL = exp(-(1/N) * sum(log P(w_i | context)))
    = exp(cross-entropy)

Lower perplexity = better model
Interpretation: "Effective vocabulary size" for prediction
```

**Example:**
```
PPL = 10: Model is as uncertain as choosing from 10 words
PPL = 100: Model is as uncertain as choosing from 100 words
```

#### Word Error Rate (WER)

```
Used for: Speech recognition

WER = (S + D + I) / N

Where:
- S = substitutions
- D = deletions
- I = insertions
- N = words in reference

Lower is better, can exceed 100%
```

#### Exact Match (EM) and F1 for QA

```
Used for: Question answering

Exact Match: 1 if prediction exactly matches answer, 0 otherwise

Token F1: 
- Treat prediction and answer as bags of tokens
- Compute precision, recall, F1 on token overlap
```

**Example:**
```
Answer: "New York City"
Prediction: "New York"

EM = 0 (not exact match)
Token F1:
  Precision = 2/2 = 1.0 (both predicted tokens in answer)
  Recall = 2/3 = 0.67 (2 of 3 answer tokens predicted)
  F1 = 2 * 1.0 * 0.67 / (1.0 + 0.67) = 0.80
```

---

### 10.5 Metric Selection Guide

#### By Task Type

| Task | Primary Metrics | Secondary |
|------|-----------------|-----------|
| Binary classification | F1, AUC-ROC, PR-AUC | Precision, Recall |
| Multi-class | Macro-F1, Accuracy | Per-class metrics |
| Imbalanced | PR-AUC, F1 | Recall at fixed precision |
| Regression | RMSE, MAE | R², MAPE |
| Ranking | NDCG, MAP | MRR, P@K |
| Translation | BLEU | METEOR, chrF |
| Summarization | ROUGE | BERTScore |
| Language model | Perplexity | Downstream tasks |
| QA | EM, F1 | - |

#### By Business Need

| Need | Metric | Why |
|------|--------|-----|
| Minimize false alarms | Precision | FP is costly |
| Don't miss positives | Recall | FN is costly |
| Balance both | F1 | Trade-off |
| Rank quality | NDCG, MAP | Position matters |
| Probability calibration | Log loss, Brier | Need good probabilities |
| Interpretable error | MAE, RMSE | Same units as target |

---

## Questions & Answers

### ⭐ Q1: Discuss the differences between precision, recall, and F1-score. When would you prioritize one over the others?

**Answer:**

**Definitions:**
```
Precision = TP / (TP + FP)
"Of predicted positives, how many are correct?"

Recall = TP / (TP + FN)
"Of actual positives, how many did we find?"

F1 = 2 * P * R / (P + R)
Harmonic mean of precision and recall
```

**Key Differences:**

| Metric | Focuses On | Penalizes |
|--------|------------|-----------|
| Precision | Prediction quality | False positives |
| Recall | Coverage | False negatives |
| F1 | Balance | Either being low |

**When to Prioritize Precision:**
```
When false positives are costly:

- Spam detection: Don't block legitimate email
- Recommendation: Don't annoy users with bad suggestions
- Legal/compliance: Don't falsely accuse
- Content moderation: Don't remove valid content

"Better to miss some than to be wrong"
```

**When to Prioritize Recall:**
```
When false negatives are costly:

- Disease screening: Don't miss cancer
- Fraud detection: Don't miss fraudulent transactions
- Security: Don't miss threats
- Search: Show all relevant results

"Better to have false alarms than to miss something"
```

**When to Use F1:**
```
When both matter equally:

- General classification benchmarks
- When you need a single metric
- Imbalanced datasets (better than accuracy)
- Model comparison

Note: F1 assumes equal cost of FP and FN
Use F-beta if costs differ
```

**Trade-off:**
```
Threshold ↑: Precision ↑, Recall ↓
Threshold ↓: Precision ↓, Recall ↑

You can't maximize both simultaneously
Choose based on business requirements
```

---

### Q2: What are common metrics for regression?

**Answer:**

**Primary Metrics:**

| Metric | Formula | Use Case |
|--------|---------|----------|
| MSE | mean((y - ŷ)²) | Optimization, penalize large errors |
| RMSE | sqrt(MSE) | Interpretable (same units as y) |
| MAE | mean(\|y - ŷ\|) | Robust to outliers |
| R² | 1 - SS_res/SS_tot | Explained variance |

**When to Use Each:**

```
RMSE:
- Standard choice
- Same units as target
- Penalizes large errors
- Use when large errors are particularly bad

MAE:
- Robust to outliers
- When all errors matter equally
- Median is optimal predictor
- Use when outliers shouldn't dominate

R²:
- Proportion of variance explained
- Compare models on same data
- Caution: can be negative, doesn't penalize complexity

MAPE:
- Scale-independent (percentage)
- Compare across different scales
- Undefined when y = 0
```

**Comparison Example:**
```
True:      [10, 20, 30, 100]
Predicted: [12, 18, 32, 50]
Errors:    [2, 2, 2, 50]

MSE = (4 + 4 + 4 + 2500) / 4 = 628
RMSE = 25.1
MAE = (2 + 2 + 2 + 50) / 4 = 14

MSE/RMSE dominated by outlier (50)
MAE more balanced
```

**Practical Advice:**
```
1. Report multiple metrics
2. RMSE for optimization
3. MAE for interpretation
4. R² for model comparison
5. Consider domain-specific metrics
```

---

### Q3: What are common evaluation metrics for NLP tasks?

**Answer:**

**By Task:**

| Task | Metrics | Notes |
|------|---------|-------|
| Classification | F1, Accuracy | Same as general ML |
| Machine Translation | BLEU, METEOR | N-gram overlap |
| Summarization | ROUGE-1/2/L | Recall-focused |
| Language Modeling | Perplexity | Lower is better |
| Question Answering | EM, F1 | Exact match + token overlap |
| Named Entity Recognition | Entity F1 | Span-level evaluation |
| Text Generation | BLEU, BERTScore | Human eval often needed |

**BLEU (Translation):**
```
- Modified n-gram precision
- Brevity penalty for short outputs
- Range: 0-100 (or 0-1)
- Higher is better
- Correlates with human judgment for translation
```

**ROUGE (Summarization):**
```
ROUGE-1: Unigram recall
ROUGE-2: Bigram recall
ROUGE-L: Longest common subsequence

Recall-focused: Does summary capture reference content?
```

**Perplexity (Language Models):**
```
PPL = exp(cross-entropy)

- Lower is better
- Measures prediction uncertainty
- PPL of 10 = choosing from 10 equally likely words
```

**Modern Metrics:**
```
BERTScore:
- Semantic similarity using BERT embeddings
- Better than n-gram for paraphrases

Human Evaluation:
- Still gold standard for generation
- Fluency, coherence, relevance
- Expensive but necessary
```

**Limitations of Automatic Metrics:**
```
- N-gram metrics miss paraphrases
- Don't capture factual correctness
- May not correlate with human preference
- Use multiple metrics + human eval
```

---

### Q4: When should you use ROC-AUC vs PR-AUC?

**Answer:**

**ROC-AUC:**
```
Plots: TPR vs FPR
Range: [0.5, 1.0] for reasonable classifiers

Use when:
- Classes are balanced
- Both classes equally important
- Want threshold-independent metric
- Comparing classifiers
```

**PR-AUC:**
```
Plots: Precision vs Recall
Range: [0, 1], baseline = proportion of positives

Use when:
- Classes are imbalanced
- Positive class is more important
- Care about precision at various recall levels
- Rare event detection
```

**Why PR-AUC for Imbalanced Data:**
```
Example: 1% positive, 99% negative

Classifier predicts all negative:
- TPR = 0, FPR = 0
- ROC point at (0, 0) - looks okay

Classifier predicts 10% positive randomly:
- Precision ≈ 1% (most predictions wrong)
- PR-AUC captures this poor performance

ROC-AUC can be misleadingly high
PR-AUC reflects actual positive class performance
```

**Comparison:**

| Aspect | ROC-AUC | PR-AUC |
|--------|---------|--------|
| Baseline | 0.5 (random) | Class proportion |
| Imbalanced data | Can be misleading | More informative |
| Focus | Both classes | Positive class |
| Interpretation | P(pos > neg) | Precision-recall trade-off |

**Practical Advice:**
```
- Report both when possible
- Imbalanced: prioritize PR-AUC
- Balanced: ROC-AUC is fine
- Consider business threshold requirements
```

