# Zero Knowledge Proofs

This chapter covers Zero Knowledge Proofs, a method of proving the validity of a statement without revealing any information about the statement itself. It introduces the concept of Zero Knowledge Proofs, its history, and how it is used in decentralized systems.

## Topics Include

- Lecture 16: ZK proofs / scaling + Alternative Consensus I

## Reading

## Important Links

- Video Lecture 16 not available

## Notes

### Lecture 16: ZK proofs / scaling + Alternative Consensus I

- Scalability is a big issue in blockchain systems
  - Bitcoin transaction rate: 5-7 tx/sec
  - Bounded by block size (Segwit helps), TX size
  - All transactions must be globally verified, stored
  - Ethereum: 15 transactions per second if they’re small
  - Visa: 24,000/sec peak (150M/day globally)
  - WeChat 256,000/sec peak
- Why not just build faster computers?
  - Loss of decentralization
  - Eventually we saturate links, due to broadcast network
  - Replicated global state falls apart
  - Scaling is possible (see Visa, WePay etc.) but it requires dedicated, centralized servers
- Ideas for scaling bitcoin
  - Off-chain transactions (channels)
    - In current Bitcoin-style networks, every transaction appears on the blockchain
      - This allows the whole network to verify financial integrity
      - I.e., we can’t go off an do transactions elsewhere, accidentally/deliberately inflate the money supply
    - The network need to see every transaction so that it can verify that the money supply is not being inflated
    - Idea: If a transaction doesn’t affect anyone else (except for the parties willing to risk money), chain doesn’t need to see it
    - Simplest example (but centralized):
      - Multiple parties deposit money into an exchange
      - Exchange is just a centralized bank, so everyone can quickly transmit money by adjusting balances
      - Only withdrawals need on-chain transactions
    - Off-chain exchange example still risks loss of funds
      - If the exchange disappears, your money goes with it (e.g., QuadrigaCX)
      - The only benefit here is that the rest of the network can’t lose money, e.g., due to inflation
    - Channels: Step-by-Step
      - Step 1: Opening the Channel
        1. **Channel Setup**:
           - Two parties, **A** and **B**, each deposit a fixed amount of BTC (e.g., 1 BTC from each) into a joint transaction recorded on the blockchain.
           - This deposit transaction, or “funding transaction,” locks the initial funds in a multisig address that both parties control, ensuring neither can access the funds unilaterally.
        2. **Input and Output**:
           - The initial transaction (input) consists of the funds from both parties.
           - The output is a transaction that requires signatures from both **A** and **B** to unlock and spend the funds.
        3. **Signatures**: Both `A` and `B` must sign to authorize any transaction, providing a layer of security and mutual consent for each action taken within the channel.

      - Step 2: Updating the Balance
        1. **Incremental Payments**: Suppose **A** wants to pay **B** a certain amount (e.g., 0.2 BTC). They can update the balance without broadcasting to the blockchain.
        2. **Revised Balance**:
           - The new balance in this example would be **0.9 BTC** for **A** and **1.1 BTC** for **B**.
           - This balance update creates a new transaction version, signed by both **A** and **B**, representing the adjusted ownership of funds within the channel.
        3. **Version Control**:
           - Each time a new balance is agreed upon, the old balance is effectively invalidated. This is done by signing only the latest transaction, ensuring that only the most recent version can be broadcasted to the blockchain upon closure.

      - Step 3: Further Transactions
        1. **Additional Payments**: Further adjustments can be made as transactions occur within the channel. For instance, **B** might pay **A** back 0.5 BTC in a subsequent transaction.
        2. **Ongoing Updates**: With each transaction, a new version is created and signed by both parties, reflecting the updated balances.
        3. **Security and Mutual Consent**: Both parties must sign every transaction update, which prevents unilateral actions and ensures agreement on the transaction history.

      - Closing the Channel
        1. **Channel Closure**:
           - When **A** or **B** decides to close the channel, they broadcast the latest transaction version to the blockchain.
           - Only the most recent transaction is recorded, while all previous transactions within the channel are ignored.
        2. **Final Settlement**:
           - The final balance is then settled on the blockchain, and each party receives their respective amounts.
           - This process preserves blockchain resources, as only the initial and final transactions are recorded on-chain, while intermediate transactions remain off-chain.
        3. Dispute Resolution: If one party fails to cooperate in closing the channel, dispute resolution mechanisms can be employed to ensure a fair outcome.
           - What if someone posts an older, out-of-date version of the transaction? or if nobody signs the first "closure" transaction? How do we escape a payment channel in the worst case?
           - Either party posts the most recent version of the transaction to the blockchain (all older versions get ignored)

    - Making Channels Atomic
      - What happens in a channel `A` -> `B` -> `C` when one party fails to complete the transaction?
      - Answer: we need to make each channel transaction “atomically” depend on later transactions
      - We will have `C` release a password to allow payment from `B` -> `C`, and this will be the same password that allows `A` -> `B` transaction to go through
      - This is done using hash locks: each transaction embeds `h` such that to unlock and complete payment, payer must know a `p` such that `h = SHA2(p)`
      - Every channel in the chain will embed the same `h`
      - We will also use timelocks to allow the channels to close if someone along the channel refuses to update their transaction
      - The combination: hash timelocks (HTLC)

      - Benefits of Channels
        - **Efficiency**: Channels allow for multiple transactions without overloading the blockchain.
        - **Privacy**: Since intermediate transactions are off-chain, they remain private between the involved parties.
        - **Reduced Fees**: Transaction fees are minimized, as fewer transactions are recorded on-chain.

      - Limitations, Problems and Risks of Channels
        - **Counterparty Risk**: If one party fails to cooperate in closing the channel, disputes may arise.
        - **Liquidity Lock**: The funds deposited in the channel remain locked and are unavailable for other uses until the channel is closed.
        - Requires pairwise channels or lots of “locked up” liquidity in the network to support routing
        - This liquidity must be controlled by “online” signing keys, which makes it vulnerable to hacking
        - LN nodes can charge fees for participating in channels, but not clear how much people will pay
        - Routing is hard technically. You need to find a route with enough liquidity from A->Z (via B, C, D… etc.) and that implies a lot of knowledge and comp. effort
        - If parties along the channel fail (perhaps deliberately) there may be a costly “unwinding” of each independent channel back onto the chain
  - Sharding: divide the network into smaller pieces
  - New consensus algorithms
- Scaling up in Ethereum
  - rollups:  idea is to take a chain of many sequential transactions and “compress” them into a small value that can be verified on chain
    - `Optimistic rollup`: Lets do all the transactions off-chain without verifying them, and publish them to the world in the hope that theyre valid. If any transaction turns out to be invalid, we provide an incentivized mechanism to post a “proof” of invalidity.
      - Imagine we have a series of transactions and we want to prove they are all valid (in a short on-chain transaction)
      - We designate a third party (“bonded aggregator”) who locks up some currency (ETH) to pay for misbehavior
      - They collect all of the transactions people sent them, and execute the transaction off chain
      - For each TX they compute a Merkle tree over the TXes, and publish them too (Merkle root + transactions)
      - Finally they publish a single TX to the Ethereum chain, containing the Merkle root and some extra logic (—>)
      - This extra logic supports “fraud proofs” of two types:
        - If anyone can provide a proof that a single transaction in the chain is invalid, they can “punish” the aggregator
        - If anyone can provide a receipt that says their own TX was included in the chain, but it isnt in the rollup, then they can “punish” the aggregator
      - Punishment means “take some or all of the bond”
      - Gaurentees: (imagine the aggregator is malicious)
        - Example: they want to inject invalid transactions into an ERC20 contract that gives them money they shouldnt have
        - Benefit of the attack (to malicious aggregator) is potentially quite high! A single invalid TX can be worth millions USD
        - Downside is potential for getting caught, and being “slashed” (punished)
        - Key requirement is that the transactions in the rollup chain are published widely enough that some honest node will discover malicious behavior
        - Might need incentive mechanisms to make sure people validate the whole chain. But who keeps the validators honest?
        - How does this work in Ethereum L1 (on chain?)

    - `ZK rollup`: Lets use the magic of zero-knowledge (VC) to prove that we verified all the transactions, and produce a small proof. A different property, that uses the magic of “verifiable computation”, and cryptographic “proving technology”
      - Basic assumption is that we have a “proving system” that can take the inputs and outputs of some program, and produce a short proof that the program has been executed correctly
      - There are many older and emerging technologies for this: SNARKs, STARKs, IOPs, PCPs, etc. etc.
      - Key property is that if a proof exists, then the program is (almost certainly) correctly-executed
      - Aggregator (may be malicious) collects transactions from participants, writes a “receipt” for each TX it receives
      - Aggregator verifies each (sequential) TX using EVM, updates state
      - Aggregator submits a Merkle root over all the transactions, plus a short verifiable proof of the following: 
        1. Each TX verifies w.r.t. input state
        2. Merkle root is computed over all TXes and state
      - Blockchain (L1) simply verifies this proof

---

## Notes

### Lecture 16: Zero Knowledge Proofs, Scaling, and Alternative Consensus I

#### Scalability Challenges in Blockchain Systems

Scalability is a significant challenge for blockchain networks:

- **Bitcoin Transaction Rate**: Approximately 5-7 transactions per second (tx/sec).
  - Bounded by block size (SegWit helps) and transaction size.
  - All transactions must be globally verified and stored.

- **Ethereum**: Handles about 15 transactions per second if they are small.

- **Traditional Payment Systems**:
  - **Visa**: Peaks at around 24,000 tx/sec (150 million transactions per day globally).
  - **WeChat Pay**: Peaks at about 256,000 tx/sec.

**Why Not Just Build Faster Computers?**

- **Loss of Decentralization**: Faster, more powerful computers may centralize the network.
- **Network Saturation**: The broadcast nature of blockchain networks can saturate links.
- **Replicated Global State Issues**: Maintaining a replicated global state becomes impractical.
- **Centralization**: Scaling is possible (e.g., Visa, WePay) but requires dedicated, centralized servers.

#### Ideas for Scaling Blockchain Networks

##### Off-Chain Transactions (Payment Channels)

In current Bitcoin-style networks, every transaction appears on the blockchain to ensure financial integrity and prevent inflation of the money supply. However, if a transaction doesn't affect anyone else except the involved parties, the blockchain doesn't necessarily need to record it.

**Centralized Example**:

- Multiple parties deposit money into an exchange.
- The exchange adjusts balances internally, allowing quick transfers.
- Only deposits and withdrawals require on-chain transactions.
- **Risk**: If the exchange disappears or acts maliciously, funds can be lost (e.g., QuadrigaCX).

**Payment Channels**:

Payment channels allow two parties to transact multiple times off-chain and only record two transactions on-chain: opening and closing the channel.

**Step-by-Step Guide to Payment Channels**

**Step 1: Opening the Channel**

1. **Channel Setup**:
   - Parties **A** and **B** each deposit a fixed amount of Bitcoin (e.g., 1 BTC each) into a joint address controlled by both.
   - This is a **funding transaction** recorded on the blockchain.
   - The funds are locked in a multi-signature (multisig) address requiring both **A** and **B** to agree on transactions.

2. **Security**:
   - Neither party can unilaterally spend the funds.
   - Both parties must sign off on any transaction spending from this address.

**Step 2: Updating Balances Off-Chain**

1. **Incremental Payments**:
   - **A** wants to pay **B** 0.2 BTC.
   - They create an off-chain transaction reflecting the new balances:
     - **A**: 0.8 BTC
     - **B**: 1.2 BTC

2. **Signing Transactions**:
   - Both **A** and **B** sign this new transaction.
   - The old transaction is invalidated or discarded.

3. **Repeatable Process**:
   - They can continue updating the balances with new transactions as needed.

**Step 3: Closing the Channel**

1. **Channel Closure**:
   - Either **A** or **B** can decide to close the channel.
   - They broadcast the latest signed transaction to the blockchain.

2. **Final Settlement**:
   - The blockchain records the final balances.
   - Funds are unlocked, and each party receives their respective amounts.

**Dispute Resolution**:

- **Question**: *What if someone tries to post an older, out-of-date transaction? Or if one party refuses to cooperate in closing the channel?*
- **Answer**:
  - **Time-Locked Transactions**: Channels use time-locked transactions to allow either party to unilaterally close the channel after a certain period.
  - **Revocation Keys**: Old transactions can be invalidated using revocation keys shared between parties.
  - **Penalty Mechanisms**: If a party broadcasts an outdated transaction, penalty mechanisms can confiscate their funds.

**Benefits of Payment Channels**

- **Scalability**: Reduces the number of transactions on the blockchain.
- **Speed**: Transactions are instant since they are off-chain.
- **Lower Fees**: Minimizes transaction fees as only the opening and closing transactions are on-chain.
- **Privacy**: Off-chain transactions are not broadcasted to the entire network.

**Limitations and Risks of Payment Channels**

- **Liquidity Lock**: Funds are locked in the channel and cannot be used elsewhere until the channel is closed.
- **Counterparty Risk**: Requires both parties to remain online and cooperative.
- **Complexity**: Managing channels and ensuring security can be complex.
- **Scalability**: To transact with many parties, numerous channels or networked channels (like the Lightning Network) are needed.

##### Making Channels Atomic with Hash Time-Locked Contracts (HTLCs)

**Problem**:

- **Question**: *What happens in a multi-hop payment channel (e.g., **A** → **B** → **C**) if one party fails to complete their part of the transaction?*

**Solution**:

- Use **Hash Time-Locked Contracts (HTLCs)** to make payments atomic across multiple channels.

**How HTLCs Work**:

1. **Hash Locks**:
   - **C** generates a secret value `p` and computes its hash `h = SHA256(p)`.
   - **C** shares `h` with **B**, who shares it with **A**.

2. **Conditional Payments**:
   - **A** agrees to pay **B** if **B** can provide `p` such that `h = SHA256(p)`.
   - **B** agrees to pay **C** under the same condition.

3. **Execution**:
   - **C** reveals `p` to claim the payment from **B**.
   - **B** now knows `p` and can claim payment from **A**.

4. **Time Locks**:
   - Time constraints ensure that if a party doesn't reveal `p` in time, the funds are returned.
   - This prevents funds from being locked indefinitely.

**Benefits of HTLCs**:

- **Atomicity**: Ensures that either all parties execute the transaction or none do.
- **Trustless**: Parties don't need to trust intermediaries.

**Limitations of HTLCs**:

- **Complexity**: Adds complexity to the transaction process.
- **Routing Challenges**: Finding a route with sufficient liquidity can be difficult.

##### Limitations and Challenges of Payment Channels

- **Liquidity Requirements**: Requires sufficient funds to be locked up in channels.
- **Online Keys**: Funds are controlled by keys that must be online, increasing security risks.
- **Fee Structures**: Nodes may charge fees for routing payments, but optimal fee structures are still uncertain.
- **Routing Complexity**: Efficiently finding payment routes through the network is technically challenging.
- **Failure Handling**: If intermediate nodes fail, unwinding the transactions can be costly and complex.

#### Sharding: Dividing the Network

- **Concept**: Splitting the blockchain network into smaller, more manageable pieces called shards.
- **Goal**: To process more transactions by having different shards handle different subsets of transactions.
- **Challenges**: Ensuring security and consistency across shards.

#### New Consensus Algorithms

- Exploring alternative consensus mechanisms to improve scalability without sacrificing decentralization and security.

#### Scaling Solutions in Ethereum

##### Rollups: Compressing Transactions

Rollups aim to increase transaction throughput by executing transactions off-chain and submitting a summary to the main blockchain.

**Types of Rollups**:

1. **Optimistic Rollups**

   - **Concept**: Assume that off-chain transactions are valid and only check them if there is a dispute.
   - **Process**:
     - Transactions are executed off-chain.
     - The aggregator publishes the transaction data and a state root to the main chain.
   - **Fraud Proofs**:
     - If someone detects an invalid transaction, they can submit a fraud proof.
     - The aggregator must post a bond (stake) that can be slashed if they act maliciously.
   - **Incentivizing Honesty**:
     - Validators are incentivized to monitor off-chain transactions and challenge invalid ones.
     - **Question**: *But who keeps the validators honest?*
     - **Answer**:
       - Validators are motivated by rewards for detecting fraud.
       - Economic incentives align validator behavior with network security.

   - **Guarantees**:
     - Malicious aggregators risk losing their bond if they include invalid transactions.
     - Honest participants can trust that invalid transactions can be challenged and reversed.

2. **Zero-Knowledge (ZK) Rollups**

   - **Concept**: Use zero-knowledge proofs to verify that off-chain transactions are valid without revealing transaction details.
   - **Process**:
     - Aggregator collects transactions and computes a new state root.
     - A succinct cryptographic proof (e.g., SNARK or STARK) is generated to prove the validity of the state transition.
     - The proof and the new state root are submitted to the main chain.
   - **Advantages**:
     - Immediate finality: No need to wait for challenge periods as in optimistic rollups.
     - Enhanced security: Mathematical proofs guarantee correctness.
   - **Technical Requirements**:
     - Advanced cryptographic techniques.
     - Efficient proof generation and verification.

##### Comparing Optimistic and ZK Rollups

- **Optimistic Rollups**:
  - **Pros**:
    - Simpler to implement.
    - Compatible with existing smart contracts.
  - **Cons**:
    - Requires challenge periods (delay in transaction finality).
    - Depends on validators to detect fraud.

- **ZK Rollups**:
  - **Pros**:
    - Faster finality.
    - Strong security guarantees.
  - **Cons**:
    - More complex and computationally intensive.
    - Limited compatibility with certain smart contracts.
