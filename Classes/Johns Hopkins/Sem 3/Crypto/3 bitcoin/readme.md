# Bitcoin

This chapter covers Bitcoin, the first and most well-known cryptocurrency. It introduces the concept of Bitcoin, its history, and how it is used in decentralized systems.

## Topics Include

- Lecture 3: Towards Bitcoin I
- Lecture 4: Towards Bitcoin II
- Lecture 5: Mechanics of Bitcoin I
- Lecture 6: Mechanics of Bitcoin II

## Reading

- NBFMG Chapter 1, 2, 3
- [Shafi+Mihir's Notes (Chapter 8 and 10)](https://cseweb.ucsd.edu/~mihir/papers/gb.pdf)
- [Merkle-Damgard Transformation](https://github.com/PratyushRT/blockchainsS21/blob/master/Papers/Merkle-Damgard.pdf)
- [PSL Impossibility](https://lamport.azurewebsites.net/pubs/reaching.pdf)
- [Paxos](https://lamport.azurewebsites.net/pubs/lamport-paxos.pdf)
- [Bitcoin Whitepaper](https://bitcoin.org/bitcoin.pdf)
- [Qureshi: Bitcoin P2P Network](https://nakamoto.com/bitcoins-p2p-network/)
- (Optional) [Analysis of Bitcoin](https://eprint.iacr.org/2016/454)
- (Optional) [Pass-shelat: Micropayments](https://shelat.khoury.northeastern.edu/dl/micropay2.pdf)

## Important Links

- Video Lecture 3 not available
- [Video Lecture 4](https://wse.zoom.us/rec/share/kdTRzqg2YK0B_MHKqm5_rAeCVziEKiIV0XBni5gjXIP60dM-Gu3Al1XGXWNroRJi.gB85Q-L-lIZilVsO?startTime=1725897433000)
- [Video Lecture 5](https://wse.zoom.us/rec/share/0Gu87q0kotNhgW79mmcyMc3-ssNjDqbRGtzYR_VABHcA73MjBeMJXfbQEe9UMQxn.Iyia0FpMlhA8vZVp?startTime=1726070163000)
- [Video Lecture 6](https://wse.zoom.us/rec/share/ThOKUWb7hOEZb64edgK7fYjhxToDO1D5A3XYO1VL1aR3luM3hcpjEViKp9jo7RB5.qT1RKLY-PUtIyXCA?startTime=1726502450000)

## Notes

### Lecture 3: Towards Bitcoin I

- Bitcoin is a decentralized digital currency that allows peer-to-peer transactions without the need for a trusted third party.

### Lecture 4: Towards Bitcoin II

- fill/flood style P2P network
- Transaction is added and validated and sent to everyone else on the network
- Mempool: where transactions are stored before they are added to the blockchain
- Bitcoin is a immutable block of chains that are linked together by hashes, where the head hash represents the entire blockchain
- The goal is to get the network to agree on a hash that represents the entire blockchain
- Consensus: extending the blockchain
  - Every node has a copy of the blockchain
  - Mempool has loose transactions
  - Loose transactions need to be put in order in the blockchain
  - Block proposal: a node proposes a block to be added to the blockchain
  - Consensus protocol: a way for nodes to agree on the order of transactions
  - Sybil Attack: Voting is a bad protocol for consensus because it is slow and can be manipulated
  - Bitcoin consensus:
    - Introduces incentives
    - Embraces randomness
  - Randomly pick a node to propose a block, the other nodes accept (extend)/reject (continue from somewhere else) this block
  - Nodes are given the chance to propose a block based on the amount of work (computation) they have done, so that subdividing compute power is not beneficial
  - Amount of work of the proposed block depends upon the structure of the hash of the previous block
  - Hashes are 256 bits long, so the probability of finding a hash that starts with a "n" number of zeros is 2^-n
  - The first person to find a hash that starts with a certain number of zeros gets to propose a block
  - Other nodes can verify the hash by hashing the block and checking if it starts with the same number of zeros
  - Block hash problem: Proof of Work (PoW) or mining
  - Nonce (number only used once): a random number that is added to the block to change the hash
  - Mining a block is supposed to take 10 minutes, adding more compute power in the network will decrease the time it takes to mine a block
  - PoW is stateless, to make sure that new blocks are added at a cap of 10 minutes, the difficulty of the hash is adjusted every 2016 blocks
  - Every 10 minutes, bitcoin does 2^64 hashes
  - [Algorithm for adjusting difficulty]
  - Collisions (fork) (Blocks mined at the same time)
    - Mutliple valid chains might be present at the same time
    - According to protocol, the longest chain is the valid chain
    - Forks dont last for very long, as the chain with more compute power will grow faster, eventually becoming the longest chain
    - Transactions in the last few blocks are not considered final
    - Finality: Final agreement on the state of a system
    - Bitcoin does probabilistic finality. It does not ahve perfect finality
    - we have to wait for a few blocks to be mined to be sure that the transaction is final and the longest chain is the valid chain

### Lecture 5: Mechanics of Bitcoin I

- difficulty level (T) is inversely proportional to the difficulty of mining a block (number of zeros in the hash)
- condition for a block to be valid:
  1. Timestamp must be valid (not too far in the future, not too far in the past)
  2. find the right nonce
  3. previous hash in the block needs to be connected to the previous valid block (or blockchain)
  4. every transaction in the block must be valid
- shorter forks are forgotten and their transactions are not considered valid (reorder process), these smaller forks are called orphan blocks
- bitcoin transactions
  - incentivise miners: transaction fees
  - total output transaction must sum up to be less than or equal to the total input transaction
  - The miners address hash is not mentioned in the transaction, but the miner can claim the transaction fees later
  - block reward: in addition to transaction fees, the miner gets a reward for mining a block
  - block reward is halved every 210,000 blocks (started as 50 BTC, now 6.25 BTC)
- Account Based ledger (not bitcoin)
  - Account balance is stored in the ledger
  - Transactions are stored in the ledger
  - Transactions are validated by checking the account balance
- Transaction based ledger (bitcoin)
  - Transactions are stored in the ledger
  - Transactions are validated by checking the previous transactions
  - The account balance is the sum of the previous transactions
  - transaction are referenced by the hash of the previous transaction
- Block size limit: 1MB [TODO]
- bitcoin transaction can have mutiple signatures, and the transaction is valid if the sum of the signatures is greater than the sum of the inputs
- users address in a block (pubKey) is stored as a hash of their public key
- Bitcoin transaction are more powerful (programmable money) than traditional transactions because they can execute scripts
- the inputs to the scripts are the outputs of the previous transactions saved as the `scriptPubKey` in the transaction
- Bitcoin scripts (`Scipt`: stack based language): output is 1 or 0 (True/False)
  - OP_DUP: duplicate the top stack element
  - OP_HASH160: hash the top stack element
  - OP_EQUALVERIFY: check if the top two stack elements are equal
  - OP_CHECKSIG: check if the signature is valid by hashing your `pubKey` and comparing it to the `sig`
  - OP_CHECKMULTISIG: check if the sum of the signatures is greater than the sum of the inputs
- `Script` language:
  - Built for bitcoin
  - simple, compact, stack-based
  - support for cryptographic operations
  - limits on time and space
  - no looping
  - 256 op_codes total (15 disabled, 75 reserved) (arithmatic, logical, flow control, stack manipulation, cryptographic)
- `sign` and `pubkey` get added to the stack first, then the operations are performed
- most nodes only accespt standard transactions
- 99.9% of operations are simple signature checks
- less than 0.01% operations are [todo]
- Proof of Burn: burning coins to prove that you have skin in the game
  - OP_RETURN: burn coins by sending them to an address that is not valid (arbitrary data)
  - arbitrary data is stored in the blockchain can be used to store data (NFTs etc.)
