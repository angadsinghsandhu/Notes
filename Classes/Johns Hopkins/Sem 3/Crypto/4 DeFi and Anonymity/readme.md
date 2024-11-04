# DeFi and Anonymity

This chapter covers Decentralized Finance (DeFi) and Anonymity, two important concepts in the world of cryptocurrencies. It introduces the concept of DeFi, its history, and how it is used in decentralized systems.

## Topics Include

- Lecture 10: Smart Contracts contd. & DeFi
- Lecture 11: DeFi applications
- Lecture 12: Etherium Applications / Finishing DeFi / Anonymity I
- Lecture 13: Ethereum Applications / Privacy / Anonymity II
- Lecture 14-15: Anonymity III and Privacy Cont'd (slides not available, in video)

## Reading

- [Jump/Oasis Exploit](https://www.blockworksresearch.com/research/we-do-a-little-counter-exploit)
- [More on Zero Knowledge](https://blog.cryptographyengineering.com/2014/11/27/zero-knowledge-proofs-illustrated-primer/)
- [Anonymity and Concurrency](https://arxiv.org/pdf/1911.09148.pdf)
- [Fast Byzantine Agreement](https://people.csail.mit.edu/silvio/Selected%20Scientific%20Papers/Distributed%20Computation/BYZANTYNE%20AGREEMENT%20MADE%20TRIVIAL.pdf)
- [Algorand](https://people.csail.mit.edu/nickolai/papers/gilad-algorand-eprint.pdf)
- (Optional) [Ouroboros (first version)](https://eprint.iacr.org/2016/889.pdf)

## Important Links

- [Video Lecture 10](https://wse.zoom.us/rec/share/VNvNFzGIuJ5l9R-ESa_lid9wJxAM5a1U9t68gSI5ArTObJXHVLPXn7jyLKKSEQU7.kS4ovBn9MmCbZ7WN?startTime=1727885103000)
- [Video Lecture 11](https://wse.zoom.us/rec/share/UmeFDazC22UWkF_-FuRDxbTDLZf4ZJgIr_YTGSrmw5xohl6eFXPVfBYkIS3kHRyH.lXEhXGU5QDv4PsUt?startTime=1728316622000)
- Video Lecture 12 not avaliable
- [Video Lecture 13](https://wse.zoom.us/rec/share/Ly-JfaBV_A_IUmjNRw_rLJ4lwsRl9oetVYycgA37PBy8mC1R6eCNuxkVd2Xmp62x.HMMmJYcKBBiF6jlD?startTime=1729094481000)
- [Video Lecture 14](https://wse.zoom.us/rec/share/-bDXUcXz4VLl04QRednRiUDrukG7piWD23iEC4Zrgv2yKowfUXOFQ5mHJwjH8I7H.riRjrpPMeytppzYu?startTime=1729526515000)
- [Video Lecture 15](https://wse.zoom.us/rec/share/RPza7AItokLUpXJnbAhGOkfqTaFs98EuoPn1Sjcd7kodzF7JtBgx4kLvONPNa5cZ.j2MNgDKzORHLk4ba?startTime=1729699356000)

## Notes

### Lecture 10: Smart Contracts contd. & DeFi

### Lecture 12: Ethereum Applications / Finishing DeFi / Anonymity I

#### Anonymity

- **Anonymity** in computer science combines **pseudonymity** (using a fake name or identifier) with **unlinkability** (making it hard to link different actions by the same user).
- For blockchain-based systems:
  - **Why Anonymous Cryptocurrencies?** Blockchain transactions are totally public, permanent, and traceable.
  - Without anonymity, privacy in cryptocurrencies can be **worse than in traditional banking**, as every transaction is openly visible.
- **Anonymous E-Cash**:
  - Introduced by **David Chaum** in 1982.
  - Uses **blind signatures**, a secure two-party computation method that allows creating digital signatures without the signer learning the content.
- **Pseudonymity vs. Anonymity** in Online Forums:
  - **Reddit**: Users create a **long-term pseudonym** (username).
  - **4chan**: Posts are made with **no attribution**, providing higher anonymity.

- **Unlinkability**:
  - Needed because many **Bitcoin services** require a real identity.
  - Linked profiles can be deanonymized through **side channels** or additional data.

- **Defining Unlinkability in Bitcoin**:
  - Hard to link different addresses or transactions to the same user.
  - Hard to link the **sender** of a payment to its **recipient**.

- **Quantifying Anonymity**:
  - **Anonymity Set**: The set of transactions an adversary cannot distinguish from the transaction in question.
  - To calculate the anonymity set:
    - Define the **adversary model**.
    - Consider what the adversary **knows**, **doesn't know**, and **cannot know**.

#### How to De-anonymize Bitcoin

- Bitcoin’s pseudo-anonymity is vulnerable to de-anonymization techniques:
  - **Creating New Addresses**: Although users can create new addresses, this doesn’t ensure unlinkability.
  - **Shared Spending**:
    - Spending multiple inputs in a single transaction (e.g., combining addresses) indicates **joint control**, which can link addresses.
  - **Clustering of Addresses**:
    - Analyzing clusters of linked addresses helps trace transaction patterns and identify users.
  - **Change Addresses**:
    - Bitcoin transactions often send change to a new address.
    - **Problem**: The "change address" can be detected and linked, reducing anonymity.
  - **Idioms of Use**:
    - Unique wallet software behaviors can reveal patterns.
    - Example: Wallets that use each address only once for change create identifiable patterns.
  - **Tagging Service Providers**:
    - Service providers in the Bitcoin network can be identified by their transaction patterns, revealing **high centralization**.
    - These tagged addresses can then be traced back to users.
  
- **From Services to Users**:
  1. **High Centralization**: Transactions often pass through centralized service providers, making them easier to trace.
  2. **Address-Identity Links**: Linking addresses to real identities is possible through forums and other public channels.

### Lecture 13: Ethereum Applications / Privacy / Anonymity II

#### Achieving Anonymity

- **Proofs of Work (PoW)**:
  - PoW is effective in proving computational effort, but **not ideal for privacy** because it reveals the **secret input** used in the computation.
  - In blockchain, **signing keys** are used to sign transactions, adding some level of privacy, but this is **not enough** to ensure anonymity.
  - **Problem with Sending the Witness (W)**:
    - Sending a witness to the verifier compromises **secrecy** and could be **expensive** in terms of bandwidth and computation, especially if the witness is large.

- **Solutions**:
  1. **Zero Knowledge (ZK) Proofs**:
     - Allows proving knowledge of a value without revealing it.
     - The **verifier learns nothing** about the input itself, only that the prover knows it.
  2. **Verifiable Computation (VC)**:
     - Enables outsourcing of computation to a third party, who then provides a proof that they completed the computation correctly.
     - Useful for **privacy and scalability**, as it’s cheaper to send a proof than the full computation.

- **Centralized System for Anonymity: Mixer**
  - Users **send coins to the mixer**, and the mixer redistributes them to different addresses over time.
  - **Purpose**: To obscure the origin of the coins, enhancing anonymity.

- **Problems with Mixers**:
  - **Trust Issues**:
    - The **centralized service** may not be fully trustworthy to keep the mappings between deposit and withdrawal addresses private.
    - The mixer could be **compromised** and reveal these mappings.
  - **Double Spending**:
    - A user could attempt to withdraw more than their deposited amount by using the same proof multiple times.

- **Fixes for Mixer Anonymity**:
  - Instead of using a simple **password or ticket** to prove entitlement, users should use a **ZK proof** that they possess a valid secret.
  - **Process**:
    1. When a user sends a coin to the mixer, they generate 2 **random secret keys (sk1 and sk2)**.
    2. The **hash of the concaternated keys** (H) is sent to the mixer along with the coins.
    3. To withdraw, the user provides the 2 secret keys, the keys are checked against the hash, and if we find a match, the user is allowed to withdraw. and sk2 is added to the **nullifier list** to prevent double spending.
  - **ZK Process**:
    1. **Generate Proof**: The user runs a program that verifies the hash of the secret keys is in the mixer's list.
    2. **Send sk2** to the mixer for double-spend prevention.
    3. For withdrawal:
       - The user provides a **ZK proof** showing that they know the secret key corresponding to a hash on the mixer’s list, without revealing the key itself.
       - The mixer checks the **nullifier list** (a list of previously spent keys) to prevent double spending.
       - The mixer adds the SK to the nullifier list upon successful withdrawal, ensuring the user cannot reuse the same proof.

### Lecture 14: Anonymity III and Privacy Cont'd

- **Goal**: To build a mixing pool that allows anonymous withdrawal using ZK Proofs without revealing the identity of the user, even to the operator.

#### Mixer Protocol

1. **Deposit Protocol**:
   - **User Actions**:
     - Generate two secret keys (sk₁, sk₂) and compute a hash (H) from them.
     - Deposit 1 ETH and H to the Mixer.
   - **Mixer Actions**:
     - Store each hash (H) in a list of notes.

2. **Withdrawal Protocol**:
   - **Objective**: To allow a user to withdraw their deposit without revealing which deposit corresponds to their withdrawal.
   - **Steps**:
     1. **Generate Proof**:
        - User runs a program (`withdraw_program`) that takes in (sk₁, sk₂) as input.
        - The program:
          - Verifies the hash of (sk₁, sk₂) is in the list of notes.
          - Checks sk₂ has not been used in a prior withdrawal.
          - Outputs `True` if the user is eligible to withdraw.
     2. **Send sk₂** to the Mixer for double-spend prevention.
     3. **Verify Non-Existence on Nullifier List**:
        - The Mixer checks sk₂ is not already on the **nullifier list** (a list of used keys).
     4. **Add sk₂ to the Nullifier List**:
        - Prevents future reuse of the same proof for double spending.

#### Security Analysis

- **Adversaries**:
  - **Non-Depositor Adversary**:
    - Without knowing sk₁ and sk₂, a non-depositor cannot produce a valid proof since it would require finding a pre-image for H, which is infeasible with a secure hash function.
  - **Double-Spending Depositor**:
    - If a depositor tries to use sk₂ twice, they will be blocked because sk₂ will already be on the nullifier list after the first withdrawal.

#### Implementing Variable Withdrawals and Change

- **Problem**: Original protocol limits users to withdrawing the exact amount they deposited.
- **Solution**: Introduce a "change" mechanism to allow partial withdrawals:
  - **Deposit**:
    - User deposits with a value V (e.g., 10 ETH), which is incorporated into the hash H.
  - **Withdrawal**:
    - User withdraws an amount less than or equal to V (e.g., 0.32 ETH).
    - The remaining balance is represented as "change," which is added back into the mixer as a new hash (new sk₁, sk₂, and remaining balance).
    - Verification checks:
      - **Withdraw Amount + Change = Original Deposit** to ensure integrity.
      - Change can be hidden within the hash to maintain privacy.

#### Additional Enhancements for Privacy

- **Merging and Splitting of Values**:
  - To handle different transaction sizes, users could merge small deposits or split large deposits within the mixing pool.
  - This creates a **UTXO model** similar to Bitcoin but with enhanced privacy due to ZK Proofs.

#### Practical Implementation with Smart Contracts: Tornado Cash

- **Tornado Cash**:
  - Uses a smart contract to implement mixing without a trusted operator.
  - Depositors send ETH to the contract, and a hash (commitment) of their secret keys is stored.
  - Withdrawal process:
    - Users provide a ZK Proof to the contract, showing they possess a valid commitment without revealing which one.
    - **Nullifier hashes** are used to prevent double-spending.
  - **Public and Private Data**:
    - Deposit and withdrawal amounts can be fixed (e.g., 10 ETH) or varied using the change mechanism.
    - The amount withdrawn is public, but the remaining change is hidden.

#### Limitations and Future Improvements

- **Fixed Deposit Amounts**:
  - Tornado Cash pools have fixed deposit amounts, limiting flexibility.
  - Variable deposit amounts can be implemented using change values but may reduce privacy if amounts are unique.
- **Incorporating "Joint-Split" Transactions**:
  - To improve utility, users could combine (merge) or split (subdivide) values within the mixer, similar to the Bitcoin UTXO model.

### Lecture 15: Anonymity III and Privacy Cont'd

#### Intuition for Zero-Knowledge Proofs

1. **Boolean Circuits**:
   - Any program with a finite run time can be represented as a **Boolean circuit**.
   - A Boolean circuit has input wires, logic gates (AND, OR, NOT), and output wires.
   - For ZK proofs, we focus on circuits that produce a single-bit output (e.g., `True` or `False`).

2. **Graph 3-Coloring Problem**:
   - A classic problem where each node in a graph is colored with one of three colors such that no two adjacent nodes share the same color.
   - Graph 3-coloring is **NP-complete** and equivalent to the **circuit satisfiability problem** (a concept used to show computational hardness in computer science).

3. **Reduction**:
   - A Boolean circuit can be converted into a graph, and its satisfying inputs can be converted into a coloring for that graph.
   - If we can prove that we know a valid 3-coloring for this graph, it implies we know a valid input that satisfies the Boolean circuit.

---

#### Protocol for Proving Knowledge of a 3-Coloring without Revealing it

1. **Physical Protocol Analogy**:
   - Imagine a warehouse with an uncolored graph drawn on the floor.
   - **Steps**:
     1. The prover (person with the coloring) colors the graph with three colors (e.g., red, green, blue) and covers each vertex with a "hat" to hide its color.
     2. The verifier (person checking) selects an edge and asks the prover to reveal the colors of its two endpoints.
     3. The prover uncovers the colors of the selected vertices.
   - **Verification**:
     - If the colors are different, the verifier gains a bit of confidence that the prover has a valid coloring.
     - Repeating this process many times with randomly chosen edges builds statistical confidence that the prover truly knows a valid 3-coloring.

2. **Probability and Repeated Testing**:
   - Each successful test (where the revealed colors differ) slightly increases the verifier's confidence.
   - With repeated random edge selections, the probability of catching a cheater (someone without a valid coloring) increases exponentially.

---

#### Digital Version of the Protocol

1. **Commitments with Hash Functions**:
   - Instead of physical hats, **hashes** are used to hide the colors of each vertex.
   - Each vertex’s color is hashed with a random number (salt) to prevent pre-image attacks (guessing the color based on limited options).

2. **Protocol Steps**:
   - **Prover**:
     1. Chooses a random color for each vertex and hashes it with a unique random value.
     2. Sends the hash commitments (representing covered colors) to the verifier.
   - **Verifier**:
     1. Chooses an edge at random and asks the prover to reveal the colors of its endpoints.
     2. The prover sends the color and salt values for the two selected vertices.
     3. The verifier re-computes the hashes and checks for consistency with the commitments.

---

#### Zero Knowledge and Privacy

- **Zero Knowledge**: The verifier only learns that the prover knows a valid coloring; they gain no information about the specific colors of any vertex.
- **Time Machine Analogy**:
  - Hypothetical scenario where a prover with no knowledge of a valid coloring could cheat by using a "time machine" to repeatedly retry tests until successful.
  - **Conclusion**: Since real verifiers cannot detect rewinding in practical protocols (e.g., virtual machines), they cannot distinguish between genuine proofs and time-machine-based cheating attempts.
  - This illustrates that no additional information is leaked to the verifier.

---

#### Efficient Zero-Knowledge Proofs

1. **Merkle Trees**:
   - Rather than sending all commitments individually, the prover can store commitments in a **Merkle tree** and send only the root.
   - For each challenge, the prover sends just the relevant commitments and paths in the Merkle tree to prove they belong to the tree.
   - This reduces the communication complexity, especially for large graphs.

2. **Verifiable Computation**:
   - Protocols are optimized to provide high confidence (catching cheaters with high probability) while minimizing data transfer.
   - Verifiable computation allows verifying the correctness of complex computations without re-running them, essential for large-scale applications (e.g., cloud computing).
