# Cryptocurrency Background

This chapter covers the basics of cryptocurrencies and their applications. It introduces the concept of cryptocurrencies, their history, and how they are used in decentralized systems.

## Topics Include

- Lecture 1: Cryptocurrency Background

## Reading

- NBFMG Chapter 1
- [Shafi+Mihir's Notes (Chapter 8 and 10)](https://cseweb.ucsd.edu/~mihir/papers/gb.pdf)

## Important Links

- [Video Lecture 1](https://youtu.be/FS0wrv77GYo)

## Notes

- cryptographic graph function (eg SHA-256)
  - it is a one-way function that takes an infinit input and produces a fixed-size output (called digest)
  - propreties of hash functions
    1. collision resistant (hard to find two inputs that produce the same output)
       - Pigeon hole principle: if you have more pigeons than pigeon holes, then at least one pigeon hole will have more than one pigeon
       - Collisions do exist, but they are hard to find
       - no efficient adversary can find x and y such that H(x) = H(y)
       - Bitcoin uses SHA-256, calculates 10^80 per second
       - Crytographic Adversaries: a probabilistic polynomial time algorithm (PPT)
       - collison resistance can formally be defined as follows: for any PPT A, the probability that A outputs x and y such that x != y and H(x) = H(y) is negligible
    2. pre-image resistant (hard to find an input that produces a given output)
       - it might be hard to find x given H(x)
       - but issues iarise when input space is small (eg Heads or Tails), this leads to brute force (enumeration) attacks
       - this can be solved by adding random bits to the input to increase the input space
       - pre-image resistance can formally be defined as follows: for any PPT A, the probability that A outputs x such that H(x) = y is negligible
       - Theorum: Collision resistance implies pre-image resistance if the hash function is sufficiently compressing (random oracle)
    3. efficient to compute
- Commitment
  - a commitment scheme allows a party to commit to a value without revealing it
  - trying to "seal a value in an envelope", and later reveal the value
  - can be done using hash functions
  - (com, key) := Commit(msg) [seal the message, publish com, keep key secret]
  - match := Verify(com, key, msg)
  - Security properties
    1. hiding: given commitment (com), no PPT adversary can guess the message (msg) with non-negligible probability
    2. binding: given commitment (com), no PPT adversary can find two messages (msg1, msg2) that both of their verifications are true
    3. collision resistance: the committer cannot find two messages that hash to the same value
- Random Oracle
  - A random oracle is a theoretical black box that responds to every unique query with a truly random response chosen uniformly from its output domain
- SHA-256 structure
- Hash Pointers and Data Structures
  - linked list with hash pointers
    - hash of the previous block
    - tamper-evident log
  - binary tree with hash pointers (Merkle Tree)
    - hash of the left child
    - hash of the right child
    - hash of the parent
- Digital Signature
  - can be used to sign a message, can only be signed you (private key), can be verified by anyone (public key)
  - signatures are tied to a document, cannot be reused or cut and pasted to another document
  - even if someone has your public key, they cannot forge your signature
  - inteface
    - (sk, pk) := KeyGen(r)
    - sig := Sign(sk, msg)
    - isValid := Verify(pk, msg, sig)
  - reuirements for signatures
    1. correctness: if (sk, pk) := KeyGen(r), then for all msg, isValid := Verify(pk, msg, Sign(sk, msg)) == true
    2. unforgeability: for any PPT adversary, the probability that the adversary outputs a valid signature for a message that was not signed by the signer is negligible (chosen message attack)
    3. non-repudiation: the signer cannot deny signing the message
    4. non-transferability: the signature cannot be transferred to another document
- notes
  - algorithms are randomized: need a good source of randomness. bad randomness can reveal secret key
  - fun trick: sign a hash pointer. signature "covers" the entire structure
  - Bitcoin uses ECDSA (Elliptic Curve Digital Signature Algorithm), a variant of Schnorr over elliptic curves
