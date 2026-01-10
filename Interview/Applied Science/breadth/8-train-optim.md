# 8. Training & Optimization

---

## Key Concepts

### 8.1 Loss Functions

Loss functions measure how well the model's predictions match the targets.

#### Regression Losses

**Mean Squared Error (MSE):**
```
L = (1/n) * sum((y_i - ŷ_i)^2)

Properties:
- Penalizes large errors heavily (squared)
- Sensitive to outliers
- Gradient: 2(ŷ - y)
- Use when: Gaussian noise assumption
```

**Mean Absolute Error (MAE):**
```
L = (1/n) * sum(|y_i - ŷ_i|)

Properties:
- Robust to outliers
- Non-differentiable at 0
- Gradient: sign(ŷ - y)
- Use when: Outliers present
```

**Huber Loss (Smooth L1):**
```
L = { 0.5 * (y - ŷ)^2        if |y - ŷ| < δ
    { δ * |y - ŷ| - 0.5*δ^2  otherwise

Properties:
- MSE for small errors, MAE for large
- Best of both worlds
- Differentiable everywhere
```

#### Classification Losses

**Binary Cross-Entropy:**
```
L = -(1/n) * sum(y*log(p) + (1-y)*log(1-p))

Where p = sigmoid(logit)

Properties:
- Derived from maximum likelihood
- Penalizes confident wrong predictions heavily
- Gradient: p - y (simple!)
```

**Categorical Cross-Entropy:**
```
L = -(1/n) * sum_i sum_k y_ik * log(p_ik)

Where p = softmax(logits)

For one-hot labels: L = -log(p_correct)
```

**Focal Loss:**
```
L = -α * (1 - p)^γ * log(p)

Properties:
- Down-weights easy examples
- Focuses on hard examples
- γ = 0: standard cross-entropy
- Use when: Class imbalance
```

**Hinge Loss (SVM):**
```
L = max(0, 1 - y * f(x))

Where y ∈ {-1, +1}

Properties:
- Margin-based
- Not differentiable at 1
- Use when: Maximum margin desired
```

#### Metric Learning Losses

**Contrastive Loss:**
```
L = (1-y) * D^2 + y * max(0, margin - D)^2

Where:
- D = distance between embeddings
- y = 1 if different class, 0 if same

Pull similar pairs together, push different apart
```

**Triplet Loss:**
```
L = max(0, D(anchor, positive) - D(anchor, negative) + margin)

Properties:
- Operates on triplets
- Relative distances matter
- Hard negative mining important
```


**InfoNCE Loss (Contrastive Learning):**
```
L = -log(exp(sim(z_i, z_j)/τ) / sum_k exp(sim(z_i, z_k)/τ))

Where:
- z_i, z_j = positive pair
- z_k = all samples (including negatives)
- τ = temperature

Used in: SimCLR, CLIP, MoCo
```

#### Loss Function Selection

| Task | Loss | When to Use |
|------|------|-------------|
| Regression | MSE | Gaussian errors, no outliers |
| Regression | MAE | Outliers present |
| Regression | Huber | Balanced robustness |
| Binary classification | BCE | Standard binary |
| Multi-class | Cross-entropy | Standard multi-class |
| Imbalanced | Focal loss | Rare class detection |
| Similarity | Triplet/Contrastive | Retrieval, face recognition |

---

### 8.2 Gradient Descent Variants

#### Batch Gradient Descent

```
θ = θ - α * (1/n) * sum_i ∇L(x_i, y_i; θ)

Use ALL training data for each update

Pros:
- Stable convergence
- True gradient direction

Cons:
- Slow for large datasets
- Memory intensive
- Can't escape local minima
```

#### Stochastic Gradient Descent (SGD)

```
For each sample (x_i, y_i):
    θ = θ - α * ∇L(x_i, y_i; θ)

Use ONE sample per update

Pros:
- Fast updates
- Can escape local minima (noise)
- Online learning possible

Cons:
- High variance
- Noisy convergence
- May not converge to minimum
```

#### Mini-Batch Gradient Descent

```
For each mini-batch B:
    θ = θ - α * (1/|B|) * sum_{i∈B} ∇L(x_i, y_i; θ)

Use SUBSET of data per update (typically 32-256)

Pros:
- Balance of stability and speed
- Efficient GPU utilization
- Moderate noise (helps generalization)

Cons:
- Batch size is hyperparameter
- Memory scales with batch size
```

#### Comparison

| Aspect | Batch | Mini-Batch | Stochastic |
|--------|-------|------------|------------|
| Samples per update | All n | B (32-256) | 1 |
| Update frequency | 1/epoch | n/B per epoch | n/epoch |
| Gradient variance | 0 | Low | High |
| Memory | O(n) | O(B) | O(1) |
| GPU efficiency | High | High | Low |
| Convergence | Smooth | Moderate | Noisy |

---

### 8.3 Optimizers

#### SGD with Momentum

```
v_t = β * v_{t-1} + ∇L(θ)
θ = θ - α * v_t

β = momentum coefficient (typically 0.9)

Intuition: Ball rolling downhill accumulates velocity
- Accelerates in consistent gradient direction
- Dampens oscillations
```

**Nesterov Momentum:**
```
v_t = β * v_{t-1} + ∇L(θ - α * β * v_{t-1})
θ = θ - α * v_t

"Look ahead" before computing gradient
Faster convergence than standard momentum
```

#### AdaGrad

```
g_t = ∇L(θ)
G_t = G_{t-1} + g_t^2  (accumulated squared gradients)
θ = θ - α * g_t / (sqrt(G_t) + ε)

Properties:
- Adapts learning rate per parameter
- Large gradients → smaller updates
- Good for sparse features

Problem: Learning rate monotonically decreases
```

#### RMSprop

```
g_t = ∇L(θ)
E[g^2]_t = β * E[g^2]_{t-1} + (1-β) * g_t^2
θ = θ - α * g_t / (sqrt(E[g^2]_t) + ε)

β = decay rate (typically 0.9)

Fix AdaGrad: Use exponential moving average
Learning rate doesn't vanish
```

#### Adam (Adaptive Moment Estimation)

```
g_t = ∇L(θ)

# First moment (mean)
m_t = β_1 * m_{t-1} + (1 - β_1) * g_t

# Second moment (variance)
v_t = β_2 * v_{t-1} + (1 - β_2) * g_t^2

# Bias correction
m̂_t = m_t / (1 - β_1^t)
v̂_t = v_t / (1 - β_2^t)

# Update
θ = θ - α * m̂_t / (sqrt(v̂_t) + ε)

Default: β_1 = 0.9, β_2 = 0.999, ε = 1e-8
```

**Why Adam Works:**
```
- Momentum (m_t): accelerates in consistent direction
- Adaptive LR (v_t): per-parameter learning rates
- Bias correction: fixes initialization bias
```

#### AdamW (Adam with Weight Decay)

```
θ = θ - α * (m̂_t / (sqrt(v̂_t) + ε) + λ * θ)
                                      └────┘
                                   Decoupled weight decay

Standard Adam: L2 regularization in loss
AdamW: Weight decay separate from gradient

Better generalization, preferred for transformers
```

#### Optimizer Comparison

| Optimizer | Adaptive LR | Momentum | Best For |
|-----------|-------------|----------|----------|
| SGD | No | Optional | Convex, with tuning |
| SGD+Momentum | No | Yes | CNNs, general |
| AdaGrad | Yes | No | Sparse features |
| RMSprop | Yes | No | RNNs, non-stationary |
| Adam | Yes | Yes | Default choice |
| AdamW | Yes | Yes | Transformers |


---

### 8.4 Learning Rate Schedules

#### Why Schedule Learning Rate?

```
High LR at start: Fast progress, escape local minima
Low LR at end: Fine-tune, converge precisely

Fixed LR problems:
- Too high: oscillate, diverge
- Too low: slow, stuck in local minima
```

#### Common Schedules

**Step Decay:**
```
α_t = α_0 * γ^(floor(t / step_size))

Example: Reduce by 0.1 every 30 epochs
Simple, widely used
```

**Exponential Decay:**
```
α_t = α_0 * γ^t

Smooth continuous decay
```

**Cosine Annealing:**
```
α_t = α_min + 0.5 * (α_max - α_min) * (1 + cos(π * t / T))

Smooth decay following cosine curve
Popular for transformers
```

**Warmup:**
```
For t < warmup_steps:
    α_t = α_max * t / warmup_steps

Then: apply main schedule

Why warmup?
- Adam statistics need time to stabilize
- Prevents early large updates
- Essential for transformers
```

**Warmup + Cosine Decay:**
```
Learning Rate
    |     /\
    |    /  \
    |   /    \
    |  /      \____
    | /            \____
    |/                  \____
    └─────────────────────────── Steps
      ↑              ↑
    warmup        cosine decay
```

**One Cycle Policy:**
```
1. Warmup: increase LR to max
2. Annealing: decrease LR to min
3. Final: very low LR

Often achieves better results faster
```

#### Learning Rate Finder

```
1. Start with very small LR
2. Increase LR exponentially each batch
3. Record loss at each LR
4. Plot loss vs LR
5. Choose LR where loss decreases fastest

Loss
  |
  |\
  | \
  |  \___
  |      \
  |       \
  └────────\──── LR
       ↑
    Good LR (steepest descent)
```

---

### 8.5 Batch Normalization

Normalize activations within each mini-batch.

#### Algorithm

```
For mini-batch B = {x_1, ..., x_m}:

1. Compute batch statistics:
   μ_B = (1/m) * sum(x_i)
   σ_B^2 = (1/m) * sum((x_i - μ_B)^2)

2. Normalize:
   x̂_i = (x_i - μ_B) / sqrt(σ_B^2 + ε)

3. Scale and shift (learnable):
   y_i = γ * x̂_i + β

γ, β are learned parameters
```

#### Why It Works

```
1. Reduces internal covariate shift
   - Layer inputs have stable distribution
   - Easier optimization

2. Allows higher learning rates
   - Gradients don't explode/vanish as easily

3. Regularization effect
   - Batch statistics add noise
   - Reduces need for dropout

4. Enables deeper networks
   - Stabilizes training
```

#### Training vs Inference

```
Training:
- Use batch statistics (μ_B, σ_B)
- Update running averages

Inference:
- Use running averages (μ_running, σ_running)
- No batch dependency
- Deterministic output

running_mean = momentum * running_mean + (1 - momentum) * μ_B
```

#### Layer Normalization

```
Normalize across features (not batch):

For each sample x:
    μ = mean across features
    σ = std across features
    x̂ = (x - μ) / (σ + ε)
    y = γ * x̂ + β

Advantages:
- Works with batch size 1
- Better for RNNs, Transformers
- No train/test discrepancy
```

#### Comparison

| Aspect | Batch Norm | Layer Norm |
|--------|------------|------------|
| Normalize over | Batch | Features |
| Batch size dependency | Yes | No |
| Best for | CNNs | RNNs, Transformers |
| Train/test difference | Yes | No |

---

### 8.6 Regularization Techniques

#### Weight Decay (L2)

```
L_total = L_data + λ * sum(w^2)

Equivalent to:
w = w - α * (∇L + 2λw)
  = w * (1 - 2αλ) - α * ∇L
       └─────────┘
       decay factor

Shrinks weights toward zero
Prevents overfitting
```

#### Dropout

```
During training:
- Randomly set neurons to 0 with probability p
- Scale remaining by 1/(1-p)

During inference:
- Use all neurons (no dropout)

Effect:
- Prevents co-adaptation
- Ensemble of subnetworks
- Regularization
```

#### Early Stopping

```
Monitor validation loss during training
Stop when validation loss stops improving

patience = number of epochs to wait
best_loss = inf
wait = 0

for epoch in epochs:
    if val_loss < best_loss:
        best_loss = val_loss
        save_model()
        wait = 0
    else:
        wait += 1
        if wait >= patience:
            break
```

#### Data Augmentation

```
Artificially increase training data diversity

Images:
- Random crop, flip, rotation
- Color jitter, cutout
- Mixup, CutMix

Text:
- Synonym replacement
- Back-translation
- Random deletion/swap

Effect: Reduces overfitting, improves generalization
```

---

### 8.7 Training Acceleration

#### Mixed Precision Training

```
Use FP16 for most operations, FP32 for critical ones

Benefits:
- 2x memory reduction
- 2-8x faster on modern GPUs
- Minimal accuracy loss

Implementation:
- Forward pass: FP16
- Loss scaling: prevent underflow
- Master weights: FP32
- Gradient accumulation: FP32
```

```python
# PyTorch automatic mixed precision
scaler = torch.cuda.amp.GradScaler()

with torch.cuda.amp.autocast():
    output = model(input)
    loss = criterion(output, target)

scaler.scale(loss).backward()
scaler.step(optimizer)
scaler.update()
```

#### Gradient Accumulation

```
Simulate larger batch size with limited memory

effective_batch = batch_size * accumulation_steps

for i, (x, y) in enumerate(dataloader):
    loss = model(x, y) / accumulation_steps
    loss.backward()
    
    if (i + 1) % accumulation_steps == 0:
        optimizer.step()
        optimizer.zero_grad()
```

#### Gradient Checkpointing

```
Trade compute for memory

Standard: Store all activations for backward pass
Checkpointing: Store only some, recompute others

Memory: O(sqrt(n)) instead of O(n)
Compute: ~30% overhead

Use for: Very deep networks, limited GPU memory
```


#### Data Parallelism

```
Distribute batches across multiple GPUs

Each GPU:
1. Gets subset of batch
2. Forward pass
3. Compute gradients
4. All-reduce gradients (average)
5. Update weights

Effective batch size = batch_per_gpu * num_gpus
```

```python
# PyTorch DataParallel
model = nn.DataParallel(model)

# PyTorch DistributedDataParallel (preferred)
model = nn.parallel.DistributedDataParallel(model)
```

#### Model Parallelism

```
Split model across GPUs (for very large models)

Pipeline parallelism:
- Split layers across GPUs
- Micro-batches flow through pipeline

Tensor parallelism:
- Split individual layers
- Each GPU computes part of layer

Use for: Models that don't fit on single GPU
```

---

### 8.8 Memory Optimization

#### Reducing Memory Usage

| Technique | Memory Savings | Trade-off |
|-----------|---------------|-----------|
| Mixed precision | 2x | Minimal accuracy loss |
| Gradient checkpointing | 2-5x | 30% slower |
| Smaller batch size | Linear | May need LR adjustment |
| Gradient accumulation | None (same effective batch) | Slower |
| Model pruning | Varies | May lose accuracy |

#### Memory Breakdown

```
GPU Memory = Model + Activations + Gradients + Optimizer States

Model: Parameters (FP32: 4 bytes each)
Activations: Intermediate outputs (scales with batch)
Gradients: Same size as parameters
Optimizer: Adam needs 2x parameters (m, v)

Example: 1B parameter model
- Parameters: 4 GB
- Gradients: 4 GB
- Adam states: 8 GB
- Total (no activations): 16 GB
```

#### Efficient Attention

```
Standard attention: O(n^2) memory for sequence length n

Flash Attention:
- Tiled computation
- O(n) memory
- Faster due to better memory access

Use for: Long sequences, large batch sizes
```

---

## Questions & Answers

### ⭐ Q1: How do loss functions, optimizers, regularization, and feature selection impact ML models?

**Answer:**

**Loss Functions:**
```
Define WHAT the model optimizes

Impact:
- MSE: Sensitive to outliers, assumes Gaussian errors
- Cross-entropy: Better for classification, handles probabilities
- Focal loss: Addresses class imbalance
- Triplet loss: Learns embeddings for similarity

Wrong loss → model optimizes wrong objective
```

**Optimizers:**
```
Define HOW the model optimizes

Impact:
- SGD: Simple, needs tuning, good generalization
- Adam: Fast convergence, adaptive LR, may overfit
- AdamW: Better generalization for transformers

Wrong optimizer → slow convergence or poor minima
```

**Regularization:**
```
Prevents overfitting

Impact:
- L2/Weight decay: Shrinks weights, smoother functions
- Dropout: Prevents co-adaptation, ensemble effect
- Early stopping: Stops before overfitting
- Data augmentation: More diverse training data

Too little → overfitting
Too much → underfitting
```

**Feature Selection:**
```
Chooses relevant features

Impact:
- Reduces dimensionality
- Removes noise
- Improves interpretability
- Faster training

Methods:
- Filter: Correlation, mutual information
- Wrapper: Forward/backward selection
- Embedded: L1 regularization, tree importance
```

**Interactions:**
```
Loss + Optimizer: Some losses work better with certain optimizers
Regularization + Features: L1 does feature selection
Batch size + LR: Larger batch often needs larger LR
```

---

### ⭐ Q2: Explain gradient descent and batch normalization. How can you accelerate and parallelize training?

**Answer:**

**Gradient Descent:**
```
Iteratively minimize loss by moving in negative gradient direction

θ = θ - α * ∇L(θ)

Variants:
- Batch: All data per update (stable, slow)
- Mini-batch: Subset per update (balanced)
- Stochastic: One sample per update (fast, noisy)

Improvements:
- Momentum: Accumulate velocity
- Adam: Adaptive learning rates
```

**Batch Normalization:**
```
Normalize activations within mini-batch

x̂ = (x - μ_B) / σ_B
y = γ * x̂ + β

Benefits:
- Stable gradients
- Higher learning rates possible
- Regularization effect
- Enables deeper networks
```

**Acceleration Techniques:**

| Technique | Speedup | How |
|-----------|---------|-----|
| Mixed precision | 2-8x | FP16 computation |
| Larger batch | Linear | More parallelism |
| Better optimizer | Varies | Faster convergence |
| Learning rate schedule | Varies | Warmup + decay |
| Efficient attention | 2-4x | Flash Attention |

**Parallelization:**

```
Data Parallelism:
- Split batch across GPUs
- Each GPU: forward, backward
- All-reduce gradients
- Scales to many GPUs

Model Parallelism:
- Split model across GPUs
- For models too large for one GPU
- Pipeline or tensor parallelism

Distributed Training:
- Multiple machines
- Gradient synchronization
- Frameworks: Horovod, PyTorch DDP
```

**Practical Recipe:**
```python
# 1. Use mixed precision
scaler = GradScaler()
with autocast():
    loss = model(x)

# 2. Use efficient optimizer
optimizer = AdamW(model.parameters(), lr=1e-4)

# 3. Use learning rate schedule
scheduler = CosineAnnealingLR(optimizer, T_max=epochs)

# 4. Use data parallelism
model = DistributedDataParallel(model)

# 5. Use gradient accumulation for larger effective batch
loss = loss / accumulation_steps
```

---

### Q3: What is the difference between batch, mini-batch, and stochastic gradient descent?

**Answer:**

**Batch Gradient Descent:**
```
θ = θ - α * (1/n) * sum_{i=1}^n ∇L(x_i, y_i; θ)

Uses ALL n samples per update

Pros:
- True gradient (no noise)
- Stable convergence
- Deterministic

Cons:
- Slow (one update per epoch)
- Memory intensive
- Can't escape local minima
```

**Stochastic Gradient Descent (SGD):**
```
For each sample:
    θ = θ - α * ∇L(x_i, y_i; θ)

Uses ONE sample per update

Pros:
- Fast updates (n per epoch)
- Can escape local minima
- Online learning possible

Cons:
- High variance
- Noisy convergence
- Poor GPU utilization
```

**Mini-Batch Gradient Descent:**
```
For each batch B of size b:
    θ = θ - α * (1/b) * sum_{i∈B} ∇L(x_i, y_i; θ)

Uses b samples per update (typically 32-256)

Pros:
- Balanced noise/stability
- Efficient GPU utilization
- Good generalization

Cons:
- Batch size is hyperparameter
```

**Comparison:**

| Aspect | Batch | Mini-Batch | SGD |
|--------|-------|------------|-----|
| Samples/update | n | b | 1 |
| Updates/epoch | 1 | n/b | n |
| Variance | 0 | Low | High |
| GPU efficiency | High | High | Low |
| Memory | O(n) | O(b) | O(1) |
| Convergence | Smooth | Moderate | Noisy |

**In Practice:**
```
Mini-batch is standard:
- Batch size 32-256 for most tasks
- Larger (1024+) for distributed training
- Smaller for limited memory

Batch size affects:
- Generalization (smaller often better)
- Training speed (larger is faster)
- Learning rate (scale with batch size)
```

---

### Q4: How do you optimize training for memory?

**Answer:**

**Memory Components:**
```
Total = Model + Activations + Gradients + Optimizer

Model: 4 bytes/param (FP32)
Activations: Scales with batch size and depth
Gradients: Same as model
Optimizer: Adam = 2x model (m, v states)
```

**Optimization Techniques:**

**1. Mixed Precision (FP16):**
```
- Model weights: FP16 (2 bytes)
- Activations: FP16
- Master weights: FP32 (for updates)
- ~2x memory reduction
```

**2. Gradient Checkpointing:**
```
- Don't store all activations
- Recompute during backward pass
- Trade compute for memory
- ~2-5x memory reduction, ~30% slower
```

**3. Gradient Accumulation:**
```
- Use smaller batch size
- Accumulate gradients over steps
- Same effective batch, less memory

for i, batch in enumerate(loader):
    loss = model(batch) / accum_steps
    loss.backward()
    if (i + 1) % accum_steps == 0:
        optimizer.step()
        optimizer.zero_grad()
```

**4. Efficient Optimizers:**
```
- SGD: No extra states (vs Adam's 2x)
- Adafactor: Factorized second moments
- 8-bit Adam: Quantized optimizer states
```

**5. Model Modifications:**
```
- Smaller batch size
- Shorter sequences (for transformers)
- Fewer layers
- Smaller hidden dimensions
- Pruning
```

**6. Efficient Attention:**
```
- Flash Attention: O(n) memory vs O(n^2)
- Sparse attention patterns
- Linear attention approximations
```

**Memory Estimation:**
```python
# Rough estimate for transformer
params = num_layers * (4 * d_model^2 + 2 * d_model * d_ff)
model_memory = params * 4  # FP32 bytes
optimizer_memory = params * 8  # Adam
activation_memory = batch * seq_len * d_model * num_layers * 4

total = model_memory + optimizer_memory + activation_memory
```

---

### Q5: How does Adam optimizer work and why is it popular?

**Answer:**

**Adam Algorithm:**
```
Initialize: m_0 = 0, v_0 = 0, t = 0

For each step:
    t = t + 1
    g_t = ∇L(θ)
    
    # Update biased first moment (momentum)
    m_t = β_1 * m_{t-1} + (1 - β_1) * g_t
    
    # Update biased second moment (RMSprop)
    v_t = β_2 * v_{t-1} + (1 - β_2) * g_t^2
    
    # Bias correction
    m̂_t = m_t / (1 - β_1^t)
    v̂_t = v_t / (1 - β_2^t)
    
    # Update parameters
    θ = θ - α * m̂_t / (sqrt(v̂_t) + ε)

Defaults: β_1 = 0.9, β_2 = 0.999, ε = 1e-8
```

**Why It Works:**

```
1. Momentum (m_t):
   - Exponential moving average of gradients
   - Accelerates in consistent direction
   - Dampens oscillations

2. Adaptive LR (v_t):
   - Per-parameter learning rates
   - Large gradients → smaller steps
   - Small gradients → larger steps

3. Bias Correction:
   - m_0 = v_0 = 0 causes bias early on
   - Correction: divide by (1 - β^t)
   - Important for first few steps
```

**Why Popular:**

| Reason | Explanation |
|--------|-------------|
| Works out of box | Good defaults, little tuning |
| Fast convergence | Combines momentum + adaptive LR |
| Robust | Works across many architectures |
| Memory efficient | Only 2x parameters for states |

**When NOT to Use:**

```
- SGD+momentum often generalizes better (CNNs)
- AdamW preferred for transformers
- Large batch: LAMB or LARS optimizers
```

