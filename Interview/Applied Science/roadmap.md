# Applied Scientist Interview Prep Roadmap

## Links

- <https://www.reddit.com/r/Btechtards/comments/1o3xftk/my_roadmap_for_mlai_as_an_applied_scientist_in/>

## Topics

### 1. Mathematical Foundations

#### 1.1 Linear Algebra
- Vectors, matrices, matrix operations
- Eigenvalues, eigenvectors, eigendecomposition
- Singular Value Decomposition (SVD)
- Matrix calculus (gradients, Jacobians, Hessians)

#### 1.2 Calculus
- Single/multivariable calculus
- Partial derivatives, chain rule
- Optimization: gradient descent, convexity, Lagrange multipliers

#### 1.3 Probability & Statistics
- Random variables (discrete, continuous)
- Probability distributions (Gaussian, Bernoulli, Multinomial, Poisson)
- Conditional probability, Bayes' theorem
- Expectation, variance, covariance
- Markov chains, stationary distributions
- Maximum Likelihood Estimation (MLE)
- Bayesian inference, MAP estimation
- Hypothesis testing, p-values, confidence intervals
- A/B testing design and analysis

---

### 2. Core Machine Learning

#### 2.1 Supervised Learning
- Linear regression (closed-form, gradient descent)
- Logistic regression (binary, multiclass)
- Decision trees, Random Forests
- Support Vector Machines (SVMs), kernel methods
- Naive Bayes classifiers
- Ensemble methods: Bagging, Boosting, XGBoost, LightGBM

#### 2.2 Unsupervised Learning
- K-means, K-medoids clustering
- Hierarchical clustering, DBSCAN
- Gaussian Mixture Models (GMM)
- Expectation-Maximization (EM) algorithm

#### 2.3 Dimensionality Reduction
- Principal Component Analysis (PCA)
- Singular Value Decomposition (SVD)
- t-SNE, UMAP
- Autoencoders

#### 2.4 Probabilistic Graphical Models
- Bayesian networks
- Markov Random Fields
- Hidden Markov Models (HMMs)
- Conditional Random Fields (CRFs)
- Latent Dirichlet Allocation (LDA)
- Monte Carlo methods, Gibbs sampling

#### 2.5 Training & Optimization
- Loss functions: MSE, cross-entropy, hinge loss, contrastive loss
- Regularization: L1 (Lasso), L2 (Ridge), Elastic Net, Dropout
- Bias-variance tradeoff
- Cross-validation techniques (k-fold, stratified, leave-one-out)
- Hyperparameter tuning: grid search, random search, Bayesian optimization
- Handling class imbalance: SMOTE, class weights, oversampling/undersampling
- Feature engineering and selection

#### 2.6 Evaluation Metrics
- Classification: accuracy, precision, recall, F1, ROC-AUC, PR-AUC
- Regression: MSE, RMSE, MAE, R²
- Ranking: NDCG, MAP, MRR
- Information retrieval metrics

---

### 3. Deep Learning

#### 3.1 Neural Network Fundamentals
- Perceptrons, MLPs, universal approximation
- Activation functions: ReLU, sigmoid, tanh, softmax, GELU, Swish
- Backpropagation, computational graphs
- Weight initialization (Xavier, He)
- Batch normalization, layer normalization
- Optimizers: SGD, momentum, Adam, AdamW, RMSprop
- Learning rate schedules, warmup

#### 3.2 Convolutional Neural Networks (CNNs)
- Convolution, pooling, stride, padding
- Architectures: LeNet, AlexNet, VGG, ResNet, Inception, EfficientNet
- Skip connections, residual learning
- Object detection: YOLO, Faster R-CNN, SSD
- Semantic segmentation: U-Net, FCN
- Transfer learning, fine-tuning

#### 3.3 Sequence Models
- Recurrent Neural Networks (RNNs)
- Vanishing/exploding gradients
- LSTM, GRU cells
- Bidirectional RNNs (BiLSTM)
- Sequence-to-sequence models
- Attention mechanisms

#### 3.4 Natural Language Processing (NLP)
- Text preprocessing, tokenization (BPE, WordPiece, SentencePiece)
- Word embeddings: Word2Vec, GloVe, FastText
- Transformer architecture (self-attention, multi-head attention)
- Positional encodings
- BERT, GPT, T5, and modern LLMs
- Fine-tuning strategies: full fine-tuning, LoRA, adapters
- NLP tasks: NER, POS tagging, sentiment analysis, QA, summarization

#### 3.5 Language Models (LLM Era)
- Pretraining objectives: MLM, CLM, denoising
- Data collection, cleaning, deduplication
- Tokenizer design and vocabulary
- Scaling laws, compute-optimal training
- RLHF, instruction tuning, alignment
- Evaluation: perplexity, downstream benchmarks
- Inference optimization, KV caching
- Prompt engineering, in-context learning

#### 3.6 Generative Models
- Autoencoders, Variational Autoencoders (VAEs)
- Generative Adversarial Networks (GANs)
- Diffusion models
- Flow-based models

#### 3.7 Computer Vision (Advanced)
- Image classification, object detection
- Face recognition: FaceNet, ArcFace
- Image segmentation
- Vision Transformers (ViT)
- Multimodal models: CLIP, BLIP

---

### 4. Efficient Scaling & Deployment

#### 4.1 Model Compression
- Pruning (structured, unstructured)
- Quantization (INT8, INT4, mixed precision)
- Knowledge distillation
- Low-rank factorization

#### 4.2 Efficient Architectures
- MobileNet, ShuffleNet
- Efficient attention mechanisms
- Sparse transformers

#### 4.3 Deployment & Serving
- Model serialization (ONNX, TorchScript, SavedModel)
- Inference optimization: TensorRT, ONNX Runtime
- Edge deployment: TFLite, Core ML
- Model serving: latency, throughput, batching
- A/B testing in production
- Monitoring, drift detection

---

### 5. Reinforcement Learning

#### 5.1 Fundamentals
- Markov Decision Processes (MDPs)
- Bellman equations
- Value functions, Q-functions
- Exploration vs exploitation

#### 5.2 Classical Methods
- Dynamic programming: value iteration, policy iteration
- Monte Carlo methods
- Temporal Difference (TD) learning
- Q-learning, SARSA
- Multi-armed bandits (UCB, Thompson sampling)

#### 5.3 Deep Reinforcement Learning
- Deep Q-Networks (DQN), Double DQN, Dueling DQN
- Policy gradient methods: REINFORCE
- Actor-Critic methods: A2C, A3C
- Proximal Policy Optimization (PPO)
- Trust Region Policy Optimization (TRPO)
- Model-based RL

#### 5.4 Applications
- Game playing, robotics
- Recommendation systems
- RLHF for LLM alignment

## Common Questions

---

## Coding

Implement ML algorithms from scratch in Python. Focus on understanding the math, not just the API.

### Algorithms to Implement

| Algorithm | Key Concepts |
|-----------|--------------|
| Linear Regression | Closed-form (normal equation), gradient descent, MSE loss |
| Logistic Regression | Sigmoid, cross-entropy loss, gradient descent |
| K-Nearest Neighbors | Distance metrics (Euclidean, Manhattan), k selection |
| K-Means Clustering | Centroid initialization, convergence, elbow method |
| Decision Tree | Information gain, Gini impurity, recursive splitting |
| Naive Bayes | Bayes theorem, conditional independence assumption |
| Simple Neural Network | Forward pass, backpropagation, weight updates |
| Softmax Regression | Multiclass classification, softmax function |
| PCA | Covariance matrix, eigendecomposition |

### Common Coding Questions

1. **Implement linear regression with gradient descent**
   - Compute predictions, loss, gradients
   - Update weights iteratively
   - Add L2 regularization

2. **Implement logistic regression from scratch**
   - Sigmoid function
   - Binary cross-entropy loss
   - Gradient computation and update

3. **Implement a 2-layer neural network**
   - Forward propagation
   - Backpropagation with chain rule
   - ReLU and softmax activations

4. **Implement K-means clustering**
   - Random centroid initialization
   - Assignment and update steps
   - Convergence check

5. **Implement a decision tree classifier**
   - Calculate information gain / Gini impurity
   - Recursive tree building
   - Prediction traversal

6. **Implement softmax and cross-entropy loss**
   - Numerically stable softmax
   - Gradient of cross-entropy w.r.t. logits

7. **Implement batch normalization forward pass**

8. **Implement dropout (training and inference modes)**

9. **Implement attention mechanism**
   - Scaled dot-product attention
   - Query, Key, Value computation

10. **Implement word2vec (skip-gram with negative sampling)**

### Activation Functions to Know
- Sigmoid: `1 / (1 + exp(-x))`
- Tanh: `(exp(x) - exp(-x)) / (exp(x) + exp(-x))`
- ReLU: `max(0, x)`
- Leaky ReLU: `max(0.01x, x)`
- Softmax: `exp(x_i) / sum(exp(x_j))`
- GELU, Swish (modern activations)

### Loss Functions to Know
- MSE: `(1/n) * sum((y - y_hat)^2)`
- Binary Cross-Entropy: `-[y*log(p) + (1-y)*log(1-p)]`
- Categorical Cross-Entropy: `-sum(y_i * log(p_i))`
- Hinge Loss: `max(0, 1 - y * f(x))`
- Contrastive Loss, Triplet Loss

---

## ML Depth

Deep dive into YOUR projects and experience. Be ready to explain every decision.

### Preparation Checklist

- [ ] List all ML projects from resume
- [ ] For each project, prepare:
  - Problem statement and business impact
  - Data: size, features, preprocessing steps
  - Model choice and why (alternatives considered)
  - Loss function and evaluation metrics
  - Training details: optimizer, hyperparameters, regularization
  - Results: quantitative metrics, A/B test outcomes
  - Challenges faced and how you solved them
  - What you would do differently now

### Common ML Depth Questions

**Project Deep Dive**
- Walk me through your most impactful ML project end-to-end
- Why did you choose [model X] over [model Y]?
- How did you handle [specific challenge] in your project?
- What was the baseline? How much did your model improve over it?
- How did you validate your model before deployment?
- What would you do differently if you had more time/data/compute?

**Technical Decisions**
- Why did you use [specific loss function]?
- How did you tune hyperparameters?
- How did you handle class imbalance / missing data / outliers?
- What features were most important? How did you determine this?
- How did you prevent overfitting?

**Production & Scale**
- How was the model deployed?
- What was the latency / throughput requirement?
- How did you monitor model performance in production?
- Did you observe any data drift? How did you handle it?

**Failure Analysis**
- Where did your model fail? What were the error patterns?
- How did you debug model issues?
- What edge cases did you discover?

### Tips
- Use the STAR method (Situation, Task, Action, Result)
- Quantify impact wherever possible
- Be honest about limitations and failures
- Show depth of understanding, not just surface-level usage

## ML Breadth

Wide conceptual coverage across ML paradigms. Questions marked with ⭐ are frequently asked.

---

### 1. Fundamentals & Learning Paradigms

**Key Concepts**
- Supervised vs Unsupervised vs Reinforcement Learning
- Parametric vs Non-parametric models
- Generative vs Discriminative models
- Inductive bias

**Questions**
- ⭐ What are the differences between supervised, unsupervised, and reinforcement learning?
- What is the difference between parametric and non-parametric models? Give examples.
- What is inductive bias? Why is it important?
- When would you use a generative model vs a discriminative model?

---

### 2. Bias-Variance Tradeoff & Regularization ⭐⭐⭐

**Key Concepts**
- Bias: error from wrong assumptions (underfitting)
- Variance: error from sensitivity to training data (overfitting)
- Regularization: L1 (Lasso), L2 (Ridge), Elastic Net
- Why L1 induces sparsity (diamond vs circle constraint geometry)

**Questions**
- ⭐ What is the bias-variance tradeoff? How does it affect model performance?
- ⭐ What are the differences between L1 and L2 regularization?
- ⭐ Why does L1 regularization favor sparse parameters?
- How do you identify if a model is overfitting or underfitting?
- ⭐ What is overfitting and how can it be prevented?
- What is the Curse of Dimensionality, and how does it impact ML algorithms?
- How do you handle collinearity in features?

---

### 3. Supervised Learning

#### 3.1 Linear Models

**Key Concepts**
- Linear regression: assumptions, closed-form solution, gradient descent
- Logistic regression: sigmoid, decision boundary, multiclass (softmax)
- Assumptions: linearity, independence, homoscedasticity, normality of residuals

**Questions**
- ⭐ What are the assumptions of linear regression?
- ⭐ What is the closed-form solution of linear regression? When is gradient descent better?
- ⭐ How does logistic regression work?
- Write the loss function for logistic regression and prove it has a global minimum.
- How do you modify logistic regression for quadratically separable data?
- What would the parameters look like for a decision tree with just 2 features? What about logistic regression?

#### 3.2 Tree-Based Models

**Key Concepts**
- Decision trees: information gain, Gini impurity
- Random Forest: bagging, feature randomness
- Gradient Boosting: sequential error correction
- XGBoost, LightGBM: optimizations

**Questions**
- ⭐ How do ensemble methods like bagging and boosting work?
- ⭐ What is the difference between Boosting, Random Forest, and Bootstrap Aggregation?
- What is the computational difference between XGBoost and Random Forest?
- How does gradient boosting handle bias vs variance?

#### 3.3 Support Vector Machines

**Key Concepts**
- Maximum margin classifier
- Kernel trick: RBF, polynomial kernels
- Soft margin, slack variables

**Questions**
- How do SVMs work? What is the kernel trick?
- When would you use SVM over logistic regression?

---

### 4. Unsupervised Learning

#### 4.1 Clustering

**Key Concepts**
- K-means: centroid-based, sensitive to initialization
- DBSCAN: density-based, handles arbitrary shapes
- Hierarchical clustering: agglomerative, dendrogram
- GMM: probabilistic, soft assignments

**Questions**
- ⭐ What are the common techniques used in unsupervised learning?
- How does K-means work? What are its limitations?
- How would you classify products into categories and sub-categories?
- When would you use DBSCAN over K-means?

#### 4.2 Dimensionality Reduction

**Key Concepts**
- PCA: variance maximization, eigendecomposition
- SVD: matrix factorization
- t-SNE: neighborhood preservation (visualization)
- Autoencoders: learned nonlinear compression

**Questions**
- ⭐ What are methods for reducing dimensionality in a dataset, and how do they work?
- How does PCA work? What are its assumptions?
- When would you use t-SNE vs PCA?

---

### 5. Probabilistic Models

**Key Concepts**
- Bayesian networks, Markov models
- EM algorithm: E-step (expectation), M-step (maximization)
- LDA: topic modeling
- Monte Carlo methods, Gibbs sampling

**Questions**
- How does the EM algorithm work?
- ⭐ How is KL divergence different from cross-entropy loss?
- What are the differences between cross-entropy loss and contrastive loss?
- When would you use Bayesian inference vs MLE?

---

### 6. Deep Learning

#### 6.1 Neural Network Fundamentals

**Key Concepts**
- Feedforward networks, backpropagation
- Activation functions: ReLU, sigmoid, tanh, softmax
- Vanishing/exploding gradients
- Batch normalization, dropout

**Questions**
- ⭐ What are the basics of ANNs? What is the benefit of ReLU activation?
- What happens in a neural network if you remove all hidden layers?
- ⭐ What are regularization procedures in deep neural networks?
- ⭐ How do you prevent overfitting or underfitting in a deep learning model?

#### 6.2 Convolutional Neural Networks (CNNs)

**Key Concepts**
- Convolution, pooling, stride, padding
- Architectures: ResNet, VGG, Inception, U-Net
- Transfer learning, fine-tuning

**Questions**
- ⭐ How does a Convolutional Neural Network (CNN) work?
- What is a U-Net architecture, and what novel features does it offer?
- How can we use ResNet models for regression tasks?
- What are skip connections and why do they help?

#### 6.3 Sequential Models (RNNs, LSTMs)

**Key Concepts**
- RNN: sequential processing, hidden state
- LSTM: forget/input/output gates
- GRU: simplified gating
- Bidirectional RNNs

**Questions**
- ⭐ How does a Recurrent Neural Network (RNN) work?
- ⭐ How do GRU cells work, and how do they address the vanishing gradient problem?
- How does a BiLSTM work?

#### 6.4 Attention & Transformers

**Key Concepts**
- Self-attention, multi-head attention
- Positional encoding
- Encoder-decoder architecture
- BERT, GPT, T5

**Questions**
- ⭐ What is Attention in machine learning models?
- How does self-attention differ from RNN-based attention?
- What are the advantages of Transformers over RNNs?

#### 6.5 NLP Techniques

**Key Concepts**
- Word embeddings: Word2Vec, GloVe, FastText
- Contextual embeddings: BERT, ELMo
- Tasks: NER, POS tagging, sentiment analysis, QA

**Questions**
- How does Word2Vec work (skip-gram, CBOW)?
- What is the difference between static and contextual embeddings?
- What are common evaluation metrics for NLP tasks?

#### 6.6 Computer Vision

**Key Concepts**
- Image classification, object detection
- YOLO, Faster R-CNN
- Face recognition: FaceNet, ArcFace

**Questions**
- How does YOLO work for object detection?
- What is the difference between one-stage and two-stage detectors?

---

### 7. Reinforcement Learning

**Key Concepts**
- MDP, value functions, Q-functions
- Q-learning, SARSA
- Policy gradients, Actor-Critic
- Multi-armed bandits, exploration vs exploitation

**Questions**
- ⭐ Explain deep reinforcement learning.
- What is the difference between Q-learning and SARSA?
- How do multi-armed bandits work?

---

### 8. Training & Optimization

**Key Concepts**
- Loss functions: MSE, cross-entropy, hinge, contrastive, triplet
- Optimizers: SGD, Adam, RMSprop
- Learning rate schedules, warmup
- Gradient descent variants: batch, mini-batch, stochastic

**Questions**
- ⭐ How do loss functions, optimizers, regularization, and feature selection impact ML models?
- ⭐ Explain gradient descent and batch normalization. How can you accelerate and parallelize training?
- What is the difference between batch, mini-batch, and stochastic gradient descent?
- How do you optimize training for memory?

---

### 9. Model Evaluation & Validation

**Key Concepts**
- Train/validation/test splits
- Cross-validation: k-fold, stratified, leave-one-out
- Metrics by task type

**Questions**
- ⭐ What is cross-validation, and why is it important?
- Describe different types of cross-validation techniques.
- ⭐ Given an existing model, how would you improve its performance or efficiency?

---

### 10. Evaluation Metrics

#### Classification

| Metric | Use Case |
|--------|----------|
| Accuracy | Balanced classes |
| Precision | Minimize false positives (spam detection) |
| Recall | Minimize false negatives (disease detection) |
| F1-Score | Balance precision/recall |
| ROC-AUC | Ranking, threshold-independent |
| PR-AUC | Imbalanced datasets |

#### Regression

| Metric | Description |
|--------|-------------|
| MSE/RMSE | Penalizes large errors |
| MAE | Robust to outliers |
| R² | Explained variance |

#### Ranking

| Metric | Use Case |
|--------|----------|
| NDCG | Search ranking |
| MAP | Information retrieval |
| MRR | First relevant result |

**Questions**
- ⭐ Discuss the differences between precision, recall, and F1-score. When would you prioritize one over the others?
- What are common metrics for regression?
- What are common evaluation metrics for NLP tasks?

---

### 11. Practical ML Challenges

**Key Concepts**
- Missing data: imputation strategies
- Class imbalance: SMOTE, class weights, oversampling
- Feature engineering and selection
- Data drift, concept drift
- Hyperparameter tuning: grid search, random search, Bayesian optimization

**Questions**
- ⭐ How would you handle missing data in a dataset?
- ⭐ How do you handle data imbalance, collinearity, feature selection, and regularization?
- What is data drift and how do you detect it?
- Designing data pipelines for processing and preparing training data.

---

### 12. Statistics & Experimentation ⭐⭐

**Key Concepts**
- Probability distributions, Bayes' theorem
- Central Limit Theorem, Law of Large Numbers
- Hypothesis testing, p-values, confidence intervals
- A/B testing design and pitfalls
- MLE vs Bayesian inference

**Questions**
- ⭐ What is the central limit theorem and why is it important?
- ⭐ Explain how you would design and evaluate an A/B test.
- ⭐ What is a p-value? How would you interpret it in an A/B test?
- What are common pitfalls in A/B testing?
- ⭐ What is Maximum Likelihood Estimation (MLE)? How does it differ from Bayesian inference?
- Why is randomization important in experimental setups?
- What is selection bias and how do you avoid it?
- Given a left-skewed distribution with median 60, what can we conclude about mean and mode?
- You flip a coin 10 times and observe only one head. What is the null hypothesis and p-value for testing fairness?
- You are testing hundreds of hypotheses with t-tests. What considerations would you take?
- What conditions must be satisfied for CLT to hold?
- What is skewness? Discuss two methods to measure it.
- You sample from uniform distribution [0, d] n times. What is your best estimate of d?
- Discuss Chi-square, ANOVA, and t-test.
- How do you calculate blended mean and standard deviation from K subsets?
- What is the relationship between significance level and confidence level?
- What is the Law of Large Numbers and how is it used in data science?
- What is the difference between a confidence interval and a prediction interval?
- Explain long-tailed distributions. Why are they important in classification/regression?

---

### 13. Applied ML & Business Problems

**Questions**
- ⭐ How would you design a recommendation system to suggest books to users?
- If Amazon wants to send marketing emails to potential customers, how would you model this?
- How would you model a warehouse inventory problem?
- How would you measure the effectiveness of extra pay for delivery drivers during peak hours?
- Create a function `rain_days` to calculate the probability of rain on the nth day (Markov chain).
- Propose machine learning methods for two real-world use cases.
- Give an example of how forecasting is applied in machine learning.
- Can you walk me through building a machine learning model from scratch?

---

## ML Design

Design end-to-end ML systems at scale. Focus on problem framing, data pipelines, model selection, and deployment.

### Framework for ML System Design

1. **Clarify Requirements**
   - What is the business objective?
   - What are the constraints (latency, throughput, cost)?
   - What data is available?

2. **Problem Formulation**
   - Frame as ML problem (classification, regression, ranking, etc.)
   - Define success metrics
   - Identify baseline approach

3. **Data Pipeline**
   - Data collection and storage
   - Feature engineering
   - Data validation and monitoring

4. **Model Development**
   - Model selection and architecture
   - Training infrastructure
   - Offline evaluation

5. **Deployment & Serving**
   - Model serving infrastructure
   - A/B testing strategy
   - Monitoring and alerting

6. **Iteration**
   - Feedback loops
   - Model retraining strategy
   - Handling data drift

### Common ML Design Questions

**Recommendation Systems**
- Design a recommendation system to suggest books/products to users
- Design YouTube/Netflix video recommendations
- Design a news feed ranking system

**Fraud & Anomaly Detection**
- Design a fraud detection system for marketplace transactions
- Design an anomaly detection system for logistics
- Design a spam detection system

**Search & Ranking**
- Design a search ranking system
- Design ad click prediction
- Ranking items for personalized recommendations

**NLP Systems**
- Design Alexa/voice assistant from scratch
- Design a sentiment analysis system
- Design a chatbot

**Computer Vision**
- Design an image classification system
- Design a face recognition system
- Design an object detection pipeline

**Forecasting & Prediction**
- Improving conversion prediction for retail
- Design a demand forecasting system
- Design a delivery time estimation system

### Key Considerations

| Aspect | Questions to Address |
|--------|---------------------|
| Scale | How many users/requests? Data volume? |
| Latency | Real-time vs batch? P99 requirements? |
| Freshness | How often to retrain? Online learning? |
| Cold Start | How to handle new users/items? |
| Explainability | Do we need interpretable predictions? |
| Fairness | Bias considerations? Protected attributes? |

---

## Resources

### Books
- "Designing Machine Learning Systems" by Chip Huyen
- "Machine Learning System Design Interview" by Ali Aminian
- "Deep Learning" by Goodfellow, Bengio, Courville

### Courses
- Stanford CS229 (Machine Learning)
- Stanford CS231n (Computer Vision)
- Stanford CS224n (NLP)
- Fast.ai Practical Deep Learning

### Practice
- LeetCode ML questions
- System design mock interviews
- Kaggle competitions

REMOVE_START
Describe briefly the hypothesis testing and p-value in layman’s term? And give a practical application for them ?
Given a left-skewed distribution that has a median of 60, what conclusions can we draw about the mean and the mode of the data?
What is the meaning of selection bias and how to avoid it?
Explain the long-tailed distribution and provide three examples of relevant phenomena that have long tails. Why are they important in classification and regression problems?
What is the meaning of KPI in statistics
Say you flip a coin 10 times and observe only one head. What would be the null hypothesis and p-value for testing whether the coin is fair or not?
You are testing hundreds of hypotheses, each with a t-test. What considerations would you take into account when doing this?
What general conditions must be satisfied for the central limit theorem to hold?
What is skewness discuss two methods to measure it?
You sample from a uniform distribution [0, d] n times. What is your best estimate of d?
Discuss the Chi-square, ANOVA, and t-test
Say you have two subsets of a dataset for which you know their means and standard deviations. How do you calculate the blended mean and standard deviation of the total dataset? Can you extend it to K subsets?
What is the relationship between the significance level and the confidence level in Statistics?###
What is the Law of Large Numbers in statistics and how it can be used in data science ?
What is the difference between a confidence interval and a prediction interval, and how do you calculate them?

Supervised and unsupervised learning algorithms
Bias–variance trade-off
Regularization techniques
Feature engineering strategies
Loss functions and objective design
Model evaluation metrics (AUC, precision/recall, RMSE, NDGC, etc.)
Hyperparameter tuning
REMOVE_END

## ML Design

- Design scalable systems for data processing and model training
- design Alexa from scratch
- recommender system Fraud detection/Anomaly detection  Or vision/NLP
- Designing an anomaly detection system for Amazon Logistics
Improving conversion prediction for Amazon Retail
Identifying fraud in marketplace transactions
Ranking items for personalized recommendations