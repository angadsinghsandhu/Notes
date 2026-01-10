# 5. Probabilistic Models

---

## Key Concepts

### 5.1 Probabilistic Graphical Models Overview

Graphical models represent joint probability distributions using graphs.

```
                Probabilistic Graphical Models
                            |
            ┌───────────────┼───────────────┐
            |               |               |
      Directed          Undirected       Hybrid
   (Bayesian Networks)  (Markov Random   (Chain Graphs)
            |            Fields)
            |               |
    Causal reasoning    Spatial/image
    Generative models   Sequence labeling
```

#### Why Graphical Models?

```
Joint distribution over d variables:
- Naive: O(k^d) parameters (k values each)
- With independence: O(d * k^2) or less

Graphs encode conditional independence assumptions
→ Compact representation
→ Efficient inference
```

---

### 5.2 Bayesian Networks

Directed acyclic graphs (DAGs) representing causal/generative relationships.

#### Structure

```
Example: Student Performance

    Difficulty ──→ Grade ←── Intelligence
                     ↓
                   Letter
                     ↓
                   Job Offer

Nodes = random variables
Edges = direct dependencies
```

#### Joint Distribution

```
P(X_1, X_2, ..., X_n) = ∏_i P(X_i | Parents(X_i))

Example:
P(D, I, G, L, J) = P(D) * P(I) * P(G|D,I) * P(L|G) * P(J|L)

Each node only depends on its parents!
```

#### Conditional Independence

```
D-separation rules determine independence:

1. Chain: A → B → C
   A ⊥ C | B  (A independent of C given B)

2. Fork: A ← B → C
   A ⊥ C | B

3. Collider: A → B ← C
   A ⊥ C (marginally)
   A ⊥̸ C | B (NOT independent given B!)
```

#### Inference

**Goal:** Compute P(Query | Evidence)

```
Exact inference:
- Variable elimination
- Belief propagation (message passing)
- Junction tree algorithm

Approximate inference:
- Monte Carlo sampling
- Variational inference
```

#### Learning

```
Structure known:
- MLE: count frequencies from data
- Bayesian: add prior (Dirichlet)

Structure unknown:
- Score-based: search + BIC/AIC
- Constraint-based: test independencies
```

---

### 5.3 Markov Models

#### Markov Chains

Sequence model where future depends only on present.

```
State diagram:
        0.7
    ┌────────┐
    ↓        |
  [Sunny] ──0.3──→ [Rainy]
    ↑               |
    └────0.4────────┘
           0.6
         ┌────┐
         ↓    |
```

**Markov Property:**
```
P(X_t | X_{t-1}, X_{t-2}, ..., X_1) = P(X_t | X_{t-1})

Future independent of past given present
```

**Transition Matrix:**
```
        Sunny  Rainy
Sunny   [0.7   0.3]
Rainy   [0.4   0.6]

P(X_{t+1} = j | X_t = i) = T_ij
```

**Stationary Distribution:**
```
π * T = π

Long-run probability of being in each state
Solve: (T^T - I) * π = 0, sum(π) = 1
```

#### Hidden Markov Models (HMM)

States are hidden; we observe emissions.

```
Hidden states:    S_1 ──→ S_2 ──→ S_3 ──→ S_4
                   ↓       ↓       ↓       ↓
Observations:     O_1     O_2     O_3     O_4
```

**Parameters:**
```
- π: initial state distribution
- A: transition matrix P(S_t | S_{t-1})
- B: emission matrix P(O_t | S_t)
```

**Three Problems:**

| Problem | Algorithm | Complexity |
|---------|-----------|------------|
| Likelihood P(O\|λ) | Forward algorithm | O(T * N^2) |
| Decoding argmax P(S\|O) | Viterbi algorithm | O(T * N^2) |
| Learning λ | Baum-Welch (EM) | O(T * N^2) per iter |

**Forward Algorithm:**
```
α_t(i) = P(O_1, ..., O_t, S_t = i)

α_1(i) = π_i * B_i(O_1)
α_t(j) = [sum_i α_{t-1}(i) * A_ij] * B_j(O_t)

P(O) = sum_i α_T(i)
```

**Viterbi Algorithm:**
```
δ_t(i) = max probability of path ending in state i at time t

δ_1(i) = π_i * B_i(O_1)
δ_t(j) = max_i [δ_{t-1}(i) * A_ij] * B_j(O_t)

Backtrack to find best path
```

**Applications:**
```
- Speech recognition
- POS tagging
- Gene finding
- Gesture recognition
```

---

### 5.4 EM Algorithm (Expectation-Maximization)

Iterative algorithm for MLE with latent variables.

#### The Problem

```
Want to maximize: log P(X | θ)

But: X depends on hidden variables Z
     P(X | θ) = sum_Z P(X, Z | θ)

Direct optimization is hard (sum inside log)
```

#### EM Solution

**E-step (Expectation):**
```
Compute expected value of complete-data log-likelihood
using current parameter estimate θ^(t)

Q(θ | θ^(t)) = E_{Z|X,θ^(t)} [log P(X, Z | θ)]
```

**M-step (Maximization):**
```
Find θ that maximizes Q

θ^(t+1) = argmax_θ Q(θ | θ^(t))
```

**Repeat until convergence.**

#### Why EM Works

```
EM guarantees: log P(X | θ^(t+1)) >= log P(X | θ^(t))

Likelihood never decreases!
Converges to local maximum.
```

**Proof sketch:**
```
log P(X|θ) = L(q, θ) + KL(q || P(Z|X,θ))

Where L is the ELBO (Evidence Lower Bound)
KL >= 0, so log P(X|θ) >= L(q, θ)

E-step: set q = P(Z|X,θ^(t)), makes KL = 0
M-step: maximize L over θ
```

#### Example: GMM

**E-step:**
```
Compute responsibilities (soft assignments):

γ_ik = P(z_i = k | x_i, θ^(t))
     = (π_k * N(x_i | μ_k, Σ_k)) / sum_j (π_j * N(x_i | μ_j, Σ_j))
```

**M-step:**
```
Update parameters:

N_k = sum_i γ_ik
π_k = N_k / N
μ_k = sum_i (γ_ik * x_i) / N_k
Σ_k = sum_i (γ_ik * (x_i - μ_k)(x_i - μ_k)^T) / N_k
```

#### EM Properties

| Property | Description |
|----------|-------------|
| Monotonic | Likelihood never decreases |
| Convergence | To local maximum (not global) |
| Initialization | Sensitive, run multiple times |
| Speed | Can be slow near convergence |
| Variants | Hard EM, variational EM |

---

### 5.5 Latent Dirichlet Allocation (LDA)

Probabilistic topic model for document collections.

#### Intuition

```
Document = mixture of topics
Topic = distribution over words

Document: "The player scored a goal in the match"
- 70% Sports topic
- 20% Competition topic  
- 10% General topic

Sports topic: {player: 0.1, goal: 0.08, match: 0.05, ...}
```

#### Generative Process

```
For each topic k:
    Draw word distribution φ_k ~ Dirichlet(β)

For each document d:
    Draw topic distribution θ_d ~ Dirichlet(α)
    For each word position n:
        Draw topic z_dn ~ Categorical(θ_d)
        Draw word w_dn ~ Categorical(φ_{z_dn})
```

**Plate Notation:**
```
    ┌─────────────────────────────┐
    │  α → θ_d → z_dn → w_dn     │
    │              ↑              │  D documents
    │         ┌────┴────┐        │
    │         │  φ_k ← β │  K    │
    │         └─────────┘        │
    └─────────────────────────────┘
```

#### Inference

```
Goal: Infer θ (document-topic) and φ (topic-word) from observed words

Methods:
- Variational inference (mean-field)
- Collapsed Gibbs sampling
- Online variational Bayes (for large corpora)
```

**Collapsed Gibbs Sampling:**
```
For each word w_dn:
    Remove current topic assignment
    Sample new topic:
    P(z_dn = k | z_{-dn}, w) ∝ 
        (n_{dk} + α) * (n_{kw} + β) / (n_k + V*β)
    
    Where:
    - n_{dk} = count of topic k in document d
    - n_{kw} = count of word w in topic k
    - n_k = total words in topic k
```

#### Hyperparameters

| Parameter | Effect |
|-----------|--------|
| α (doc-topic) | Small: documents have few topics |
| β (topic-word) | Small: topics have few words |
| K (num topics) | More topics = finer granularity |

---

### 5.6 Monte Carlo Methods

Use random sampling to estimate quantities.

#### Basic Monte Carlo

```
Estimate E[f(X)] where X ~ P(X):

1. Sample X_1, X_2, ..., X_n from P(X)
2. Estimate: E[f(X)] ≈ (1/n) * sum_i f(X_i)

Law of Large Numbers: converges to true expectation
Variance: O(1/n) regardless of dimension!
```

#### Importance Sampling

When P(X) is hard to sample from:

```
E_P[f(X)] = E_Q[f(X) * P(X)/Q(X)]
          = E_Q[f(X) * w(X)]

Where w(X) = P(X)/Q(X) is importance weight

Sample from easy Q, reweight by w
```

#### Markov Chain Monte Carlo (MCMC)

Construct Markov chain with stationary distribution = target P(X).

**Metropolis-Hastings:**
```
1. Start at X_0
2. For t = 1, 2, ...:
   a. Propose X' ~ Q(X' | X_t)
   b. Compute acceptance ratio:
      α = min(1, P(X')*Q(X_t|X') / P(X_t)*Q(X'|X_t))
   c. Accept X_{t+1} = X' with probability α
      Otherwise X_{t+1} = X_t
```

**Properties:**
```
- Detailed balance: P(X)*Q(X'|X)*α = P(X')*Q(X|X')*α'
- Stationary distribution is P(X)
- Samples are correlated (not independent)
- Need burn-in period
```

#### Gibbs Sampling

Special case of MCMC: sample each variable from conditional.

```
For variables X = (X_1, X_2, ..., X_d):

Repeat:
    X_1 ~ P(X_1 | X_2, X_3, ..., X_d)
    X_2 ~ P(X_2 | X_1, X_3, ..., X_d)
    ...
    X_d ~ P(X_d | X_1, X_2, ..., X_{d-1})
```

**Advantages:**
```
- No rejection (always accept)
- No tuning of proposal distribution
- Natural for graphical models (conditionals easy)
```

**Disadvantages:**
```
- Can be slow if variables highly correlated
- Need closed-form conditionals
```

---

### 5.7 Information Theory Concepts

#### Entropy

```
H(X) = -sum_x P(x) * log P(x)
     = E[-log P(X)]

Measures uncertainty/information content
Units: bits (log base 2) or nats (natural log)

Maximum entropy: uniform distribution
Minimum entropy: deterministic (H = 0)
```

#### Cross-Entropy

```
H(P, Q) = -sum_x P(x) * log Q(x)
        = E_P[-log Q(X)]

Expected bits to encode P using code optimized for Q
Always >= H(P) (equality when P = Q)
```

#### KL Divergence

```
KL(P || Q) = sum_x P(x) * log(P(x) / Q(x))
           = H(P, Q) - H(P)
           = E_P[log P(X) - log Q(X)]

"Extra bits" needed when using Q instead of P
```

**Properties:**
```
- KL(P || Q) >= 0 (Gibbs' inequality)
- KL(P || Q) = 0 iff P = Q
- NOT symmetric: KL(P || Q) ≠ KL(Q || P)
- NOT a distance (no triangle inequality)
```

#### Mutual Information

```
I(X; Y) = KL(P(X,Y) || P(X)P(Y))
        = H(X) - H(X|Y)
        = H(Y) - H(Y|X)

Information shared between X and Y
I(X; Y) = 0 iff X and Y are independent
```

---

### 5.8 MLE vs Bayesian Inference

#### Maximum Likelihood Estimation (MLE)

```
θ_MLE = argmax_θ P(D | θ)
      = argmax_θ ∏_i P(x_i | θ)
      = argmax_θ sum_i log P(x_i | θ)

Point estimate: single "best" θ
```

**Example: Coin flips**
```
Data: H, H, T, H (3 heads, 1 tail)
θ = probability of heads

L(θ) = θ^3 * (1-θ)^1
log L(θ) = 3*log(θ) + 1*log(1-θ)

d/dθ: 3/θ - 1/(1-θ) = 0
θ_MLE = 3/4 = 0.75
```

#### Bayesian Inference

```
P(θ | D) = P(D | θ) * P(θ) / P(D)
         ∝ P(D | θ) * P(θ)

posterior ∝ likelihood × prior

Full distribution over θ, not just point estimate
```

**Example: Coin flips with Beta prior**
```
Prior: θ ~ Beta(α, β)
Likelihood: Binomial(n, k | θ)
Posterior: θ | D ~ Beta(α + k, β + n - k)

With α = β = 1 (uniform prior), k = 3, n = 4:
Posterior: Beta(4, 2)
Mean = 4/6 = 0.67 (shrunk toward 0.5)
```

#### MAP Estimation

```
θ_MAP = argmax_θ P(θ | D)
      = argmax_θ P(D | θ) * P(θ)

Point estimate like MLE, but includes prior
Regularization interpretation: prior = regularizer
```

#### Comparison

| Aspect | MLE | Bayesian | MAP |
|--------|-----|----------|-----|
| Output | Point estimate | Distribution | Point estimate |
| Prior | None | Required | Required |
| Uncertainty | No | Yes | No |
| Computation | Often easy | Can be hard | Often easy |
| Small data | Overfits | Regularized | Regularized |
| Interpretation | Frequentist | Bayesian | Hybrid |

---

## Questions & Answers

### Q1: How does the EM algorithm work?

**Answer:**

EM is an iterative algorithm for maximum likelihood estimation when there are latent (hidden) variables.

**The Problem:**
```
Want: θ* = argmax_θ log P(X | θ)

But: P(X | θ) = sum_Z P(X, Z | θ)

Sum inside log makes direct optimization hard
```

**EM Solution:**

**E-step (Expectation):**
```
Compute posterior over latent variables given current θ:
q(Z) = P(Z | X, θ^(t))

Compute expected complete-data log-likelihood:
Q(θ | θ^(t)) = E_q [log P(X, Z | θ)]
```

**M-step (Maximization):**
```
Update parameters to maximize Q:
θ^(t+1) = argmax_θ Q(θ | θ^(t))
```

**Why It Works:**
```
Each iteration increases (or maintains) likelihood
Converges to local maximum

Intuition:
- E-step: "If I knew θ, what are the hidden variables?"
- M-step: "If I knew hidden variables, what's the best θ?"
```

**GMM Example:**
```
E-step: Compute responsibility γ_ik = P(point i from cluster k)
M-step: Update μ_k, Σ_k, π_k using weighted statistics
```

**Properties:**
- Guaranteed to converge (monotonic likelihood)
- May find local, not global, maximum
- Sensitive to initialization
- Can be slow near convergence

---

### ⭐ Q2: How is KL divergence different from cross-entropy loss?

**Answer:**

**Definitions:**

```
Cross-Entropy:
H(P, Q) = -sum_x P(x) * log Q(x)

KL Divergence:
KL(P || Q) = sum_x P(x) * log(P(x) / Q(x))
           = -sum_x P(x) * log Q(x) + sum_x P(x) * log P(x)
           = H(P, Q) - H(P)
```

**Key Relationship:**
```
KL(P || Q) = H(P, Q) - H(P)
           = Cross-Entropy - Entropy of P

When P is fixed (true distribution):
H(P) is constant, so minimizing KL ≡ minimizing cross-entropy
```

**In Machine Learning:**

```
Classification:
- P = true labels (one-hot): [0, 0, 1, 0]
- Q = model predictions: [0.1, 0.2, 0.6, 0.1]

Cross-entropy loss:
L = -sum_i y_i * log(q_i) = -log(0.6)

Since P is one-hot, H(P) = 0
So: KL(P || Q) = H(P, Q) - 0 = H(P, Q)

Cross-entropy and KL are equivalent for one-hot labels!
```

**Differences:**

| Aspect | Cross-Entropy | KL Divergence |
|--------|---------------|---------------|
| Formula | H(P,Q) = -E_P[log Q] | KL = H(P,Q) - H(P) |
| Range | [H(P), ∞) | [0, ∞) |
| Minimum | H(P) when Q = P | 0 when Q = P |
| Symmetry | No | No |
| Use in ML | Loss function | Regularization, VAE |

**When They Differ:**

```
Soft labels (label smoothing, distillation):
P = [0.1, 0.1, 0.7, 0.1]  (not one-hot)
H(P) ≠ 0

Now KL and cross-entropy differ by constant H(P)
For optimization: still equivalent (same gradient)
For comparison: KL is normalized (min = 0)
```

**Practical Usage:**
```
- Classification loss: Cross-entropy (simpler)
- VAE: KL divergence (regularize latent space)
- Distillation: Cross-entropy with soft targets
- Comparing distributions: KL (interpretable as "extra bits")
```

---

### Q3: What are the differences between cross-entropy loss and contrastive loss?

**Answer:**

**Cross-Entropy Loss:**
```
L_CE = -sum_i y_i * log(p_i)

For classification:
- Compares predicted distribution to true labels
- Operates on single sample
- Requires explicit class labels
```

**Contrastive Loss:**
```
L_contrastive = (1-y) * D^2 + y * max(0, margin - D)^2

Where:
- D = distance between embeddings
- y = 1 if different class, 0 if same class
- margin = minimum distance for different classes

Operates on PAIRS of samples
```

**Triplet Loss (related):**
```
L_triplet = max(0, D(anchor, positive) - D(anchor, negative) + margin)

Operates on TRIPLETS: anchor, positive, negative
Push negatives away, pull positives closer
```

**Key Differences:**

| Aspect | Cross-Entropy | Contrastive/Triplet |
|--------|---------------|---------------------|
| Input | Single sample + label | Pairs/triplets |
| Output | Class probabilities | Embeddings |
| Goal | Classify correctly | Learn similarity |
| Labels | Class labels | Same/different |
| Use case | Classification | Retrieval, face recognition |

**When to Use Each:**

```
Cross-Entropy:
- Fixed set of classes
- Standard classification
- Enough labeled data per class

Contrastive/Triplet:
- Many classes (face recognition: millions of people)
- Few examples per class
- Similarity/retrieval tasks
- Transfer learning (learn general embeddings)
```

**Modern Alternatives:**

```
InfoNCE (used in SimCLR, CLIP):
L = -log(exp(sim(z_i, z_j)/τ) / sum_k exp(sim(z_i, z_k)/τ))

Combines ideas from both:
- Softmax-like normalization (cross-entropy style)
- Operates on positive/negative pairs (contrastive style)
```

---

### ⭐ Q4: When would you use Bayesian inference vs MLE?

**Answer:**

**Use MLE when:**

```
1. Large dataset
   - Prior becomes negligible
   - MLE ≈ MAP ≈ Bayesian mean
   
2. Computational constraints
   - MLE is often closed-form or easy optimization
   - Bayesian may need MCMC/variational inference

3. Point estimate sufficient
   - Don't need uncertainty quantification
   - Just want best single prediction

4. No prior knowledge
   - Uninformative prior → MLE anyway
   - Prior might introduce bias
```

**Use Bayesian when:**

```
1. Small dataset
   - Prior regularizes, prevents overfitting
   - Uncertainty estimates are meaningful

2. Need uncertainty quantification
   - Medical diagnosis: "80% confident"
   - Decision making under uncertainty
   - Active learning (explore uncertain regions)

3. Have informative prior
   - Domain knowledge to incorporate
   - Previous experiments/studies

4. Sequential updating
   - Online learning: posterior becomes next prior
   - Natural framework for updating beliefs

5. Model comparison
   - Bayesian model selection
   - Automatic Occam's razor
```

**Comparison:**

| Scenario | MLE | Bayesian |
|----------|-----|----------|
| 1000+ samples | ✓ | Either |
| 10-100 samples | Overfits | ✓ |
| Need confidence intervals | Bootstrap | ✓ (natural) |
| Real-time prediction | ✓ (fast) | Depends |
| Interpretable uncertainty | No | ✓ |
| Prior knowledge available | Ignored | ✓ |

**Practical Middle Ground:**

```
MAP estimation:
- Point estimate like MLE
- Includes prior (regularization)
- L2 regularization = Gaussian prior
- L1 regularization = Laplace prior

Often best of both worlds for prediction tasks
```

---

### Q5: Explain Gibbs sampling and when to use it.

**Answer:**

**What is Gibbs Sampling:**

```
MCMC method that samples each variable from its conditional distribution.

For X = (X_1, X_2, ..., X_d):

Initialize X^(0)
For t = 1, 2, ...:
    X_1^(t) ~ P(X_1 | X_2^(t-1), X_3^(t-1), ..., X_d^(t-1))
    X_2^(t) ~ P(X_2 | X_1^(t), X_3^(t-1), ..., X_d^(t-1))
    ...
    X_d^(t) ~ P(X_d | X_1^(t), X_2^(t), ..., X_{d-1}^(t))
```

**Why It Works:**
```
- Special case of Metropolis-Hastings with acceptance = 1
- Satisfies detailed balance
- Stationary distribution is target P(X)
- After burn-in, samples approximate P(X)
```

**When to Use:**

```
1. Conditionals are easy to sample
   - Conjugate priors in Bayesian models
   - Graphical models (local structure)

2. High-dimensional problems
   - Sample one variable at a time
   - Avoid curse of dimensionality in proposals

3. Graphical models
   - LDA topic models
   - Bayesian networks
   - Markov random fields
```

**Advantages:**
```
- No rejection (always accept)
- No tuning of proposal distribution
- Natural for structured models
```

**Disadvantages:**
```
- Slow mixing if variables highly correlated
- Need closed-form conditionals
- Sequential (hard to parallelize)
```

**Example: LDA Topic Model**
```
For each word w in document d:
    Sample topic z ~ P(z | z_{-}, w, d)
    
Conditional is easy:
P(z = k) ∝ (count of k in doc + α) × (count of w in topic k + β)
```

---

### Q6: What is the difference between generative and discriminative models?

**Answer:**

**Discriminative Models:**
```
Model P(Y | X) directly

"Given features, what's the label?"

Examples:
- Logistic regression
- SVM
- Neural networks (most)
- CRF
```

**Generative Models:**
```
Model P(X, Y) = P(X | Y) * P(Y)

"How is the data generated?"

Use Bayes' rule for classification:
P(Y | X) = P(X | Y) * P(Y) / P(X)

Examples:
- Naive Bayes
- GMM
- HMM
- LDA
- VAE, GAN
```

**Comparison:**

| Aspect | Discriminative | Generative |
|--------|----------------|------------|
| Models | P(Y\|X) | P(X,Y) or P(X) |
| Goal | Decision boundary | Data distribution |
| Classification | Often better | May be worse |
| Missing data | Problematic | Natural handling |
| Outlier detection | Hard | Natural |
| Sample generation | No | Yes |
| Training data | Less needed | More needed |

**When to Use Each:**

```
Discriminative:
- Classification is the only goal
- Have enough labeled data
- Want best accuracy

Generative:
- Need to generate new samples
- Handle missing features
- Detect outliers/anomalies
- Semi-supervised learning
- Understand data structure
```

**Hybrid Approaches:**
```
- Use generative model for data augmentation
- Train discriminative model on augmented data
- Best of both worlds
```

