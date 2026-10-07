---
title: "9. Model Evaluation & Validation"
---
# 9. Model Evaluation & Validation

---

## Key Concepts

### 9.1 Train/Validation/Test Splits

#### Why Split Data?

```
Training set:   Learn model parameters
Validation set: Tune hyperparameters, model selection
Test set:       Final unbiased evaluation

Without proper splits:
- Overfitting goes undetected
- Hyperparameter tuning leaks information
- Reported performance is optimistic
```

#### Standard Split

```
┌─────────────────────────────────────────────────────┐
│                    Full Dataset                      │
├────────────────────────┬──────────┬─────────────────┤
│      Training (60%)    │Val (20%) │   Test (20%)    │
└────────────────────────┴──────────┴─────────────────┘

Common ratios:
- 60/20/20 (small datasets)
- 80/10/10 (medium datasets)
- 98/1/1 (large datasets, millions of samples)
```

#### Data Leakage

```
Problem: Information from test/val leaks into training

Common causes:
1. Feature engineering on full data before split
2. Normalization using full data statistics
3. Duplicate samples across splits
4. Time series: future data in training

Prevention:
- Split FIRST, then preprocess
- Use only training statistics for normalization
- Check for duplicates
- Respect temporal order
```

#### Stratified Splitting

```
Maintain class distribution across splits

Original: 90% class A, 10% class B
Train:    90% class A, 10% class B  ✓
Val:      90% class A, 10% class B  ✓
Test:     90% class A, 10% class B  ✓

Important for imbalanced datasets
```

```python
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)
```

---

### 9.2 Cross-Validation

Use all data for both training and validation by rotating splits.

#### K-Fold Cross-Validation

```
Split data into K folds, train K times

Fold 1: [Val  ][Train][Train][Train][Train]
Fold 2: [Train][Val  ][Train][Train][Train]
Fold 3: [Train][Train][Val  ][Train][Train]
Fold 4: [Train][Train][Train][Val  ][Train]
Fold 5: [Train][Train][Train][Train][Val  ]

Final score = average of K validation scores
```

**Algorithm:**
```
scores = []
for k in range(K):
    val_fold = data[k]
    train_folds = data[not k]
    
    model.fit(train_folds)
    score = model.evaluate(val_fold)
    scores.append(score)

mean_score = mean(scores)
std_score = std(scores)
```

**Choosing K:**
```
K = 5:  Standard choice, good balance
K = 10: More reliable estimate, slower
K = n:  Leave-one-out (LOO), maximum data usage
```

#### Stratified K-Fold

```
Maintain class distribution in each fold

Essential for:
- Imbalanced datasets
- Small datasets
- Multi-class problems
```

```python
from sklearn.model_selection import StratifiedKFold

skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
for train_idx, val_idx in skf.split(X, y):
    X_train, X_val = X[train_idx], X[val_idx]
    y_train, y_val = y[train_idx], y[val_idx]
```


#### Leave-One-Out (LOO)

```
K = n (each sample is its own fold)

For i = 1 to n:
    Train on all samples except i
    Validate on sample i

Pros:
- Maximum training data
- Deterministic (no randomness)

Cons:
- Computationally expensive: O(n) model fits
- High variance in estimate
- Only practical for small datasets
```

#### Leave-P-Out

```
Leave P samples out for validation

More general than LOO
C(n, p) possible combinations
Usually too expensive for p > 1
```

#### Group K-Fold

```
Ensure groups don't span train/val

Example: Multiple samples per patient
- Patient 1: samples 1, 2, 3
- Patient 2: samples 4, 5
- Patient 3: samples 6, 7, 8

Wrong: Patient 1's samples in both train and val
Right: All of patient's samples in same fold
```

```python
from sklearn.model_selection import GroupKFold

gkf = GroupKFold(n_splits=5)
for train_idx, val_idx in gkf.split(X, y, groups=patient_ids):
    # All samples from same patient in same split
    pass
```

#### Time Series Split

```
Respect temporal order: train on past, validate on future

Fold 1: [Train     ][Val]
Fold 2: [Train          ][Val]
Fold 3: [Train               ][Val]
Fold 4: [Train                    ][Val]

Never use future data to predict past!
```

```python
from sklearn.model_selection import TimeSeriesSplit

tscv = TimeSeriesSplit(n_splits=5)
for train_idx, val_idx in tscv.split(X):
    # train_idx always before val_idx
    pass
```

#### Cross-Validation Comparison

| Method | Use Case | Pros | Cons |
|--------|----------|------|------|
| K-Fold | General | Balanced | Random splits |
| Stratified K-Fold | Imbalanced | Preserves distribution | - |
| LOO | Small data | Max training data | Expensive, high variance |
| Group K-Fold | Grouped data | No leakage | Need group labels |
| Time Series | Temporal data | Respects time | Less training data |

---

### 9.3 Nested Cross-Validation

Separate hyperparameter tuning from performance estimation.

```
Outer loop: Estimate generalization performance
Inner loop: Tune hyperparameters

┌─────────────────────────────────────────────────────┐
│ Outer Fold 1: [Test    ][  Train/Val for inner CV  ]│
│ Outer Fold 2: [Train/Val][Test    ][   Train/Val   ]│
│ Outer Fold 3: [Train/Val         ][Test   ][T/V    ]│
└─────────────────────────────────────────────────────┘

For each outer fold:
    Inner CV to find best hyperparameters
    Train final model on outer train
    Evaluate on outer test
```

**Why Nested CV?**
```
Single CV with hyperparameter tuning:
- Validation set used for both tuning AND evaluation
- Optimistic bias in reported performance

Nested CV:
- Inner loop: tune hyperparameters
- Outer loop: unbiased performance estimate
- More reliable, especially for small datasets
```

---

### 9.4 Evaluation Metrics

#### Classification Metrics

**Confusion Matrix:**
```
                 Predicted
              Pos      Neg
Actual Pos [  TP   |   FN  ]
Actual Neg [  FP   |   TN  ]

TP = True Positive (correct positive)
FP = False Positive (Type I error)
FN = False Negative (Type II error)
TN = True Negative (correct negative)
```

**Basic Metrics:**
```
Accuracy = (TP + TN) / (TP + TN + FP + FN)
- Overall correctness
- Misleading for imbalanced data

Precision = TP / (TP + FP)
- Of predicted positives, how many are correct?
- High when FP is costly (spam detection)

Recall (Sensitivity) = TP / (TP + FN)
- Of actual positives, how many did we find?
- High when FN is costly (disease detection)

Specificity = TN / (TN + FP)
- Of actual negatives, how many did we find?

F1 Score = 2 * (Precision * Recall) / (Precision + Recall)
- Harmonic mean of precision and recall
- Balanced metric
```

**ROC and AUC:**
```
ROC Curve: TPR vs FPR at different thresholds
- TPR = Recall = TP / (TP + FN)
- FPR = FP / (FP + TN)

AUC = Area Under ROC Curve
- 0.5: Random classifier
- 1.0: Perfect classifier
- Threshold-independent
```

```
TPR
 1 |      ___________
   |     /
   |    /
   |   /
   |  /
   | /
 0 |/________________
   0               1  FPR
   
   AUC = area under curve
```

**Precision-Recall Curve:**
```
Better for imbalanced datasets than ROC

PR-AUC: Area under PR curve
- Focuses on positive class
- More informative when negatives dominate
```

#### Regression Metrics

```
MSE = (1/n) * sum((y - ŷ)^2)
- Penalizes large errors
- Same units as y^2

RMSE = sqrt(MSE)
- Same units as y
- More interpretable

MAE = (1/n) * sum(|y - ŷ|)
- Robust to outliers
- Same units as y

R² = 1 - SS_res / SS_tot
   = 1 - sum((y - ŷ)^2) / sum((y - ȳ)^2)
- Proportion of variance explained
- 1.0: perfect, 0: same as mean prediction
- Can be negative (worse than mean)

MAPE = (100/n) * sum(|y - ŷ| / |y|)
- Percentage error
- Undefined when y = 0
```

#### Ranking Metrics

```
NDCG (Normalized Discounted Cumulative Gain):
- Measures ranking quality
- Higher positions weighted more
- Range [0, 1]

MAP (Mean Average Precision):
- Average precision across queries
- For information retrieval

MRR (Mean Reciprocal Rank):
- 1 / rank of first relevant item
- For single relevant item scenarios
```


---

### 9.5 Model Selection

#### Hyperparameter Tuning

**Grid Search:**
```
Try all combinations of hyperparameters

param_grid = {
    'C': [0.1, 1, 10],
    'kernel': ['rbf', 'linear']
}

Total: 3 × 2 = 6 combinations

Pros: Exhaustive, finds best in grid
Cons: Exponential in number of params
```

**Random Search:**
```
Sample random combinations

Pros:
- More efficient than grid search
- Better for high-dimensional spaces
- Can find good values between grid points

Often finds good solution with fewer trials
```

**Bayesian Optimization:**
```
Use probabilistic model to guide search

1. Fit surrogate model (Gaussian Process)
2. Use acquisition function to choose next point
3. Evaluate, update model
4. Repeat

Pros: Sample-efficient
Cons: Overhead for surrogate model
```

#### Model Comparison

```
Compare models using validation/CV scores

Statistical tests:
- Paired t-test on fold scores
- Wilcoxon signed-rank test
- McNemar's test (for classifiers)

Consider:
- Mean performance
- Variance across folds
- Computational cost
- Interpretability
```

---

### 9.6 Improving Model Performance

#### Diagnosis First

```
1. Check learning curves
   - High train & val error: Underfitting
   - Low train, high val error: Overfitting
   - Both decreasing: Need more data

2. Error analysis
   - What types of errors?
   - Patterns in misclassifications?
   - Edge cases?

3. Feature importance
   - Which features matter?
   - Any useless features?
```

#### Addressing Underfitting

| Strategy | Description |
|----------|-------------|
| More complex model | Deeper network, more trees |
| More features | Feature engineering |
| Less regularization | Reduce L2, dropout |
| Train longer | More epochs |
| Better features | Domain knowledge |

#### Addressing Overfitting

| Strategy | Description |
|----------|-------------|
| More data | Data augmentation, collection |
| Regularization | L1, L2, dropout |
| Simpler model | Fewer layers, parameters |
| Early stopping | Stop when val loss increases |
| Ensemble | Combine multiple models |
| Cross-validation | Better hyperparameter tuning |

#### Data-Centric Improvements

```
1. More data
   - Often most effective
   - Data augmentation
   - Synthetic data generation

2. Better data
   - Clean labels
   - Remove outliers
   - Handle missing values

3. Better features
   - Domain expertise
   - Feature engineering
   - Feature selection
```

#### Model-Centric Improvements

```
1. Architecture
   - Try different models
   - Adjust capacity
   - Use pretrained models

2. Training
   - Learning rate tuning
   - Better optimizer
   - Longer training

3. Regularization
   - Dropout, weight decay
   - Data augmentation
   - Early stopping

4. Ensemble
   - Bagging, boosting
   - Model averaging
   - Stacking
```

---

### 9.7 Improving Model Efficiency

#### Inference Speed

| Technique | Speedup | Trade-off |
|-----------|---------|-----------|
| Quantization | 2-4x | Minor accuracy loss |
| Pruning | 2-10x | May need fine-tuning |
| Knowledge distillation | Varies | Smaller model |
| Efficient architecture | Varies | Design effort |
| Batching | Linear | Latency vs throughput |
| Caching | Varies | Memory usage |

#### Model Compression

**Quantization:**
```
Reduce precision: FP32 → INT8 → INT4

Post-training quantization:
- Quick, no retraining
- Some accuracy loss

Quantization-aware training:
- Train with quantization
- Better accuracy
```

**Pruning:**
```
Remove unimportant weights

Unstructured: Remove individual weights
Structured: Remove entire neurons/filters

Steps:
1. Train full model
2. Identify unimportant weights
3. Remove weights
4. Fine-tune
```

**Knowledge Distillation:**
```
Train small model to mimic large model

Teacher: Large, accurate model
Student: Small, fast model

Loss = α * CE(student, labels) + (1-α) * KL(student, teacher)

Student learns "soft" knowledge from teacher
```

---

## Questions & Answers

### ⭐ Q1: What is cross-validation, and why is it important?

**Answer:**

**What is Cross-Validation:**
```
Technique to evaluate model performance using all data for both training and validation.

K-Fold CV:
1. Split data into K folds
2. For each fold:
   - Train on K-1 folds
   - Validate on remaining fold
3. Average scores across folds
```

**Why It's Important:**

```
1. Better performance estimate
   - Uses all data for validation
   - Reduces variance in estimate
   - More reliable than single split

2. Detects overfitting
   - High variance across folds = unstable model
   - Large train-val gap = overfitting

3. Efficient data use
   - Critical for small datasets
   - Every sample used for validation once

4. Hyperparameter tuning
   - More reliable comparison between configs
   - Less prone to lucky/unlucky splits
```

**When to Use:**
```
- Small to medium datasets
- Model selection
- Hyperparameter tuning
- Reporting final performance

When NOT to use:
- Very large datasets (single split sufficient)
- Time series (use time-based splits)
- Grouped data (use group-aware CV)
```

**Example:**
```python
from sklearn.model_selection import cross_val_score

scores = cross_val_score(model, X, y, cv=5, scoring='accuracy')
print(f"Accuracy: {scores.mean():.3f} ± {scores.std():.3f}")
```

---

### Q2: Describe different types of cross-validation techniques.

**Answer:**

**1. K-Fold Cross-Validation:**
```
Standard approach, split into K equal folds

Use: General purpose
K=5 or K=10 typical
```

**2. Stratified K-Fold:**
```
Maintain class distribution in each fold

Use: Imbalanced classification
Essential when classes are skewed
```

**3. Leave-One-Out (LOO):**
```
K = n, each sample is a fold

Use: Very small datasets
Pros: Maximum training data
Cons: Expensive, high variance
```

**4. Group K-Fold:**
```
Keep groups together (no group spans folds)

Use: Grouped data (patients, users)
Prevents data leakage from group structure
```

**5. Time Series Split:**
```
Train on past, validate on future

Use: Temporal data
Respects time ordering
```

**6. Repeated K-Fold:**
```
Run K-fold multiple times with different splits

Use: More stable estimate
Reduces variance from random splits
```

**7. Nested Cross-Validation:**
```
Outer loop: performance estimation
Inner loop: hyperparameter tuning

Use: When tuning hyperparameters
Unbiased performance estimate
```

**Comparison:**

| Method | Data Type | Key Feature |
|--------|-----------|-------------|
| K-Fold | General | Standard |
| Stratified | Imbalanced | Preserves distribution |
| LOO | Small data | Max training data |
| Group | Grouped | No group leakage |
| Time Series | Temporal | Respects time |
| Nested | With tuning | Unbiased estimate |

---

### ⭐ Q3: Given an existing model, how would you improve its performance or efficiency?

**Answer:**

**Step 1: Diagnose the Problem**

```
Plot learning curves:

Train Loss    Val Loss     Diagnosis
High          High         Underfitting
Low           High         Overfitting
Both decreasing           Need more data/training
```

**Step 2: Improve Performance**

**If Underfitting:**
```
- Increase model complexity
  - More layers/neurons
  - More trees/depth
  
- Better features
  - Feature engineering
  - Domain knowledge
  
- Reduce regularization
  - Lower L2/dropout
  
- Train longer
  - More epochs
  - Lower learning rate
```

**If Overfitting:**
```
- More data
  - Data augmentation
  - Collect more samples
  
- Regularization
  - L1/L2, dropout
  - Early stopping
  
- Simpler model
  - Fewer parameters
  - Shallower network
  
- Ensemble methods
  - Bagging reduces variance
```

**General Improvements:**
```
- Hyperparameter tuning (learning rate, batch size)
- Better optimizer (Adam, AdamW)
- Learning rate schedule
- Pretrained models / transfer learning
- Ensemble multiple models
```

**Step 3: Improve Efficiency**

**For Inference Speed:**
```
- Quantization (FP32 → INT8)
- Pruning (remove weights)
- Knowledge distillation (smaller model)
- Efficient architecture (MobileNet, EfficientNet)
- Batching requests
- Caching predictions
```

**For Training Speed:**
```
- Mixed precision (FP16)
- Larger batch size
- Data parallelism
- Gradient accumulation
- Efficient data loading
```

**For Memory:**
```
- Gradient checkpointing
- Smaller batch size
- Model pruning
- Quantization
- Efficient attention (Flash Attention)
```

**Practical Checklist:**
```
□ Analyze errors - what's the model getting wrong?
□ Check data quality - labels correct? outliers?
□ Try simple baselines - is complex model needed?
□ Tune hyperparameters - learning rate most important
□ Add regularization - if overfitting
□ Get more data - often most effective
□ Try ensemble - usually improves performance
□ Profile inference - find bottlenecks
□ Apply compression - quantization, pruning
```

---

### Q4: When should you use precision vs recall vs F1?

**Answer:**

**Precision: Minimize False Positives**
```
Precision = TP / (TP + FP)

"Of predicted positives, how many are correct?"

Use when FP is costly:
- Spam detection (don't block legitimate email)
- Recommendation (don't annoy users)
- Legal/compliance (don't falsely accuse)
```

**Recall: Minimize False Negatives**
```
Recall = TP / (TP + FN)

"Of actual positives, how many did we find?"

Use when FN is costly:
- Disease detection (don't miss cancer)
- Fraud detection (don't miss fraud)
- Security (don't miss threats)
```

**F1: Balance Both**
```
F1 = 2 * (P * R) / (P + R)

Harmonic mean of precision and recall

Use when:
- Both FP and FN matter
- Classes are imbalanced
- Need single metric for comparison
```

**Trade-off:**
```
Threshold ↑: Precision ↑, Recall ↓
Threshold ↓: Precision ↓, Recall ↑

Adjust threshold based on business needs
```

**Example Scenarios:**

| Scenario | Priority | Why |
|----------|----------|-----|
| Cancer screening | Recall | Missing cancer is dangerous |
| Spam filter | Precision | Blocking real email is bad |
| Search results | Precision@K | Users see top K results |
| Fraud detection | Recall | Missing fraud is costly |
| Content moderation | Balance (F1) | Both errors problematic |

---

### Q5: How do you handle evaluation for imbalanced datasets?

**Answer:**

**Problem with Accuracy:**
```
Dataset: 99% negative, 1% positive
Model: Always predict negative
Accuracy: 99% (but useless!)
```

**Better Metrics:**

```
1. Precision, Recall, F1
   - Focus on minority class
   - F1 balances both

2. PR-AUC (Precision-Recall AUC)
   - Better than ROC-AUC for imbalanced
   - Focuses on positive class

3. Balanced Accuracy
   - Average of recall per class
   - (TPR + TNR) / 2

4. Matthews Correlation Coefficient (MCC)
   - Balanced measure for binary
   - Range [-1, 1], 0 = random
```

**Evaluation Strategies:**

```
1. Stratified splits
   - Maintain class ratio in all splits
   - Essential for imbalanced data

2. Class-weighted metrics
   - Weight by inverse class frequency
   - macro-F1 vs micro-F1

3. Confusion matrix analysis
   - Look at actual numbers
   - Understand error types

4. Cost-sensitive evaluation
   - Assign costs to different errors
   - Optimize for business metric
```

**Reporting:**
```
Don't just report accuracy!

Report:
- Precision, Recall, F1 for each class
- Confusion matrix
- PR curve and PR-AUC
- ROC curve and AUC (with caution)
```

