# File: Leetcode/Solutions/355_Design_Twitter.py

"""
Problem Number: 355
Problem Name: Design Twitter
Difficulty: Medium
Tags: Design, Hash Table, Heap (Priority Queue), Linked List, Neetcode 150
Company (Frequency): Amazon, Google, Facebook, Microsoft, Apple
Leetcode Link: <https://leetcode.com/problems/design-twitter/description/>

DESCRIPTION

Design a simplified Twitter where users can post tweets, follow/unfollow other users, and retrieve the 10 most recent tweets in the user's news feed. Implement:

* `postTweet(userId, tweetId)`
* `getNewsFeed(userId) -> List[int]` (10 most recent tweet ids from user + followees)
* `follow(followerId, followeeId)`
* `unfollow(followerId, followeeId)`

Function signature example (python):

* `class Twitter:`

  * `def postTweet(self, userId: int, tweetId: int) -> None:`
  * `def getNewsFeed(self, userId: int) -> List[int]:`
  * `def follow(self, followerId: int, followeeId: int) -> None:`
  * `def unfollow(self, followerId: int, followeeId: int) -> None:`

Approaches:

* Use a global timestamped list per user, and fetch recent tweets from user + followees using a max-heap (merge k sorted lists).
* Maintain follow sets and per-user linked list/array of tweets.
"""
