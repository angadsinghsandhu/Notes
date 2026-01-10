# 12. Statistics & Experimentation ⭐⭐

---

## Key Concepts

### 12.1 Probability Distributions

#### Common Distributions

**Discrete:**
```
Bernoulli(p):
- Single trial, success probability p
- P(X=1) = p, P(X=0) = 1-p
- E[X] = p, Var(X) = p(1-p)

Binomial(n, p):
- n independent Bernoulli trials
- P(X=k) = C(n,k) * p^k * (1-p)^(n-k)
- E[X] = np, Var(X) = np(1-p)

Poisson(λ):
- Count of events in fixed interval
- P(X=k) = (λ^k * e^(-λ)) / k!
- E[X] = Var(X) = λ
- Approximates Binomial when n large, p small
```

**Continuous:**
```
Uniform(a, b):
- Equal probability in [a, b]
- f(x) = 1/(b-a)
- E[X] = (a+b)/2, Var(X) = (b-a)²/12

Normal(μ, σ²):
- Bell curve, symmetric
- f(x) = (1/√(2πσ²)) * exp(-(x-μ)²/(2σ²))
- E[X] = μ, Var(X) = σ²
- 68-95-99.7 rule for 1-2-3 σ

Exponential(λ):
- Time between Poisson events
- f(x) = λ * e^(-λx)
- E[X] = 1/λ, Var(X) = 1/λ²
- Memoryless property
```

#### Bayes' Theorem

```
P(A|B) = P(B|A) * P(A) / P(B)

posterior = likelihood × prior / evidence

Example: Disease testing
- P(Disease) = 0.01 (prior)
- P(Positive|Disease) = 0.99 (sensitivity)
- P(Positive|No Disease) = 0.05 (false positive)

P(Disease|Positive) = ?

P(Positive) = 0.99*0.01 + 0.05*0.99 = 0.0594
P(Disease|Positive) = 0.99*0.01 / 0.0594 = 0.167

Only 16.7% chance of disease given positive test!
```

---

### 12.2 Central Limit Theorem (CLT)

#### Statement

```
For independent, identically distributed (iid) random variables X_1, ..., X_n
with mean μ and variance σ²:

X̄_n = (1/n) * Σ X_i

As n → ∞:
√n * (X̄_n - μ) / σ → N(0, 1)

Or equivalently:
X̄_n ~ N(μ, σ²/n) approximately for large n
```

#### Conditions

```
1. Independence: Samples must be independent
2. Identical distribution: Same distribution
3. Finite variance: σ² < ∞
4. Sample size: n ≥ 30 (rule of thumb)
   - Less if distribution is symmetric
   - More if highly skewed
```

#### Why It's Important

```
1. Enables inference about population mean
   - Don't need to know population distribution
   - Sample mean is approximately normal

2. Foundation for hypothesis testing
   - Z-tests, t-tests rely on CLT
   - Confidence intervals

3. Justifies many statistical methods
   - Linear regression assumptions
   - Maximum likelihood asymptotics
```

---

### 12.3 Law of Large Numbers (LLN)

#### Statement

```
Weak LLN:
X̄_n → μ in probability as n → ∞

For any ε > 0:
P(|X̄_n - μ| > ε) → 0 as n → ∞

Strong LLN:
X̄_n → μ almost surely as n → ∞
```

#### Intuition

```
Sample mean converges to population mean

n = 10:    X̄ might be far from μ
n = 100:   X̄ closer to μ
n = 1000:  X̄ very close to μ
n → ∞:     X̄ = μ
```

#### Applications in Data Science

```
1. Monte Carlo estimation
   - Estimate E[f(X)] by averaging samples
   - More samples → better estimate

2. Training convergence
   - SGD averages over many batches
   - Converges to expected gradient

3. A/B testing
   - More samples → more reliable estimate
   - Justifies sample size calculations
```

---

### 12.4 Hypothesis Testing

#### Framework

```
1. State hypotheses:
   H₀: Null hypothesis (status quo)
   H₁: Alternative hypothesis (what we want to show)

2. Choose significance level α (typically 0.05)

3. Collect data, compute test statistic

4. Calculate p-value or compare to critical value

5. Decision:
   p-value < α → Reject H₀
   p-value ≥ α → Fail to reject H₀
```

#### P-Value

```
P-value = P(observing data as extreme or more extreme | H₀ is true)

NOT: P(H₀ is true | data)

Interpretation:
- Small p-value: Data unlikely under H₀
- p < 0.05: "Statistically significant"
- p < 0.01: "Highly significant"
```

#### Types of Errors

```
                    Reality
                H₀ True    H₀ False
Decision  Reject   Type I     Correct
          Accept   Correct    Type II

Type I Error (α): False positive
- Reject H₀ when it's true
- P(Type I) = α (significance level)

Type II Error (β): False negative
- Fail to reject H₀ when it's false
- Power = 1 - β
```

#### Common Tests

**Z-Test:**
```
When: Known population variance, large n
Test statistic: Z = (X̄ - μ₀) / (σ/√n)
Distribution: N(0, 1) under H₀
```

**T-Test:**
```
When: Unknown variance, small n
Test statistic: t = (X̄ - μ₀) / (s/√n)
Distribution: t(n-1) under H₀

Two-sample t-test:
t = (X̄₁ - X̄₂) / √(s₁²/n₁ + s₂²/n₂)
```

**Chi-Square Test:**
```
When: Categorical data, goodness of fit
Test statistic: χ² = Σ (O_i - E_i)² / E_i
Distribution: χ²(df) under H₀
```

**ANOVA (F-Test):**
```
When: Compare means of 3+ groups
Test statistic: F = MS_between / MS_within
Distribution: F(df₁, df₂) under H₀
```


---

### 12.5 Confidence Intervals

#### Definition

```
A (1-α) confidence interval for parameter θ:

P(L ≤ θ ≤ U) = 1 - α

Interpretation:
If we repeat the experiment many times,
(1-α)% of intervals will contain true θ

NOT: θ has (1-α) probability of being in this interval
(θ is fixed, interval is random)
```

#### For Mean (Normal)

```
Known variance:
CI = X̄ ± z_{α/2} * σ/√n

Unknown variance:
CI = X̄ ± t_{α/2, n-1} * s/√n

95% CI: z_{0.025} = 1.96
99% CI: z_{0.005} = 2.576
```

#### Confidence vs Prediction Interval

```
Confidence Interval:
- For population parameter (mean)
- Uncertainty about where mean is
- Width: O(1/√n)

Prediction Interval:
- For individual observation
- Includes both mean uncertainty AND individual variation
- Width: O(1) (doesn't shrink to 0)

Prediction interval always wider than confidence interval
```

---

### 12.6 A/B Testing

#### Design

```
1. Define hypothesis:
   H₀: μ_A = μ_B (no difference)
   H₁: μ_A ≠ μ_B (two-sided) or μ_A > μ_B (one-sided)

2. Choose metrics:
   - Primary: What you're optimizing
   - Guardrail: What you don't want to hurt

3. Calculate sample size:
   n = 2 * (z_{α/2} + z_β)² * σ² / δ²
   
   Where:
   - α = significance level (typically 0.05)
   - β = Type II error (typically 0.2, so power = 0.8)
   - σ = standard deviation
   - δ = minimum detectable effect

4. Randomize users to treatment/control

5. Run experiment for predetermined duration

6. Analyze results
```

#### Sample Size Calculation

```python
from statsmodels.stats.power import TTestIndPower

analysis = TTestIndPower()
sample_size = analysis.solve_power(
    effect_size=0.2,      # Cohen's d = δ/σ
    alpha=0.05,           # Significance level
    power=0.8,            # 1 - β
    alternative='two-sided'
)
```

#### Analysis

```python
from scipy import stats

# Two-sample t-test
t_stat, p_value = stats.ttest_ind(control, treatment)

# For proportions (conversion rates)
from statsmodels.stats.proportion import proportions_ztest
z_stat, p_value = proportions_ztest(
    [successes_A, successes_B],
    [n_A, n_B]
)
```

#### Common Pitfalls

```
1. Peeking (multiple testing)
   - Looking at results before predetermined end
   - Inflates false positive rate
   - Solution: Sequential testing, fixed horizon

2. Insufficient sample size
   - Underpowered test
   - May miss real effects
   - Solution: Power analysis before experiment

3. Selection bias
   - Non-random assignment
   - Confounding variables
   - Solution: Proper randomization

4. Novelty/primacy effects
   - Users react differently to new things
   - Effect may not persist
   - Solution: Run longer, analyze by cohort

5. Multiple comparisons
   - Testing many metrics inflates false positives
   - Solution: Bonferroni correction, FDR control

6. Simpson's paradox
   - Aggregate result opposite of subgroup results
   - Solution: Segment analysis

7. Interference/spillover
   - Treatment affects control (network effects)
   - Solution: Cluster randomization
```

---

### 12.7 Multiple Testing Correction

#### The Problem

```
Testing m hypotheses at α = 0.05:
P(at least one false positive) = 1 - (1-α)^m

m = 1:   P = 0.05
m = 10:  P = 0.40
m = 100: P = 0.99

Almost guaranteed false positive with many tests!
```

#### Bonferroni Correction

```
Adjusted α = α / m

Test each hypothesis at α/m level
Controls Family-Wise Error Rate (FWER)

Conservative: May miss true effects
```

#### False Discovery Rate (FDR)

```
Benjamini-Hochberg procedure:
1. Sort p-values: p₁ ≤ p₂ ≤ ... ≤ p_m
2. Find largest k where p_k ≤ k/m * α
3. Reject H₁, ..., H_k

Controls expected proportion of false discoveries
Less conservative than Bonferroni
```

---

### 12.8 MLE vs Bayesian Inference

#### Maximum Likelihood Estimation (MLE)

```
θ_MLE = argmax_θ P(Data | θ)
      = argmax_θ Π P(x_i | θ)
      = argmax_θ Σ log P(x_i | θ)

Point estimate: Single "best" θ
No prior information used
```

**Example: Coin Flips**
```
Data: k heads in n flips
L(p) = p^k * (1-p)^(n-k)
log L(p) = k*log(p) + (n-k)*log(1-p)

d/dp: k/p - (n-k)/(1-p) = 0
p_MLE = k/n
```

#### Bayesian Inference

```
P(θ | Data) = P(Data | θ) * P(θ) / P(Data)
posterior ∝ likelihood × prior

Full distribution over θ
Incorporates prior knowledge
```

**Example: Coin Flips with Beta Prior**
```
Prior: p ~ Beta(α, β)
Likelihood: Binomial(n, k | p)
Posterior: p | Data ~ Beta(α + k, β + n - k)

Posterior mean = (α + k) / (α + β + n)
```

#### MAP Estimation

```
θ_MAP = argmax_θ P(θ | Data)
      = argmax_θ P(Data | θ) * P(θ)

Point estimate like MLE, but includes prior
Regularization interpretation
```

#### Comparison

| Aspect | MLE | Bayesian |
|--------|-----|----------|
| Output | Point estimate | Distribution |
| Prior | None | Required |
| Uncertainty | Bootstrap/asymptotic | Natural |
| Small data | May overfit | Regularized by prior |
| Computation | Often easy | Can be hard |
| Interpretation | Frequentist | Bayesian |

---

### 12.9 Skewness and Distributions

#### Skewness

```
Skewness = E[(X - μ)³] / σ³

Positive skew (right-skewed):
- Long tail on right
- Mean > Median > Mode
- Example: Income distribution

Negative skew (left-skewed):
- Long tail on left
- Mean < Median < Mode
- Example: Age at death in developed countries

       Left-skewed          Symmetric          Right-skewed
          /\                  /\                    /\
         /  \                /  \                  /  \
        /    \              /    \                /    \
    ___/      \            /      \              /      \___
    Mode Med Mean        Mode=Med=Mean        Mean Med Mode
```

#### Measuring Skewness

```
1. Pearson's First Coefficient:
   Sk₁ = (Mean - Mode) / σ

2. Pearson's Second Coefficient:
   Sk₂ = 3(Mean - Median) / σ

3. Fisher's Coefficient (moment-based):
   Sk = E[(X - μ)³] / σ³
```

#### Long-Tailed Distributions

```
Heavy tails: More extreme values than normal

Examples:
- Power law (Pareto): P(X > x) ~ x^(-α)
- Log-normal: log(X) ~ Normal
- Student's t with low df

Importance in ML:
- Outliers more common
- Mean may not be representative
- May need robust methods
- Class imbalance often follows power law
```


---

## Questions & Answers

### ⭐ Q1: What is the central limit theorem and why is it important?

**Answer:**

**Statement:**
```
For iid random variables X₁, ..., Xₙ with mean μ and variance σ²:

X̄ₙ = (1/n) Σ Xᵢ

As n → ∞: √n(X̄ₙ - μ)/σ → N(0, 1)

Equivalently: X̄ₙ ~ N(μ, σ²/n) for large n
```

**Conditions:**
```
1. Independence
2. Identically distributed
3. Finite variance
4. Sufficient sample size (n ≥ 30 rule of thumb)
```

**Why It's Important:**

```
1. Universal applicability
   - Works regardless of original distribution
   - Sum/mean of many variables → Normal

2. Foundation for inference
   - Confidence intervals
   - Hypothesis tests (z-test, t-test)
   - Don't need to know population distribution

3. Justifies statistical methods
   - Linear regression
   - Maximum likelihood asymptotics
   - Bootstrap methods

4. Practical applications
   - A/B testing: Compare sample means
   - Quality control: Process monitoring
   - Polling: Estimate population proportions
```

**Example:**
```
Rolling a die: Uniform distribution, not normal
Average of 30 dice rolls: Approximately normal!

This lets us make probability statements about averages
even when individual observations aren't normal.
```

---

### ⭐ Q2: Explain how you would design and evaluate an A/B test.

**Answer:**

**Design Phase:**

```
1. Define Hypothesis
   H₀: No difference between A and B
   H₁: B is better than A (or different)

2. Choose Metrics
   Primary: Conversion rate, revenue, engagement
   Guardrail: Latency, error rate, user complaints

3. Calculate Sample Size
   n = 2(z_α/2 + z_β)² σ² / δ²
   
   Inputs needed:
   - α = 0.05 (significance level)
   - Power = 0.8 (1 - β)
   - MDE = minimum detectable effect
   - Baseline variance

4. Determine Duration
   - Enough time for sample size
   - Cover weekly patterns
   - Account for novelty effects

5. Randomization
   - Random assignment to treatment/control
   - Check for balance in covariates
   - Consider stratification
```

**Execution:**
```
1. Implement tracking
2. Verify randomization is working
3. Monitor for bugs/issues
4. Don't peek at results (or use sequential testing)
5. Run for predetermined duration
```

**Evaluation:**
```python
from scipy import stats

# For continuous metrics
t_stat, p_value = stats.ttest_ind(control, treatment)

# For proportions
from statsmodels.stats.proportion import proportions_ztest
z_stat, p_value = proportions_ztest(
    [conversions_A, conversions_B],
    [n_A, n_B]
)

# Decision
if p_value < 0.05:
    print("Statistically significant difference")
    # Also check practical significance (effect size)
```

**Report:**
```
- Point estimate of effect
- Confidence interval
- P-value
- Sample sizes
- Segment analysis
- Recommendation
```

---

### ⭐ Q3: What is a p-value? How would you interpret it in an A/B test?

**Answer:**

**Definition:**
```
P-value = P(observing data as extreme or more extreme | H₀ is true)

It is NOT:
- P(H₀ is true)
- P(result is due to chance)
- Probability the effect is real
```

**Interpretation:**
```
p = 0.03 means:
"If there were truly no difference between A and B,
we would see a difference this large or larger
only 3% of the time by random chance."

Small p-value → Data unlikely under H₀ → Evidence against H₀
```

**In A/B Testing:**
```
Example: Testing new checkout flow
- Control: 10% conversion (1000/10000)
- Treatment: 11% conversion (1100/10000)
- p-value = 0.02

Interpretation:
"If the new checkout had no real effect,
we'd see a 1% or larger difference only 2% of the time.
This is unlikely, so we have evidence the new flow is better."

Decision at α = 0.05:
p = 0.02 < 0.05 → Reject H₀ → Statistically significant
```

**Important Caveats:**
```
1. Statistical vs practical significance
   - p < 0.05 doesn't mean effect is large or important
   - Always report effect size and confidence interval

2. Not the probability H₀ is true
   - Common misconception
   - P-value assumes H₀ is true

3. Depends on sample size
   - Large n → small p even for tiny effects
   - Small n → large p even for real effects

4. Multiple testing inflates false positives
   - Testing 20 metrics at α = 0.05
   - Expected 1 false positive even if no real effects
```

---

### Q4: What are common pitfalls in A/B testing?

**Answer:**

**1. Peeking (Early Stopping):**
```
Problem: Checking results repeatedly inflates false positive rate
- Check daily at α = 0.05 for 20 days
- Actual false positive rate ≈ 30%!

Solution:
- Pre-commit to sample size/duration
- Use sequential testing methods
- Adjust α for multiple looks
```

**2. Underpowered Tests:**
```
Problem: Not enough samples to detect real effects
- 80% power means 20% chance of missing true effect

Solution:
- Power analysis before experiment
- Ensure MDE is meaningful
- Run longer if needed
```

**3. Multiple Comparisons:**
```
Problem: Testing many metrics/segments
- 20 tests at α = 0.05 → expect 1 false positive

Solution:
- Pre-specify primary metric
- Bonferroni or FDR correction
- Distinguish exploratory vs confirmatory
```

**4. Selection Bias:**
```
Problem: Non-random assignment
- Self-selection into treatment
- Technical issues affecting assignment

Solution:
- Verify randomization balance
- Check pre-experiment metrics
- Use intention-to-treat analysis
```

**5. Novelty/Primacy Effects:**
```
Problem: Users react to change, not the change itself
- New feature gets attention initially
- Effect fades over time

Solution:
- Run longer experiments
- Analyze by user tenure
- Look at long-term metrics
```

**6. Interference/Spillover:**
```
Problem: Treatment affects control
- Social networks: treated users influence control
- Marketplace: supply/demand effects

Solution:
- Cluster randomization
- Geo-based experiments
- Account for network effects
```

**7. Simpson's Paradox:**
```
Problem: Aggregate result opposite of subgroups
- Treatment better overall
- But worse in every segment!

Solution:
- Segment analysis
- Check for confounders
- Stratified randomization
```

---

### ⭐ Q5: What is Maximum Likelihood Estimation (MLE)? How does it differ from Bayesian inference?

**Answer:**

**MLE:**
```
Find parameter θ that maximizes probability of observed data

θ_MLE = argmax_θ P(Data | θ)
      = argmax_θ Π P(xᵢ | θ)
      = argmax_θ Σ log P(xᵢ | θ)

Properties:
- Point estimate (single value)
- No prior information
- Asymptotically unbiased and efficient
- Can overfit with small data
```

**Bayesian Inference:**
```
Compute full posterior distribution over θ

P(θ | Data) ∝ P(Data | θ) × P(θ)
posterior ∝ likelihood × prior

Properties:
- Full distribution (uncertainty quantified)
- Incorporates prior knowledge
- Regularized by prior
- Computationally harder
```

**Key Differences:**

| Aspect | MLE | Bayesian |
|--------|-----|----------|
| Output | Point estimate | Distribution |
| Prior | None | Required |
| Uncertainty | Via bootstrap/asymptotics | Natural from posterior |
| Small data | May overfit | Regularized |
| Computation | Usually easy | Can be hard (MCMC) |
| Philosophy | Frequentist | Bayesian |

**Example: Coin Flips**
```
Data: 3 heads in 10 flips

MLE:
p_MLE = 3/10 = 0.3

Bayesian with Beta(1,1) prior (uniform):
Posterior: Beta(1+3, 1+7) = Beta(4, 8)
Posterior mean = 4/12 = 0.33
Posterior gives full uncertainty distribution

Bayesian with Beta(10,10) prior (believe fair):
Posterior: Beta(13, 17)
Posterior mean = 13/30 = 0.43
Prior pulls estimate toward 0.5
```

**When to Use Each:**
```
MLE:
- Large datasets
- No prior knowledge
- Need simple point estimate
- Computational constraints

Bayesian:
- Small datasets
- Have prior knowledge
- Need uncertainty quantification
- Sequential updating
```

---

### Q6: Given a left-skewed distribution with median 60, what can we conclude about mean and mode?

**Answer:**

```
Left-skewed (negative skew):
- Long tail on the LEFT
- Mean < Median < Mode

       /\
      /  \
     /    \
    /      \
___/        \
Mean  Med  Mode

Given: Median = 60

Conclusions:
- Mean < 60 (pulled left by tail)
- Mode > 60 (peak is to the right)

Order: Mean < 60 < Mode
```

**Intuition:**
```
Left tail contains extreme low values
These pull the mean down
Mode is at the peak (right side)
Median is in the middle
```

---

### Q7: You flip a coin 10 times and observe only one head. What is the null hypothesis and p-value for testing fairness?

**Answer:**

```
Null Hypothesis:
H₀: p = 0.5 (coin is fair)
H₁: p ≠ 0.5 (two-sided test)

Data: k = 1 head in n = 10 flips

Under H₀: X ~ Binomial(10, 0.5)

P-value (two-sided):
P(X ≤ 1 or X ≥ 9 | p = 0.5)
= P(X ≤ 1) + P(X ≥ 9)
= [C(10,0)(0.5)¹⁰ + C(10,1)(0.5)¹⁰] × 2
= [1/1024 + 10/1024] × 2
= 11/1024 × 2
= 22/1024
≈ 0.0215

Conclusion:
p-value ≈ 0.02 < 0.05
Reject H₀ at α = 0.05
Evidence suggests coin is not fair
```

---

### Q8: You are testing hundreds of hypotheses with t-tests. What considerations would you take?

**Answer:**

```
Problem: Multiple Testing
- 100 tests at α = 0.05
- Expected false positives: 100 × 0.05 = 5
- P(at least one false positive) ≈ 99%

Solutions:

1. Bonferroni Correction
   - Test each at α/m = 0.05/100 = 0.0005
   - Controls FWER (family-wise error rate)
   - Very conservative, may miss true effects

2. Benjamini-Hochberg (FDR)
   - Controls false discovery rate
   - Less conservative than Bonferroni
   - Sort p-values, find threshold

3. Pre-registration
   - Specify primary hypothesis beforehand
   - Distinguish confirmatory vs exploratory

4. Hierarchical Testing
   - Test overall effect first
   - Only test subgroups if overall significant

5. Report All Tests
   - Transparency about how many tests run
   - Let readers assess

Practical Approach:
- Use FDR for discovery (exploratory)
- Use Bonferroni for confirmation
- Always report number of tests conducted
```

---

### Q9: How do you calculate blended mean and standard deviation from K subsets?

**Answer:**

```
Given K subsets with:
- nᵢ = sample size of subset i
- x̄ᵢ = mean of subset i
- sᵢ = standard deviation of subset i

Blended Mean:
x̄ = Σ(nᵢ × x̄ᵢ) / Σnᵢ
  = (n₁x̄₁ + n₂x̄₂ + ... + nₖx̄ₖ) / (n₁ + n₂ + ... + nₖ)

Blended Variance:
s² = [Σnᵢ(sᵢ² + x̄ᵢ²) - n×x̄²] / n

Or equivalently:
s² = [Σnᵢsᵢ² + Σnᵢ(x̄ᵢ - x̄)²] / n
     └─────────┘   └──────────────┘
     within-group   between-group
     variance       variance

Blended Std Dev:
s = √s²
```

**Example:**
```
Subset 1: n₁=100, x̄₁=50, s₁=10
Subset 2: n₂=200, x̄₂=60, s₂=15

Blended mean:
x̄ = (100×50 + 200×60) / 300 = 17000/300 = 56.67

Blended variance:
s² = [100×(100+2500) + 200×(225+3600) - 300×56.67²] / 300
   = [260000 + 765000 - 963333] / 300
   = 205.56

s = √205.56 ≈ 14.34
```

---

### Q10: What is the relationship between significance level and confidence level?

**Answer:**

```
Significance Level (α):
- Probability of Type I error
- Rejecting H₀ when it's true
- Typically 0.05 or 0.01

Confidence Level (1 - α):
- Probability interval contains true parameter
- Complement of significance level
- Typically 0.95 or 0.99

Relationship:
Confidence Level = 1 - Significance Level

α = 0.05 → 95% confidence interval
α = 0.01 → 99% confidence interval
```

**Connection:**
```
Hypothesis test at α = 0.05:
Reject H₀: μ = μ₀ if μ₀ outside 95% CI

The (1-α) CI contains all μ₀ values
that would NOT be rejected at level α

They are mathematically equivalent:
- 95% CI for μ excludes μ₀
- ⟺ p-value < 0.05 for testing H₀: μ = μ₀
```

