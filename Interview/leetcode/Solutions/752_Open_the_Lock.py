# TODO: revisit

# File: Leetcode/Solutions/752_Open_the_Lock.py

"""
Problem Number: 752
Problem Name: Open the Lock
Difficulty: Medium
Tags: Breadth-First Search, Graph, Hash Table, String
Company (Frequency): Google (10), Amazon (8), Facebook (6)
Leetcode Link: https://leetcode.com/problems/open-the-lock/description/

DESCRIPTION

You have a lock with 4 circular wheels. Each wheel has 10 slots: '0' to '9'. The wheels can rotate freely and wrap around. 

The lock initially starts at '0000'.

You are given a list of `deadends`, meaning if the lock displays any of these codes, it stops turning and you cannot open it.

Given a `target` representing the unlocking code, return the minimum number of moves required to open the lock, or `-1` if it's impossible.

---

#### Example 1:
**Input:**
```plaintext
deadends = ["0201","0101","0102","1212","2002"]
target = "0202"
```
**Output:**
```plaintext
6
```
**Explanation:**
A sequence of valid moves would be "0000" -> "1000" -> "1100" -> "1200" -> "1201" -> "1202" -> "0202".

#### Constraints:
- `1 <= deadends.length <= 500`
- `deadends[i].length == 4`
- `target.length == 4`
- `target` will not be in `deadends`.
- `target` and `deadends[i]` consist of digits only.
"""

from collections import deque
from typing import List

class Solution:
    """
    Thought Process:
    - This is a shortest path problem on an unweighted graph.
    - BFS (Breadth-First Search) is the optimal approach.
    - Each state (lock combination) can generate up to 8 new states.
    
    Input:
        deadends: List[str] - A list of dead-end states.
        target: str - The target combination to unlock.

    Output:
        int - The minimum number of moves required to reach the target, or -1 if impossible.
    """
    
    def brute_force_solution(self, deadends: List[str], target: str) -> int:
        """
        Approach:
        - Try all possible sequences of moves recursively.
        - This results in an exponential number of possibilities.
        
        T.C.: O(10^4) - Exponential in worst case.
        S.C.: O(10^4) - Large recursion depth due to backtracking.
        """
        return -1  # Brute force is infeasible for this problem.

    def optimized_solution(self, deadends: List[str], target: str) -> int:
        """
        Approach:
        - Use BFS to explore all possible lock combinations level-by-level.
        - Store visited states in a set to avoid re-exploring.
        - Stop searching when we reach the target.
        
        T.C.: O(10^4) - Worst case explores all 10,000 possible states.
        S.C.: O(10^4) - Space for queue and visited set.
        """
        def get_next_states(state):
            """Generates all possible states from the current state."""
            next_states = []
            state_list = list(state)
            for i in range(4):
                original_digit = state_list[i]
                
                # Decrease digit (wrap around)
                state_list[i] = '9' if original_digit == '0' else str(int(original_digit) - 1)
                next_states.append("".join(state_list))
                
                # Increase digit (wrap around)
                state_list[i] = '0' if original_digit == '9' else str(int(original_digit) + 1)
                next_states.append("".join(state_list))
                
                # Restore the original digit
                state_list[i] = original_digit
            
            return next_states

        if target == "0000":
            return 0
        deadend_set = set(deadends)
        if "0000" in deadend_set:
            return -1
        
        queue = deque([("0000", 0)])  # (state, steps)
        visited = set(["0000"])
        
        while queue:
            state, steps = queue.popleft()
            if state == target:
                return steps
            for next_state in get_next_states(state):
                if next_state not in visited and next_state not in deadend_set:
                    visited.add(next_state)
                    queue.append((next_state, steps + 1))
        
        return -1

# Run and print sample test cases
if __name__ == "__main__":
    solution = Solution()

    # Test case 1
    deadends1 = ["0201","0101","0102","1212","2002"]
    target1 = "0202"
    print(solution.optimized_solution(deadends1, target1))  # Output: 6

    # Test case 2
    deadends2 = ["8888"]
    target2 = "0009"
    print(solution.optimized_solution(deadends2, target2))  # Output: 1

    # Test case 3
    deadends3 = ["8887","8889","8878","8898","8788","8988","7888","9888"]
    target3 = "8888"
    print(solution.optimized_solution(deadends3, target3))  # Output: -1
