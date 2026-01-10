# 7. Reinforcement Learning

---

## Key Concepts

### 7.1 Reinforcement Learning Overview

Agent learns to make decisions by interacting with an environment.

```
        ┌─────────────────────────────────────┐
        │                                     │
        ▼                                     │
    ┌───────┐    action a_t    ┌───────────┐ │
    │ Agent │ ───────────────→ │Environment│ │
    └───────┘                  └───────────┘ │
        ▲                           │        │
        │    state s_t, reward r_t  │        │
        └───────────────────────────┘        │
                                             │
        At each timestep t:                  │
        1. Agent observes state s_t          │
        2. Agent takes action a_t            │
        3. Environment returns s_{t+1}, r_t ─┘
```

#### RL vs Other Paradigms

| Paradigm | Feedback | Goal |
|----------|----------|------|
| Supervised | Correct answer for each input | Minimize prediction error |
| Unsupervised | None | Find structure |
| Reinforcement | Delayed reward signal | Maximize cumulative reward |

#### Key Challenges

```
1. Credit assignment: Which actions led to reward?
2. Exploration vs exploitation: Try new vs use known good
3. Delayed rewards: Reward may come much later
4. Non-stationarity: Environment may change
```

---

### 7.2 Markov Decision Process (MDP)

Mathematical framework for sequential decision making.

#### Components

```
MDP = (S, A, P, R, γ)

S: State space (all possible states)
A: Action space (all possible actions)
P: Transition function P(s' | s, a)
R: Reward function R(s, a, s')
γ: Discount factor ∈ [0, 1]
```

#### Markov Property

```
P(s_{t+1} | s_t, a_t, s_{t-1}, a_{t-1}, ...) = P(s_{t+1} | s_t, a_t)

Future depends only on current state and action
History is summarized in current state
```

#### Policy

```
π(a | s) = probability of taking action a in state s

Deterministic: π(s) = a
Stochastic: π(a | s) = P(a | s)

Goal: Find optimal policy π* that maximizes expected return
```

#### Return and Discount Factor

```
Return G_t = r_t + γ*r_{t+1} + γ^2*r_{t+2} + ...
           = sum_{k=0}^∞ γ^k * r_{t+k}

γ close to 0: Myopic (care about immediate reward)
γ close to 1: Far-sighted (care about future rewards)

Why discount?
- Mathematical convenience (ensures finite sum)
- Models uncertainty about future
- Preference for sooner rewards
```

---

### 7.3 Value Functions

#### State Value Function V(s)

```
V^π(s) = E_π[G_t | s_t = s]
       = E_π[sum_{k=0}^∞ γ^k * r_{t+k} | s_t = s]

Expected return starting from state s, following policy π
```

#### Action Value Function Q(s, a)

```
Q^π(s, a) = E_π[G_t | s_t = s, a_t = a]

Expected return starting from state s, taking action a, then following π
```

#### Relationship

```
V^π(s) = sum_a π(a|s) * Q^π(s, a)

Q^π(s, a) = R(s, a) + γ * sum_{s'} P(s'|s,a) * V^π(s')
```


#### Bellman Equations

**Bellman Expectation Equation:**
```
V^π(s) = sum_a π(a|s) * [R(s,a) + γ * sum_{s'} P(s'|s,a) * V^π(s')]

Q^π(s,a) = R(s,a) + γ * sum_{s'} P(s'|s,a) * sum_{a'} π(a'|s') * Q^π(s',a')
```

**Bellman Optimality Equation:**
```
V*(s) = max_a [R(s,a) + γ * sum_{s'} P(s'|s,a) * V*(s')]

Q*(s,a) = R(s,a) + γ * sum_{s'} P(s'|s,a) * max_{a'} Q*(s',a')

Optimal policy: π*(s) = argmax_a Q*(s, a)
```

---

### 7.4 Dynamic Programming

Solve MDPs when model (P, R) is known.

#### Policy Evaluation

Compute V^π for a given policy:

```
Repeat until convergence:
    For each state s:
        V(s) = sum_a π(a|s) * [R(s,a) + γ * sum_{s'} P(s'|s,a) * V(s')]
```

#### Policy Improvement

```
π'(s) = argmax_a [R(s,a) + γ * sum_{s'} P(s'|s,a) * V^π(s')]

If π' ≠ π, then π' is strictly better
```

#### Policy Iteration

```
1. Initialize π arbitrarily
2. Repeat:
   a. Policy Evaluation: compute V^π
   b. Policy Improvement: π' = greedy(V^π)
   c. If π' = π, stop (optimal)
   d. π = π'
```

#### Value Iteration

```
Combine evaluation and improvement:

Repeat until convergence:
    For each state s:
        V(s) = max_a [R(s,a) + γ * sum_{s'} P(s'|s,a) * V(s')]

Extract policy: π(s) = argmax_a [R(s,a) + γ * sum_{s'} P(s'|s,a) * V(s')]
```

---

### 7.5 Model-Free Methods

Learn without knowing P and R.

#### Monte Carlo Methods

Learn from complete episodes:

```
For each episode:
    Generate episode using π: s_0, a_0, r_0, s_1, a_1, r_1, ...
    For each state s visited:
        G = return from first visit to s
        V(s) = V(s) + α * (G - V(s))

First-visit MC: Use only first occurrence of s
Every-visit MC: Use all occurrences of s
```

**Properties:**
- Unbiased estimate
- High variance (full episode needed)
- Only works for episodic tasks

#### Temporal Difference (TD) Learning

Learn from incomplete episodes using bootstrapping:

```
TD(0) update:
V(s) = V(s) + α * [r + γ*V(s') - V(s)]
                   └────────────────┘
                      TD target

TD error: δ = r + γ*V(s') - V(s)
```

**Properties:**
- Biased (bootstraps from estimate)
- Lower variance than MC
- Works for continuing tasks
- Online learning (update every step)

#### MC vs TD

| Aspect | Monte Carlo | TD Learning |
|--------|-------------|-------------|
| Bias | Unbiased | Biased |
| Variance | High | Low |
| Episodes | Complete required | Incomplete OK |
| Bootstrapping | No | Yes |
| Convergence | Slower | Faster |

---

### 7.6 Q-Learning

Off-policy TD control algorithm.

#### Algorithm

```
Initialize Q(s, a) arbitrarily

For each episode:
    Initialize s
    For each step:
        Choose a using policy derived from Q (e.g., ε-greedy)
        Take action a, observe r, s'
        
        Q(s, a) = Q(s, a) + α * [r + γ * max_{a'} Q(s', a') - Q(s, a)]
                                 └──────────────────────────────────┘
                                           TD target (uses max)
        s = s'
```

**Key Properties:**
```
- Off-policy: learns Q* regardless of behavior policy
- Uses max over actions (optimistic)
- Converges to optimal Q* under conditions
```

#### ε-Greedy Exploration

```
With probability ε: choose random action (explore)
With probability 1-ε: choose argmax_a Q(s, a) (exploit)

Decay ε over time: start exploring, then exploit
```


---

### 7.7 SARSA

On-policy TD control algorithm.

#### Algorithm

```
Initialize Q(s, a) arbitrarily

For each episode:
    Initialize s
    Choose a using policy derived from Q (e.g., ε-greedy)
    
    For each step:
        Take action a, observe r, s'
        Choose a' using policy derived from Q (e.g., ε-greedy)
        
        Q(s, a) = Q(s, a) + α * [r + γ * Q(s', a') - Q(s, a)]
                                 └────────────────────────────┘
                                   TD target (uses actual a')
        s = s', a = a'
```

**Name:** State-Action-Reward-State-Action (SARSA)

#### Q-Learning vs SARSA

```
Q-Learning (off-policy):
Q(s,a) += α * [r + γ * max_{a'} Q(s',a') - Q(s,a)]
                       └─────────────┘
                       Best possible action

SARSA (on-policy):
Q(s,a) += α * [r + γ * Q(s', a') - Q(s,a)]
                       └────────┘
                       Actual next action
```

| Aspect | Q-Learning | SARSA |
|--------|------------|-------|
| Policy | Off-policy | On-policy |
| Target | max Q(s', a') | Q(s', a') |
| Learns | Optimal Q* | Q for current policy |
| Safety | Ignores exploration cost | Accounts for exploration |
| Convergence | To Q* | To Q^π |

**Cliff Walking Example:**
```
Start ─────────────────── Goal
      │ Cliff (negative) │

Q-Learning: Takes optimal (risky) path near cliff
SARSA: Takes safer path away from cliff (accounts for ε-greedy mistakes)
```

---

### 7.8 Policy Gradient Methods

Directly optimize the policy without value functions.

#### Why Policy Gradients?

```
Value-based limitations:
- Discrete actions only (argmax)
- Can't represent stochastic policies
- Small Q changes → big policy changes

Policy gradients:
- Continuous actions natural
- Stochastic policies
- Smooth policy updates
```

#### Policy Parameterization

```
π_θ(a | s) = parameterized policy

For discrete actions: softmax over action preferences
π_θ(a | s) = exp(h(s,a,θ)) / sum_{a'} exp(h(s,a',θ))

For continuous actions: Gaussian
π_θ(a | s) = N(μ_θ(s), σ_θ(s))
```

#### Objective

```
J(θ) = E_π[G_0] = E_π[sum_t γ^t * r_t]

Goal: Find θ* = argmax_θ J(θ)
```

#### Policy Gradient Theorem

```
∇_θ J(θ) = E_π[∇_θ log π_θ(a|s) * Q^π(s, a)]

Intuition:
- Increase probability of actions with high Q
- Decrease probability of actions with low Q
```

#### REINFORCE Algorithm

```
For each episode:
    Generate trajectory: s_0, a_0, r_0, ..., s_T
    For t = 0 to T:
        G_t = sum_{k=t}^T γ^{k-t} * r_k  (return from t)
        θ = θ + α * ∇_θ log π_θ(a_t | s_t) * G_t
```

**Properties:**
- Monte Carlo: uses full returns
- High variance (full episode)
- Unbiased gradient estimate

#### Variance Reduction: Baseline

```
∇_θ J(θ) = E_π[∇_θ log π_θ(a|s) * (Q^π(s,a) - b(s))]

Baseline b(s) doesn't change expectation but reduces variance
Common choice: b(s) = V^π(s)

Advantage: A(s,a) = Q(s,a) - V(s)
"How much better is action a than average?"
```

---

### 7.9 Actor-Critic Methods

Combine policy gradients (actor) with value functions (critic).

#### Architecture

```
┌────────────────────────────────────┐
│              Agent                 │
│  ┌──────────┐    ┌──────────┐     │
│  │  Actor   │    │  Critic  │     │
│  │  π_θ(a|s)│    │  V_w(s)  │     │
│  └────┬─────┘    └────┬─────┘     │
│       │               │           │
│       │    TD error   │           │
│       │◄──────────────┤           │
│       │               │           │
└───────┼───────────────┼───────────┘
        │               │
        ▼               ▼
    Action a      Value estimate
```

#### Algorithm (A2C - Advantage Actor-Critic)

```
For each step:
    Take action a ~ π_θ(a | s)
    Observe r, s'
    
    # Critic update (TD learning)
    δ = r + γ * V_w(s') - V_w(s)  # TD error ≈ advantage
    w = w + α_w * δ * ∇_w V_w(s)
    
    # Actor update (policy gradient)
    θ = θ + α_θ * δ * ∇_θ log π_θ(a | s)
```

**Key Insight:**
```
TD error δ = r + γV(s') - V(s) ≈ A(s,a)

Use TD error as advantage estimate
- Lower variance than Monte Carlo
- Some bias from bootstrapping
```

#### A3C (Asynchronous Advantage Actor-Critic)

```
Multiple parallel actors:
- Each actor interacts with own environment copy
- Asynchronously update shared parameters
- Diverse experience, faster training
```

---

### 7.10 Deep Reinforcement Learning

Use neural networks to approximate value functions or policies.

#### Deep Q-Network (DQN)

```
Q(s, a; θ) ≈ Q*(s, a)

Neural network takes state s, outputs Q-values for all actions
```

**Key Innovations:**

**1. Experience Replay:**
```
Store transitions (s, a, r, s') in replay buffer
Sample random mini-batches for training

Benefits:
- Breaks correlation between consecutive samples
- Reuse experience multiple times
- More stable training
```

**2. Target Network:**
```
Use separate network θ^- for TD target:
y = r + γ * max_{a'} Q(s', a'; θ^-)

Update θ^- periodically (copy from θ)

Benefits:
- Stable targets during training
- Prevents oscillation/divergence
```

**DQN Algorithm:**
```
Initialize replay buffer D
Initialize Q-network θ, target network θ^- = θ

For each episode:
    For each step:
        Select a = argmax_a Q(s, a; θ) with ε-greedy
        Execute a, observe r, s'
        Store (s, a, r, s') in D
        
        Sample mini-batch from D
        Compute targets: y = r + γ * max_{a'} Q(s', a'; θ^-)
        Update θ by minimizing (y - Q(s, a; θ))^2
        
        Periodically: θ^- = θ
```


#### DQN Improvements

| Method | Improvement |
|--------|-------------|
| Double DQN | Reduce overestimation: use θ to select, θ^- to evaluate |
| Dueling DQN | Separate V(s) and A(s,a) streams |
| Prioritized Replay | Sample important transitions more often |
| Noisy Nets | Parameter noise for exploration |
| Rainbow | Combine all improvements |

#### Policy Gradient with Neural Networks

```
Actor network: π_θ(a | s)
Critic network: V_w(s) or Q_w(s, a)

PPO (Proximal Policy Optimization):
- Clip policy updates to prevent large changes
- L^CLIP = min(r_t * A_t, clip(r_t, 1-ε, 1+ε) * A_t)
- Where r_t = π_θ(a|s) / π_θ_old(a|s)

TRPO (Trust Region Policy Optimization):
- Constrain KL divergence between old and new policy
- More stable but computationally expensive
```

---

### 7.11 Multi-Armed Bandits

Simplified RL: single state, immediate rewards.

#### Problem Setup

```
K slot machines (arms), each with unknown reward distribution
At each round:
    1. Choose an arm
    2. Receive reward from that arm's distribution
    
Goal: Maximize cumulative reward
Challenge: Explore to learn vs exploit best known
```

#### Regret

```
Regret = T * μ* - sum_t r_t

Where μ* = expected reward of best arm
Measures loss from not always playing optimal arm
```

#### Strategies

**ε-Greedy:**
```
With probability ε: random arm
With probability 1-ε: best known arm

Simple but ε is fixed (doesn't adapt)
```

**UCB (Upper Confidence Bound):**
```
a_t = argmax_a [Q(a) + c * sqrt(log(t) / N(a))]
                └────┘   └────────────────────┘
               exploit        explore bonus

Optimism in face of uncertainty
Explore arms with high uncertainty
Regret: O(log T)
```

**Thompson Sampling:**
```
Maintain posterior distribution for each arm's mean
At each round:
    Sample θ_a from posterior for each arm
    Play arm with highest sampled θ_a
    Update posterior with observed reward

Bayesian approach
Often best empirical performance
```

#### Comparison

| Method | Regret | Computation | Tuning |
|--------|--------|-------------|--------|
| ε-greedy | O(T) | O(1) | ε |
| UCB | O(log T) | O(K) | c |
| Thompson | O(log T) | O(K) | Prior |

---

### 7.12 Exploration vs Exploitation

Fundamental tradeoff in RL.

#### The Dilemma

```
Exploitation: Use current knowledge to maximize reward
Exploration: Try new actions to gain information

Too much exploitation: Miss better options (local optimum)
Too much exploration: Waste time on suboptimal actions
```

#### Exploration Strategies

**1. ε-Greedy:**
```
Simple, widely used
Decay ε over time: ε_t = ε_0 / t
```

**2. Boltzmann (Softmax) Exploration:**
```
P(a) = exp(Q(a) / τ) / sum_{a'} exp(Q(a') / τ)

τ = temperature
High τ: uniform (explore)
Low τ: greedy (exploit)
```

**3. UCB (Optimism):**
```
Add exploration bonus to value estimates
Naturally balances explore/exploit
```

**4. Intrinsic Motivation:**
```
Reward curiosity/novelty
Bonus for visiting new states
Helps in sparse reward environments
```

**5. Parameter Noise:**
```
Add noise to network parameters
More structured exploration than action noise
```

---

## Questions & Answers

### ⭐ Q1: Explain deep reinforcement learning.

**Answer:**

Deep RL combines deep neural networks with reinforcement learning to handle high-dimensional state/action spaces.

**Why Deep Learning for RL?**
```
Traditional RL: Tabular (store Q(s,a) for each state-action)
Problem: State space too large (images, continuous states)

Solution: Use neural networks as function approximators
- Q(s, a; θ) ≈ Q*(s, a)
- π_θ(a | s) ≈ π*(a | s)
- V_θ(s) ≈ V*(s)
```

**Key Algorithms:**

| Algorithm | Type | Key Idea |
|-----------|------|----------|
| DQN | Value-based | Q-network + replay + target network |
| Double DQN | Value-based | Reduce Q overestimation |
| A3C/A2C | Actor-Critic | Parallel actors, advantage |
| PPO | Policy gradient | Clipped objective for stability |
| SAC | Actor-Critic | Maximum entropy, continuous actions |

**DQN Innovations:**
```
1. Experience Replay
   - Store (s, a, r, s') in buffer
   - Sample random batches
   - Breaks correlation, reuses data

2. Target Network
   - Separate network for TD targets
   - Updated periodically
   - Stabilizes training
```

**Challenges:**
```
- Sample inefficiency (need millions of interactions)
- Stability (divergence, catastrophic forgetting)
- Exploration in high dimensions
- Credit assignment over long horizons
```

**Applications:**
```
- Game playing (Atari, Go, StarCraft)
- Robotics (manipulation, locomotion)
- Recommendation systems
- RLHF for LLMs (ChatGPT, Claude)
```

---

### ⭐ Q2: What is the difference between Q-learning and SARSA?

**Answer:**

Both are TD methods for learning action values, but differ in policy used for updates.

**Q-Learning (Off-policy):**
```
Q(s,a) += α * [r + γ * max_{a'} Q(s',a') - Q(s,a)]
                       └─────────────┘
                       Uses BEST action

- Learns optimal Q* regardless of behavior policy
- More aggressive (optimistic about future)
- Can learn from any data (off-policy)
```

**SARSA (On-policy):**
```
Q(s,a) += α * [r + γ * Q(s',a') - Q(s,a)]
                       └────────┘
                       Uses ACTUAL next action

- Learns Q for the policy being followed
- More conservative (accounts for exploration)
- Must use data from current policy
```

**Key Differences:**

| Aspect | Q-Learning | SARSA |
|--------|------------|-------|
| Update target | max Q(s', a') | Q(s', a') |
| Policy type | Off-policy | On-policy |
| Learns | Q* (optimal) | Q^π (current policy) |
| Exploration cost | Ignores | Accounts for |
| Data efficiency | Can reuse old data | Needs fresh data |

**Cliff Walking Example:**
```
Safe path (longer):  ████████████
                     S          G
Optimal path:        S──────────G
                     ▓▓▓▓▓▓▓▓▓▓▓▓  (cliff: -100)

Q-Learning: Learns optimal path (near cliff)
            Ignores that ε-greedy might fall off

SARSA: Learns safer path (away from cliff)
       Accounts for exploration mistakes
```

**When to Use:**
```
Q-Learning:
- Want optimal policy
- Can afford exploration mistakes
- Have replay buffer (off-policy)

SARSA:
- Safety matters (robotics)
- Want policy that accounts for exploration
- Online learning without replay
```

---

### ⭐ Q3: How do multi-armed bandits work?

**Answer:**

Multi-armed bandits are a simplified RL problem with one state and immediate rewards.

**Problem:**
```
K arms (slot machines), each with unknown reward distribution
Each round: choose arm, receive reward
Goal: Maximize cumulative reward over T rounds
```

**Challenge: Explore vs Exploit**
```
Exploit: Play arm with highest estimated reward
Explore: Try other arms to learn their rewards

Need to balance both!
```

**Key Strategies:**

**1. ε-Greedy:**
```
With prob ε: random arm (explore)
With prob 1-ε: best arm (exploit)

Simple but doesn't adapt
Regret: O(εT) for fixed ε
```

**2. UCB (Upper Confidence Bound):**
```
Play: argmax_a [Q(a) + c * sqrt(log(t) / N(a))]

- Q(a): estimated value of arm a
- N(a): times arm a was played
- Bonus decreases as arm is played more

"Optimism in face of uncertainty"
Regret: O(log T) - optimal!
```

**3. Thompson Sampling:**
```
For each arm, maintain posterior over mean reward
Each round:
    Sample θ_a from posterior for each arm
    Play arm with highest sample
    Update posterior with observed reward

Bayesian approach
Often best in practice
```

**Comparison:**

| Method | Idea | Regret |
|--------|------|--------|
| ε-greedy | Random exploration | O(T) |
| UCB | Optimistic bonus | O(log T) |
| Thompson | Sample from posterior | O(log T) |

**Applications:**
```
- A/B testing (which variant is better?)
- Ad selection (which ad to show?)
- Clinical trials (which treatment?)
- Recommendation (which item to suggest?)
```

**Extensions:**
```
- Contextual bandits: state/context affects rewards
- Non-stationary: reward distributions change
- Combinatorial: select multiple arms
```

---

### Q4: What is the Bellman equation?

**Answer:**

The Bellman equation expresses the relationship between value of a state and values of successor states.

**Bellman Expectation Equation (for policy π):**
```
V^π(s) = E_π[r + γ * V^π(s') | s]
       = sum_a π(a|s) * [R(s,a) + γ * sum_{s'} P(s'|s,a) * V^π(s')]

"Value = immediate reward + discounted future value"
```

**Bellman Optimality Equation:**
```
V*(s) = max_a [R(s,a) + γ * sum_{s'} P(s'|s,a) * V*(s')]

Q*(s,a) = R(s,a) + γ * sum_{s'} P(s'|s,a) * max_{a'} Q*(s',a')

"Optimal value = best action's value"
```

**Why It Matters:**
```
1. Foundation of RL algorithms
   - Dynamic programming: solve Bellman equations
   - TD learning: sample-based Bellman updates

2. Recursive structure
   - Value of state depends on successor values
   - Enables bootstrapping

3. Optimality condition
   - Optimal policy satisfies Bellman optimality
   - Basis for Q-learning, value iteration
```

**In Practice:**
```
TD update is sampled Bellman equation:
V(s) += α * [r + γ*V(s') - V(s)]
            └──────────────────┘
            Bellman error (should be 0 at optimum)
```

---

### Q5: Explain the actor-critic architecture.

**Answer:**

Actor-critic combines policy gradient (actor) with value function (critic).

**Components:**
```
Actor: π_θ(a | s) - learns the policy
Critic: V_w(s) or Q_w(s,a) - evaluates the policy
```

**Why Combine?**
```
Pure policy gradient (REINFORCE):
- Uses Monte Carlo returns
- High variance, slow learning

Actor-Critic:
- Critic provides value estimates
- Lower variance through bootstrapping
- Faster learning
```

**Algorithm:**
```
For each step:
    # Act
    a ~ π_θ(a | s)
    Observe r, s'
    
    # Compute advantage (TD error)
    δ = r + γ * V_w(s') - V_w(s)
    
    # Update critic
    w += α_w * δ * ∇_w V_w(s)
    
    # Update actor
    θ += α_θ * δ * ∇_θ log π_θ(a | s)
```

**Key Insight:**
```
TD error δ ≈ Advantage A(s,a) = Q(s,a) - V(s)

Advantage: "How much better is action a than average?"
- Positive: action better than expected → increase probability
- Negative: action worse than expected → decrease probability
```

**Variants:**

| Method | Description |
|--------|-------------|
| A2C | Synchronous advantage actor-critic |
| A3C | Asynchronous parallel actors |
| PPO | Clipped objective for stability |
| SAC | Maximum entropy for exploration |

**Benefits:**
```
- Lower variance than pure policy gradient
- Works with continuous actions
- Online learning (no need for complete episodes)
- Can use experience replay (with importance sampling)
```

