# Introduction to Blockchains

This chapter covers the basics of blockchains and their applications. It introduces the concept of blockchains, their structure, and how they are used in cryptocurrencies and other decentralized systems.

## Topics Include

- Lecture 1: Introduction to Blockchains

## Reading

- NBFMG Chapter 0

## Important Links

- [Video Lecture 1](https://wse.zoom.us/rec/share/EyHyN_S_Zs22WupwkbDdckOonVQ1gstyu_yOZ9a0wbJq5e1_6byHQc5oN_wecPc.x7ANzUK8a0oRqtTX?startTime=1724689056000)

## Notes

- 1980s when we started seeing digital cash
  - cannot convert bills to digital cash because of double spending problem
  - solution to double spending
    - online trusted third party (star policy graph)
    - offline computers that never misbehave (eg BOA e-ATM cards)
  - problems with online cash
    - privacy
    - fraud
    - security
    - centralization
    - robustness
    - double spending
  - older electronic technologies
    - e-cash
    - SET
    - Liberty Reserve / e-gold
- 2008 advent of Bitcoin
  - decentralized
  - no central authority
  - no single point of failure
  - no single point of control
  - no single point of trust
  - no single point of vulnerability
  - no single point of censorship
  - no single point of failure
  - no single point of attack
- Consensus needed for decentralized systems
  - compress database into a serializer form (like a string, or chain) that can be agreed on by all parties
  - New Data Structure => Blockchain, divide our huge database into ordered blocks
  - new blocks can only be added to the end of the chain and the chain is immutable
- Structure of Bitcoin
  - trnasactions are stored in blocks
  - blocks are linked together in a chain using cryptographic hashes
  - a hash function is a one-way function that takes an input and produces a fixed-size output (called digest)
  - hash functions are collision resistant (hard to find two inputs that produce the same output)
  - each block contains a hash of the previous block
  - The transactions are not checked for validity, only the blocks are checked by recursively checking the hash of the previous block till the genesis block (first block)
- Limitations of Blockchain
  - scalability, VISA performs 10k-140k transactions per second, Bitcoin performs 7-10 transactions per second
  - Psudo-anonymity, not truly anonymous. Each account identifier is random number
- Features of Ethereum
  - Smart Contracts, self-executing contracts with the terms of the agreement between buyer and seller being directly written into lines of code
