# TODO: understand problem and do again

### **File:** `Leetcode/Solutions/1152_Analyze_User_Website_Visit_Pattern.py`

"""
Problem Number: 1152
Problem Name: Analyze User Website Visit Pattern
Difficulty: Medium
Tags: Array, Hash Table, Sorting
Company (Frequency): Amazon (82)
Leetcode Link: <https://leetcode.com/problems/analyze-user-website-visit-pattern/>

DESCRIPTION

You are given the browsing history of multiple users stored in three arrays:  
- `username[i]` represents the user who visited `website[i]` at time `timestamp[i]`.

The goal is to find a **sequence of three websites** that is the most popular among users.

A **pattern** is defined as any three websites visited in **chronological order**, not necessarily distinct.

The **popularity** of a pattern is determined by counting how many **unique users** visited that sequence in order.

Return the **most visited pattern** with the highest score.  
In case of a tie, return the **lexicographically smallest pattern**.

---

#### Example 1:
**Input:**
```plaintext
username = ["joe","joe","joe","jane","jane","jane"]
timestamp = [1,2,3,4,5,6]
website = ["home","about","career","home","cart","maps"]
```
**Output:**
```plaintext
["home","about","career"]
```

#### Example 2:
**Input:**
```plaintext
username = ["u1","u1","u1","u2","u2","u2"]
timestamp = [1,2,3,4,5,6]
website = ["a","b","a","a","b","c"]
```
**Output:**
```plaintext
["a","b","c"]
```

#### Constraints:
- `1 <= username.length <= 5000`
- `1 <= username[i].length <= 10`
- `0 <= timestamp[i] <= 10^9`
- `1 <= website[i].length <= 10`
- `username[i]` and `website[i]` consist of lowercase English letters.
- It is guaranteed that at least one user has visited at least three websites.

"""

from collections import defaultdict, Counter
from itertools import combinations

class Solution:
    """
    Thought Process:
    - We need to analyze users' browsing history and determine the most visited sequence of **three websites**.
    - First, **sort** the data by `timestamp` to ensure visits are in chronological order.
    - Then, **group visits by user**, keeping their visited websites in order.
    - Generate all **unique three-website sequences** per user.
    - Count occurrences of each sequence across all users.
    - Return the **most frequent sequence**, breaking ties **lexicographically**.

    Input:
        username: List[str] - List of usernames.
        timestamp: List[int] - Timestamps corresponding to user visits.
        website: List[str] - Websites visited at corresponding timestamps.

    Output:
        List[str] - The most frequently visited three-website sequence.
    """

    def mostVisitedPattern(
        self, username: list[str], timestamp: list[int], website: list[str]
    ) -> list[str]:
        """
        Approach:
        - Sort data by timestamp.
        - Create a **dictionary** mapping each user to their ordered list of visited websites.
        - Generate all unique **three-website sequences** per user.
        - Use a **counter** to track occurrences of each pattern.
        - Sort patterns by **frequency (descending) and lexicographically**.

        T.C.: O(n log n) + O(n) + O(u * m^3) ≈ O(n^3) in worst case.
        S.C.: O(n^3) in worst case.
        """
        # Step 1: Sort the data by timestamp
        sorted_events = sorted(zip(username, timestamp, website), key=lambda x: x[1])

        # Step 2: Map users to their chronological list of visited websites
        users_visits = defaultdict(list)
        for user, _, site in sorted_events:
            users_visits[user].append(site)

        # Step 3: Generate all unique three-website sequences per user
        pattern_count = Counter()
        for sites in users_visits.values():
            if len(sites) >= 3:
                unique_patterns = set(combinations(sites, 3))  # Generate all unique 3-sequences
                for pattern in unique_patterns:
                    pattern_count[pattern] += 1  # Count occurrences

        # Step 4: Sort by frequency (descending) and lexicographically
        return sorted(pattern_count.items(), key=lambda x: (-x[1], x[0]))[0][0]


# Run and print sample test cases
if __name__ == "__main__":
    solution = Solution()

    # Test cases
    print(solution.mostVisitedPattern(
        ["joe","joe","joe","jane","jane","jane"],
        [1,2,3,4,5,6],
        ["home","about","career","home","cart","maps"]
    ))  # Output: ["home","about","career"]

    print(solution.mostVisitedPattern(
        ["u1","u1","u1","u2","u2","u2"],
        [1,2,3,4,5,6],
        ["a","b","a","a","b","c"]
    ))  # Output: ["a","b","c"]