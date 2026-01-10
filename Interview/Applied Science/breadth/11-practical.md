# 11. Practical ML Challenges

---

## Key Concepts

### 11.1 Missing Data

#### Types of Missing Data

```
MCAR (Missing Completely At Random):
- Missingness unrelated to any variable
- Example: Random sensor failures
- Safe to drop or impute

MAR (Missing At Random):
- Missingness related to observed variables
- Example: Older people less likely to report income
- Can model missingness, impute carefully

MNAR (Missing Not At Random):
- Missingness related to the missing value itself
- Example: High earners don't report income
- Most problematic, may need domain knowledge
```

#### Detection

```python
# Check missing values
df.isnull().sum()
df.isnull().mean()  # Percentage missing

# Visualize patterns
import missingno as msno
msno.matrix(df)
msno.heatmap(df)  # Correlation of missingness
```

#### Imputation Strategies

**Simple Imputation:**
```
Mean/Median:
- Fast, simple
- Reduces variance
- Use median for skewed data

Mode:
- For categorical features
- Most frequent value

Constant:
- Fill with specific value (0, -1, "Unknown")
- Preserves missingness information
```

**Advanced Imputation:**
```
KNN Imputation:
- Use K nearest neighbors to estimate
- Considers feature relationships
- Computationally expensive

Iterative/MICE:
- Model each feature as function of others
- Iterate until convergence
- Multiple imputation for uncertainty

Model-based:
- Train model to predict missing values
- Random Forest, regression
- Can capture complex patterns
```

**Missing Indicator:**
```
Add binary column indicating missingness
- Preserves information that value was missing
- Combine with imputation
- Useful when missingness is informative
```

#### Strategy Selection

| Scenario | Strategy |
|----------|----------|
| < 5% missing, MCAR | Drop rows or mean impute |
| Numerical, few missing | Median imputation |
| Categorical | Mode or "Unknown" category |
| Many features missing | KNN or iterative imputation |
| Missingness informative | Add missing indicator |
| Time series | Forward/backward fill |

```python
from sklearn.impute import SimpleImputer, KNNImputer

# Simple
imputer = SimpleImputer(strategy='median')
X_imputed = imputer.fit_transform(X)

# KNN
imputer = KNNImputer(n_neighbors=5)
X_imputed = imputer.fit_transform(X)
```

---

### 11.2 Class Imbalance

#### The Problem

```
Imbalanced dataset:
Class 0: 9900 samples (99%)
Class 1: 100 samples (1%)

Naive classifier predicts all Class 0:
- Accuracy: 99% (misleading!)
- Recall for Class 1: 0% (useless)
```

#### Data-Level Solutions

**Oversampling (Increase Minority):**
```
Random Oversampling:
- Duplicate minority samples
- Risk: Overfitting to duplicates

SMOTE (Synthetic Minority Oversampling):
- Create synthetic samples
- Interpolate between minority neighbors
- Better than simple duplication
```

```python
from imblearn.over_sampling import SMOTE, RandomOverSampler

smote = SMOTE(random_state=42)
X_resampled, y_resampled = smote.fit_resample(X, y)
```

**Undersampling (Decrease Majority):**
```
Random Undersampling:
- Remove majority samples
- Risk: Lose information

Tomek Links:
- Remove majority samples close to minority
- Cleans decision boundary

NearMiss:
- Keep majority samples closest to minority
- Various strategies
```

**Combination:**
```
SMOTEENN: SMOTE + Edited Nearest Neighbors
SMOTETomek: SMOTE + Tomek Links

Oversample minority, then clean with undersampling
```


#### Algorithm-Level Solutions

**Class Weights:**
```python
# Sklearn
model = LogisticRegression(class_weight='balanced')
model = RandomForestClassifier(class_weight='balanced')

# Manual weights
weights = {0: 1, 1: 10}  # 10x weight for minority
model = LogisticRegression(class_weight=weights)

# PyTorch
weights = torch.tensor([1.0, 10.0])
criterion = nn.CrossEntropyLoss(weight=weights)
```

**Threshold Adjustment:**
```
Default: Predict class 1 if P(class 1) > 0.5
Adjusted: Predict class 1 if P(class 1) > threshold

Lower threshold → Higher recall, lower precision
Find optimal threshold using PR curve
```

**Cost-Sensitive Learning:**
```
Assign different costs to different errors

Cost matrix:
              Predicted
            Neg    Pos
Actual Neg [ 0     C_FP ]
Actual Pos [ C_FN   0   ]

Optimize: minimize expected cost
```

#### Evaluation for Imbalanced Data

```
DON'T use: Accuracy

DO use:
- Precision, Recall, F1
- PR-AUC (better than ROC-AUC)
- Confusion matrix
- Class-specific metrics
```

#### Strategy Selection

| Scenario | Strategy |
|----------|----------|
| Moderate imbalance (10:1) | Class weights |
| Severe imbalance (100:1) | SMOTE + class weights |
| Very few minority samples | Oversampling + augmentation |
| Large dataset | Undersampling okay |
| Need probabilities | Calibration after resampling |

---

### 11.3 Feature Engineering

#### Numerical Features

```
Scaling:
- StandardScaler: (x - mean) / std
- MinMaxScaler: (x - min) / (max - min)
- RobustScaler: Uses median and IQR (robust to outliers)

Transformations:
- Log: log(x + 1) for right-skewed data
- Square root: sqrt(x) for count data
- Box-Cox: Automatic power transformation
- Binning: Convert to categorical

Interactions:
- x1 * x2: Multiplicative interaction
- x1 / x2: Ratio features
- x1 - x2: Difference features
```

#### Categorical Features

```
One-Hot Encoding:
- Binary column per category
- Sparse for high cardinality
- Use for nominal categories

Label Encoding:
- Integer per category
- Use for ordinal categories
- Trees can handle this

Target Encoding:
- Replace category with target mean
- Risk of leakage (use CV)
- Good for high cardinality

Frequency Encoding:
- Replace with category frequency
- No leakage risk
```

```python
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from category_encoders import TargetEncoder

# One-hot
encoder = OneHotEncoder(sparse=False, handle_unknown='ignore')
X_encoded = encoder.fit_transform(X[['category']])

# Target encoding (with CV to prevent leakage)
encoder = TargetEncoder(cols=['category'])
X_encoded = encoder.fit_transform(X, y)
```

#### Time Features

```
From datetime:
- Year, month, day, hour, minute
- Day of week, weekend flag
- Quarter, week of year
- Time since event

Cyclical encoding:
- sin(2π * hour / 24), cos(2π * hour / 24)
- Preserves cyclical nature (23:00 close to 00:00)

Lag features:
- Value at t-1, t-2, ...
- Rolling statistics (mean, std)
```

#### Text Features

```
Basic:
- Length, word count
- Character count
- Special character count

TF-IDF:
- Term frequency-inverse document frequency
- Sparse representation

Embeddings:
- Word2Vec, GloVe (word level)
- Sentence transformers (sentence level)
- BERT embeddings (contextual)
```

---

### 11.4 Feature Selection

#### Filter Methods

```
Evaluate features independently of model

Correlation:
- Remove features highly correlated with each other
- Keep features correlated with target

Mutual Information:
- Measures dependency between feature and target
- Works for non-linear relationships

Variance Threshold:
- Remove low-variance features
- Near-constant features are useless
```

```python
from sklearn.feature_selection import (
    VarianceThreshold, 
    mutual_info_classif,
    SelectKBest
)

# Variance threshold
selector = VarianceThreshold(threshold=0.01)
X_selected = selector.fit_transform(X)

# Mutual information
selector = SelectKBest(mutual_info_classif, k=10)
X_selected = selector.fit_transform(X, y)
```

#### Wrapper Methods

```
Use model performance to select features

Forward Selection:
- Start with no features
- Add best feature one at a time
- Stop when no improvement

Backward Elimination:
- Start with all features
- Remove worst feature one at a time
- Stop when performance drops

Recursive Feature Elimination (RFE):
- Train model, rank features by importance
- Remove least important
- Repeat until desired number
```

```python
from sklearn.feature_selection import RFE

selector = RFE(estimator=RandomForestClassifier(), n_features_to_select=10)
X_selected = selector.fit_transform(X, y)
```

#### Embedded Methods

```
Feature selection during model training

L1 Regularization (Lasso):
- Drives coefficients to exactly zero
- Automatic feature selection

Tree-based Importance:
- Feature importance from Random Forest, XGBoost
- Based on split quality or permutation

Attention Weights:
- In neural networks
- Learn which features to focus on
```

#### Method Comparison

| Method | Pros | Cons |
|--------|------|------|
| Filter | Fast, model-agnostic | Ignores feature interactions |
| Wrapper | Considers interactions | Slow, overfitting risk |
| Embedded | Efficient, model-specific | Tied to specific model |


---

### 11.5 Data Drift and Concept Drift

#### Types of Drift

```
Data Drift (Covariate Shift):
- Input distribution P(X) changes
- P(Y|X) stays the same
- Example: User demographics shift

Concept Drift:
- Relationship P(Y|X) changes
- Example: What "spam" looks like changes

Label Drift:
- Output distribution P(Y) changes
- Example: Fraud rate increases
```

**Visual:**
```
Data Drift:              Concept Drift:
Training    Production   Training    Production
  ●●●         ○○○          ●●●         ●●●
  ●●●         ○○○          ───         ╱
  ───         ───          ○○○        ○○○
  ○○○         ○○○
              
X distribution  Same boundary,   Same X,
changes         different X      different boundary
```

#### Detection Methods

**Statistical Tests:**
```
Kolmogorov-Smirnov Test:
- Compare distributions of each feature
- p-value < threshold → drift detected

Population Stability Index (PSI):
PSI = sum((actual% - expected%) * ln(actual% / expected%))
- PSI < 0.1: No drift
- PSI 0.1-0.2: Moderate drift
- PSI > 0.2: Significant drift

Chi-Square Test:
- For categorical features
- Compare frequency distributions
```

**Model-Based Detection:**
```
Performance Monitoring:
- Track metrics over time
- Alert on significant drops

Prediction Distribution:
- Monitor P(Y) distribution
- Shift indicates potential drift

Domain Classifier:
- Train model to distinguish train vs production data
- High accuracy → significant drift
```

```python
from scipy.stats import ks_2samp

# KS test for each feature
for col in features:
    stat, p_value = ks_2samp(train[col], production[col])
    if p_value < 0.05:
        print(f"Drift detected in {col}")
```

#### Handling Drift

```
1. Retrain model on recent data
2. Use sliding window of training data
3. Online learning (continuous updates)
4. Ensemble with recent and historical models
5. Feature engineering to be more robust
```

---

### 11.6 Hyperparameter Tuning

#### Grid Search

```
Exhaustive search over parameter grid

param_grid = {
    'max_depth': [3, 5, 7],
    'learning_rate': [0.01, 0.1],
    'n_estimators': [100, 200]
}

Total combinations: 3 × 2 × 2 = 12

Pros: Thorough, finds best in grid
Cons: Exponential complexity, misses between grid points
```

```python
from sklearn.model_selection import GridSearchCV

grid_search = GridSearchCV(
    estimator=XGBClassifier(),
    param_grid=param_grid,
    cv=5,
    scoring='f1'
)
grid_search.fit(X, y)
print(grid_search.best_params_)
```

#### Random Search

```
Sample random combinations

param_distributions = {
    'max_depth': randint(3, 10),
    'learning_rate': uniform(0.01, 0.3),
    'n_estimators': randint(50, 500)
}

Pros: 
- More efficient than grid search
- Can find values between grid points
- Better for high-dimensional spaces

Cons:
- May miss optimal by chance
```

```python
from sklearn.model_selection import RandomizedSearchCV

random_search = RandomizedSearchCV(
    estimator=XGBClassifier(),
    param_distributions=param_distributions,
    n_iter=50,
    cv=5
)
```

#### Bayesian Optimization

```
Use probabilistic model to guide search

1. Fit surrogate model (Gaussian Process) to observed results
2. Use acquisition function to choose next point
   - Balance exploration vs exploitation
3. Evaluate, update surrogate
4. Repeat

Pros: Sample-efficient, finds good solutions faster
Cons: Overhead for surrogate model, sequential
```

```python
from skopt import BayesSearchCV

bayes_search = BayesSearchCV(
    estimator=XGBClassifier(),
    search_spaces={
        'max_depth': (3, 10),
        'learning_rate': (0.01, 0.3, 'log-uniform'),
        'n_estimators': (50, 500)
    },
    n_iter=50,
    cv=5
)
```

#### Comparison

| Method | Trials Needed | Parallelizable | Best For |
|--------|---------------|----------------|----------|
| Grid | Exponential | Yes | Few params, small grid |
| Random | ~60 for 95% | Yes | Many params |
| Bayesian | ~20-50 | Limited | Expensive evaluations |

---

### 11.7 Data Pipelines

#### Pipeline Components

```
┌─────────────────────────────────────────────────────────┐
│                    Data Pipeline                         │
├──────────┬──────────┬──────────┬──────────┬────────────┤
│  Ingest  │  Clean   │Transform │  Feature │   Output   │
│          │          │          │  Engineer│            │
├──────────┼──────────┼──────────┼──────────┼────────────┤
│ Load data│ Handle   │ Scale    │ Create   │ Train/Val  │
│ Validate │ missing  │ Encode   │ features │ split      │
│ Schema   │ Outliers │ Normalize│ Select   │ Save       │
└──────────┴──────────┴──────────┴──────────┴────────────┘
```

#### Sklearn Pipeline

```python
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer

# Numerical pipeline
num_pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

# Categorical pipeline
cat_pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
    ('encoder', OneHotEncoder(handle_unknown='ignore'))
])

# Combined
preprocessor = ColumnTransformer([
    ('num', num_pipeline, numerical_cols),
    ('cat', cat_pipeline, categorical_cols)
])

# Full pipeline with model
full_pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier())
])

# Fit and predict
full_pipeline.fit(X_train, y_train)
predictions = full_pipeline.predict(X_test)
```

#### Best Practices

```
1. Fit on training data only
   - Prevent data leakage
   - Transform test with training statistics

2. Version control
   - Track pipeline code
   - Save fitted transformers

3. Reproducibility
   - Set random seeds
   - Log all parameters

4. Monitoring
   - Track data statistics
   - Alert on anomalies

5. Testing
   - Unit tests for transformations
   - Integration tests for pipeline
```

---

## Questions & Answers

### ⭐ Q1: How would you handle missing data in a dataset?

**Answer:**

**Step 1: Understand the Missingness**
```
1. How much is missing?
   - < 5%: Usually safe to drop or simple impute
   - 5-20%: Need careful imputation
   - > 20%: Consider if feature is usable

2. What type of missingness?
   - MCAR: Safe to drop/impute
   - MAR: Model-based imputation
   - MNAR: Domain knowledge needed

3. Is missingness informative?
   - If yes, add missing indicator feature
```

**Step 2: Choose Strategy**

| Scenario | Strategy |
|----------|----------|
| Few missing, MCAR | Drop rows |
| Numerical feature | Median (robust) or mean |
| Categorical feature | Mode or "Unknown" category |
| Complex patterns | KNN or iterative imputation |
| Time series | Forward/backward fill |
| Missingness matters | Add indicator + impute |

**Step 3: Implementation**
```python
# Simple approach
from sklearn.impute import SimpleImputer

num_imputer = SimpleImputer(strategy='median')
cat_imputer = SimpleImputer(strategy='most_frequent')

# Advanced approach
from sklearn.impute import KNNImputer
imputer = KNNImputer(n_neighbors=5)

# With missing indicator
from sklearn.impute import MissingIndicator
indicator = MissingIndicator()
missing_flags = indicator.fit_transform(X)
```

**Step 4: Validate**
```
- Compare distributions before/after
- Check model performance with different strategies
- Use cross-validation to assess impact
```

**Key Points:**
```
- Never impute test data with test statistics
- Fit imputer on training data only
- Consider multiple imputation for uncertainty
- Document your strategy
```

---

### ⭐ Q2: How do you handle data imbalance, collinearity, feature selection, and regularization?

**Answer:**

**Data Imbalance:**
```
Problem: Model biased toward majority class

Solutions:
1. Resampling:
   - SMOTE: Create synthetic minority samples
   - Undersampling: Reduce majority class
   
2. Algorithm-level:
   - Class weights: class_weight='balanced'
   - Threshold adjustment: Lower decision threshold
   
3. Evaluation:
   - Use F1, PR-AUC instead of accuracy
   - Focus on minority class metrics
```

**Collinearity:**
```
Problem: Correlated features cause unstable coefficients

Detection:
- Correlation matrix: |r| > 0.8 is concerning
- VIF > 5-10 indicates multicollinearity

Solutions:
1. Remove one of correlated pair
2. PCA to create uncorrelated components
3. Ridge regression (L2) handles it naturally
4. Domain knowledge to combine features
```

**Feature Selection:**
```
Goal: Keep relevant features, remove noise

Methods:
1. Filter: Correlation, mutual information, variance
2. Wrapper: RFE, forward/backward selection
3. Embedded: L1 regularization, tree importance

Approach:
- Start with filter methods (fast)
- Use embedded methods during training
- Validate with wrapper if needed
```

**Regularization:**
```
Goal: Prevent overfitting

Types:
- L1 (Lasso): Sparse solutions, feature selection
- L2 (Ridge): Shrinks weights, handles collinearity
- Elastic Net: Combines L1 and L2
- Dropout: For neural networks

Selection:
- L1 when you want feature selection
- L2 when all features likely relevant
- Elastic Net when unsure
```

**Integrated Approach:**
```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import SelectFromModel
from sklearn.linear_model import LogisticRegression
from imblearn.over_sampling import SMOTE

# Handle imbalance
X_resampled, y_resampled = SMOTE().fit_resample(X, y)

# Pipeline with regularization and feature selection
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('selector', SelectFromModel(
        LogisticRegression(penalty='l1', solver='saga')
    )),
    ('classifier', LogisticRegression(
        penalty='l2',
        class_weight='balanced'
    ))
])
```

---

### Q3: What is data drift and how do you detect it?

**Answer:**

**Types of Drift:**
```
Data Drift (Covariate Shift):
- P(X) changes, P(Y|X) same
- Input distribution shifts
- Example: Customer demographics change

Concept Drift:
- P(Y|X) changes
- Relationship between features and target changes
- Example: What constitutes fraud evolves

Label Drift:
- P(Y) changes
- Target distribution shifts
- Example: Conversion rate changes seasonally
```

**Detection Methods:**

**1. Statistical Tests:**
```python
from scipy.stats import ks_2samp, chi2_contingency

# Numerical features: KS test
stat, p_value = ks_2samp(train_data, prod_data)
if p_value < 0.05:
    print("Drift detected")

# Categorical features: Chi-square
chi2, p_value, _, _ = chi2_contingency([train_counts, prod_counts])
```

**2. Population Stability Index (PSI):**
```python
def calculate_psi(expected, actual, bins=10):
    expected_percents = np.histogram(expected, bins=bins)[0] / len(expected)
    actual_percents = np.histogram(actual, bins=bins)[0] / len(actual)
    
    psi = np.sum((actual_percents - expected_percents) * 
                  np.log(actual_percents / expected_percents))
    return psi

# PSI < 0.1: No drift
# PSI 0.1-0.2: Moderate
# PSI > 0.2: Significant
```

**3. Model-Based:**
```python
# Domain classifier
combined = pd.concat([
    train.assign(source=0),
    production.assign(source=1)
])

classifier = RandomForestClassifier()
cv_score = cross_val_score(classifier, combined[features], combined['source'])

# High accuracy (> 0.6) indicates drift
```

**4. Performance Monitoring:**
```
- Track model metrics over time
- Set up alerts for significant drops
- Compare predictions to actuals when labels available
```

**Handling Drift:**
```
1. Retrain on recent data
2. Use sliding window training
3. Online learning for continuous updates
4. Ensemble recent and historical models
5. Investigate root cause
```

---

### Q4: Designing data pipelines for processing and preparing training data.

**Answer:**

**Pipeline Architecture:**
```
┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
│  Source  │ → │  Ingest  │ → │  Clean   │ → │Transform │
└──────────┘   └──────────┘   └──────────┘   └──────────┘
                                                   │
┌──────────┐   ┌──────────┐   ┌──────────┐        │
│  Deploy  │ ← │  Train   │ ← │  Split   │ ←──────┘
└──────────┘   └──────────┘   └──────────┘
```

**Key Components:**

**1. Data Ingestion:**
```python
# Validate schema
def validate_schema(df, expected_schema):
    for col, dtype in expected_schema.items():
        assert col in df.columns, f"Missing column: {col}"
        assert df[col].dtype == dtype, f"Wrong type for {col}"
```

**2. Data Cleaning:**
```python
def clean_data(df):
    # Handle missing values
    df = df.dropna(subset=['target'])  # Drop if target missing
    
    # Remove duplicates
    df = df.drop_duplicates()
    
    # Handle outliers
    for col in numerical_cols:
        q1, q3 = df[col].quantile([0.25, 0.75])
        iqr = q3 - q1
        df = df[(df[col] >= q1 - 1.5*iqr) & (df[col] <= q3 + 1.5*iqr)]
    
    return df
```

**3. Feature Engineering:**
```python
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

preprocessor = ColumnTransformer([
    ('num', Pipeline([
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ]), numerical_cols),
    ('cat', Pipeline([
        ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
        ('encoder', OneHotEncoder(handle_unknown='ignore'))
    ]), categorical_cols)
])
```

**4. Train/Test Split:**
```python
from sklearn.model_selection import train_test_split

# Stratified split for classification
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

# Time-based split for time series
train = df[df['date'] < cutoff_date]
test = df[df['date'] >= cutoff_date]
```

**Best Practices:**
```
1. Reproducibility:
   - Set random seeds
   - Version control code and data
   - Log all parameters

2. Prevent Leakage:
   - Split before any preprocessing
   - Fit transformers on train only
   - Be careful with time-based features

3. Modularity:
   - Separate concerns (cleaning, features, model)
   - Easy to swap components
   - Unit test each step

4. Monitoring:
   - Log data statistics at each step
   - Alert on anomalies
   - Track data lineage

5. Scalability:
   - Use chunked processing for large data
   - Consider distributed frameworks (Spark)
   - Cache intermediate results
```

