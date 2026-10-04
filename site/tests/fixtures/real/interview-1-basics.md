# 1. Fundamentals & Learning Paradigms

## Key Concepts

### 1.1 Supervised vs Unsupervised vs Reinforcement Learning

These are the three main paradigms of machine learning, distinguished by the type of feedback available during training.

#### Supervised Learning
The model learns from labeled data—each input has a corresponding target output.

- **Goal**: Learn a mapping function f(x) → y from input features to known labels
- **Training signal**: Direct error between prediction and ground truth
- **Examples**: 
  - Classification: spam detection, image recognition, sentiment analysis
  - Regression: house price prediction, stock forecasting

```
Input: Image of a cat → Label: "cat"
Model learns: features that distinguish cats from other objects
```

#### Unsupervised Learning
The model discovers patterns in data without explicit labels.

- **Goal**: Find hidden structure, patterns, or representations in data
- **Training signal**: Internal metrics (reconstruction error, cluster cohesion, etc.)
- **Examples**:
  - Clustering: customer segmentation, document grouping (K-means, DBSCAN)
  - Dimensionality reduction: PCA, t-SNE, autoencoders
  - Density estimation: anomaly detection
  - Association: market basket analysis

```
Input: Customer purchase history (no labels)
Model learns: natural groupings of similar customers
```

#### Reinforcement Learning
The model learns through interaction with an environment, receiving rewards or penalties.

- **Goal**: Learn a policy π(s) → a that maximizes cumulative reward
- **Training signal**: Delayed, sparse rewards from environment
- **Key components**:
  - Agent: the learner/decision maker
  - Environment: what the agent interacts with
  - State: current situation
  - Action: choices available to agent
  - Reward: feedback signal
- **Examples**: game playing (AlphaGo), robotics, autonomous vehicles, recommendation systems

```
Agent: Robot arm
State: Current position of arm and object
Action: Move joint by X degrees
Reward: +1 if object picked up, 0 otherwise
```

#### Comparison Table

| Aspect | Supervised | Unsupervised | Reinforcement |
|--------|-----------|--------------|---------------|
| Labels | Required | Not required | Rewards (delayed) |
| Feedback | Immediate, per sample | None (internal metrics) | Delayed, sparse |
| Goal | Predict labels | Find structure | Maximize reward |
| Data | (x, y) pairs | x only | (s, a, r, s') tuples |

---

### 1.2 Parametric vs Non-parametric Models

This distinction is about how model complexity scales with data.

#### Parametric Models
Have a **fixed number of parameters** regardless of training data size.

- **Characteristics**:
  - Model complexity is bounded
  - Faster inference (constant time)
  - Strong assumptions about data distribution
  - May underfit if assumptions are wrong
  - Lower memory footprint

- **Examples**:
  - Linear Regression: parameters = weights for each feature + bias
  - Logistic Regression: same as linear, fixed by feature count
  - Neural Networks: fixed architecture determines parameter count
  - Naive Bayes: parameters for class priors and feature likelihoods
  - Linear SVM: weight vector in feature space

```python
# Linear regression: always d+1 parameters (d features + bias)
# Regardless if you have 100 or 1 million training samples
y = w0 + w1*x1 + w2*x2 + ... + wd*xd
```

#### Non-parametric Models
Model complexity **grows with training data**. "Non-parametric" doesn't mean "no parameters"—it means the number of parameters is not fixed in advance.

- **Characteristics**:
  - More flexible, fewer assumptions
  - Can capture complex patterns
  - Slower inference (often O(n) or worse)
  - Higher memory requirements (may store training data)
  - Less prone to underfitting, more prone to overfitting

- **Examples**:
  - K-Nearest Neighbors: stores all training points
  - Decision Trees: depth/nodes grow with data complexity
  - Kernel SVM: support vectors scale with data
  - Gaussian Processes: covariance matrix grows with n²
  - Random Forests: ensemble of trees

```python
# KNN: must store and compare against all n training points
# Inference time: O(n * d) for n samples, d features
prediction = majority_vote(k_nearest_neighbors(query, all_training_data))
```

#### Comparison Table

| Aspect | Parametric | Non-parametric |
|--------|-----------|----------------|
| Parameters | Fixed | Grows with data |
| Assumptions | Strong | Weak |
| Flexibility | Limited | High |
| Inference speed | Fast (O(1)) | Slow (O(n)) |
| Memory | Low | High |
| Risk | Underfitting | Overfitting |

---

### 1.3 Generative vs Discriminative Models

This distinction is about **what the model learns** about the data.

#### Discriminative Models
Learn the **decision boundary** directly—model P(y|x).

- **Goal**: Directly predict the label given features
- **What they learn**: How to separate classes
- **Advantages**:
  - Often more accurate for classification (directly optimizing for the task)
  - Simpler to train
  - Need less data for good performance
- **Disadvantages**:
  - Can't generate new samples
  - Can't handle missing features well
  - No insight into data distribution

- **Examples**:
  - Logistic Regression
  - SVM
  - Neural Networks (most)
  - Decision Trees
  - Random Forests

```
Discriminative: "Given these features, what's the probability it's class A vs B?"
Learns: P(y|x) directly
```

#### Generative Models
Learn the **full joint distribution** P(x, y) or P(x)—model how the data was generated.

- **Goal**: Model the underlying data distribution
- **What they learn**: P(x|y) and P(y), then use Bayes' rule: P(y|x) = P(x|y)P(y) / P(x)
- **Advantages**:
  - Can generate new samples
  - Handle missing data naturally
  - Provide insight into data structure
  - Can detect outliers
- **Disadvantages**:
  - Often less accurate for pure classification
  - More complex to train
  - Need more data

- **Examples**:
  - Naive Bayes
  - Gaussian Mixture Models (GMM)
  - Hidden Markov Models (HMM)
  - Variational Autoencoders (VAE)
  - Generative Adversarial Networks (GAN)
  - Diffusion Models
  - Large Language Models (GPT, etc.)

```
Generative: "What does data from class A typically look like? Class B?"
Learns: P(x|y) for each class, then applies Bayes' rule
```

#### Visual Intuition

```
Discriminative:                    Generative:
   Class A    |    Class B            Class A         Class B
     ●●●      |      ○○○              (●●●)           (○○○)
    ●●●●●     |     ○○○○○            (●●●●●)         (○○○○○)
     ●●●      |      ○○○              (●●●)           (○○○)
              ↑                         ↑               ↑
        Decision boundary         Model each class distribution
```

#### Comparison Table

| Aspect | Discriminative | Generative |
|--------|---------------|------------|
| Models | P(y\|x) | P(x,y) or P(x) |
| Goal | Classification boundary | Data distribution |
| Can generate samples | No | Yes |
| Missing features | Problematic | Handled naturally |
| Training data needed | Less | More |
| Classification accuracy | Often higher | Often lower |

---

### 1.4 Inductive Bias

**Inductive bias** refers to the set of assumptions a learning algorithm makes to generalize from training data to unseen data.

#### Why It's Necessary
Without inductive bias, learning is impossible. Given finite training data, infinitely many hypotheses could explain the data perfectly. Inductive bias constrains the hypothesis space to make learning tractable.

```
Training data: (1,2), (2,4), (3,6)
Possible hypotheses:
  - y = 2x (linear)
  - y = 2x + sin(2πx) (also fits perfectly!)
  - Infinitely many others...

Inductive bias (e.g., "prefer simpler functions") → choose y = 2x
```

#### Types of Inductive Bias

1. **Restriction bias**: Limits the hypothesis space
   - Linear models assume linear relationships
   - Decision trees assume axis-aligned splits

2. **Preference bias**: Ranks hypotheses within the space
   - Occam's Razor: prefer simpler hypotheses
   - Regularization: prefer smaller weights

#### Examples of Inductive Bias

| Algorithm | Inductive Bias |
|-----------|---------------|
| Linear Regression | Relationship is linear; features are independent |
| KNN | Similar inputs have similar outputs; local smoothness |
| Decision Trees | Features can be split independently; axis-aligned boundaries |
| CNN | Spatial locality matters; translation invariance |
| RNN/LSTM | Sequential/temporal dependencies matter |
| Transformers | Attention patterns capture relationships; position matters |

#### The Bias-Variance Tradeoff Connection
- **Strong inductive bias** → Lower variance, higher bias (may underfit)
- **Weak inductive bias** → Higher variance, lower bias (may overfit)

The "No Free Lunch" theorem states that no algorithm is universally best—the right inductive bias depends on the problem domain.

---

## Questions & Answers

### ⭐ Q1: What are the differences between supervised, unsupervised, and reinforcement learning?

**Answer:**

The three paradigms differ in their learning signal and objective:

**Supervised Learning:**
- Learns from labeled examples (input-output pairs)
- Receives immediate feedback on every prediction
- Objective: minimize prediction error on known labels
- Use when: you have labeled data and want to predict labels for new data

**Unsupervised Learning:**
- Learns from unlabeled data
- No external feedback; uses internal metrics
- Objective: discover hidden structure (clusters, patterns, representations)
- Use when: you want to understand data structure, reduce dimensionality, or find anomalies

**Reinforcement Learning:**
- Learns through trial-and-error interaction with environment
- Receives delayed, sparse reward signals
- Objective: maximize cumulative reward over time
- Use when: sequential decision-making with delayed consequences

**Key insight for interviews:** The fundamental difference is the feedback mechanism—supervised gets direct labels, unsupervised gets none, and RL gets delayed rewards that require credit assignment across actions.

---

### Q2: What is the difference between parametric and non-parametric models? Give examples.

**Answer:**

**Parametric models** have a fixed number of parameters determined before training:
- Complexity is bounded regardless of data size
- Make strong assumptions about data distribution
- Fast inference, low memory
- Examples: Linear/Logistic Regression, Neural Networks, Naive Bayes

**Non-parametric models** have complexity that grows with training data:
- Number of "parameters" scales with dataset size
- Make fewer assumptions, more flexible
- Slower inference, higher memory (often store training data)
- Examples: KNN, Decision Trees, Kernel SVM, Gaussian Processes

**Common misconception:** "Non-parametric" doesn't mean "no parameters." It means the number of effective parameters isn't fixed in advance.

**Trade-off:** Parametric models risk underfitting (too rigid), while non-parametric models risk overfitting (too flexible) and computational cost.

---

### Q3: What is inductive bias? Why is it important?

**Answer:**

**Inductive bias** is the set of assumptions an algorithm uses to generalize beyond training data.

**Why it's essential:**
1. **Makes learning possible:** Without bias, infinite hypotheses fit any finite dataset
2. **Enables generalization:** Constrains the model to prefer certain solutions
3. **Encodes domain knowledge:** CNNs assume spatial locality; RNNs assume temporal dependencies

**Examples:**
- Linear regression assumes linear relationships
- KNN assumes local smoothness (nearby points are similar)
- Neural networks with specific architectures encode structural assumptions

**The key insight:** There's no "unbiased" learner. The goal is to choose inductive biases that match your problem domain. This is why CNNs work well for images (spatial structure) but RNNs work better for sequences (temporal structure).

---

### Q4: When would you use a generative model vs a discriminative model?

**Answer:**

**Use Discriminative Models when:**
- Primary goal is classification/prediction accuracy
- You have sufficient labeled data
- You don't need to generate new samples
- Computational efficiency matters
- Examples: spam detection, image classification, sentiment analysis

**Use Generative Models when:**
- You need to generate new samples (images, text, audio)
- Handling missing or partial data is important
- You want to understand the data distribution
- Outlier/anomaly detection is needed
- Semi-supervised learning (limited labels, lots of unlabeled data)
- Examples: image synthesis (GANs, diffusion), text generation (LLMs), data augmentation

**Practical guidance:**
- For pure classification with clean data → discriminative (often more accurate)
- For generation, missing data, or understanding data → generative
- Modern trend: large generative models (LLMs) can be adapted for discriminative tasks through fine-tuning or prompting

**Interview tip:** Mention that discriminative models directly optimize for the classification objective, which often leads to better classification performance, but generative models provide richer understanding of the data and enable capabilities like generation and handling missing features.
