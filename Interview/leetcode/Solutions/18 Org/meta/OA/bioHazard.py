"""
File: bioHazard.py

A biological researcher is studying the interactions of various bacteria. Some of the bacteria are poisonous to others. All of the samples are arranged in a row, numbered consecutively from 1 to n in order. Given a list of which bacteria are poisonous to others, determine the number of intervals of samples that contain only samples that can coexist.

### Example

n = 3
allergic = [2, 1, 3]
poisonous = [3, 3, 1]

To determine relationships, the elements of:
- poisonous[0] -> allergic[0], so 3 is poisonous to 2
- poisonous[1] -> allergic[1], so 3 is poisonous to 1
- poisonous[2] -> allergic[2], so 1 is poisonous to 3

The bacteria are arranged as 1, 2, 3. An interval must be contiguous and the samples may not be reordered, like a subarray. All of the possible intervals are (1), (2), (3), (1, 2), (2, 3), (1, 2, 3). Since the poisonous bacteria need to be kept apart from those that are allergic to them, the only valid intervals are (1), (2), (3), (1, 2). No intervals can contain both bacteria 1 and 3 or bacteria 2 and 3. There are 4 valid intervals.

### Sample Input 0:
n = 3
allergic = [2, 1, 3]
poisonous = [3, 3, 1]

### Sample Output 0:
4

### Sample Input 1:
n = 4
allergic = [1, 2]
poisonous = [3, 4]

### Sample Output 1:
7

### Sample Input 2:
n = 5
allergic = [1, 2]
poisonous = [3, 5]

### Sample Output 2:
11
"""

class Solution:
    """
    The Solution class contains methods to compute the number of intervals of bacteria samples
    that can coexist without any poisonous interactions. The general approach is to process the
    poisonous relationships and, for each position in the sequence of bacteria, determine the
    earliest position where a conflict occurs. This allows us to calculate the number of valid
    intervals efficiently by keeping track of the minimum valid start position for each interval.
    """

    def bioHazard(self, n, allergic, poisonous):
        """
        Computes the number of intervals where all bacteria can coexist.

        Args:
            n (int): The number of unique bacteria types.
            allergic (List[int]): List where allergic[i] is allergic to poisonous[i].
            poisonous (List[int]): List of poisonous bacteria.

        Returns:
            int: The number of intervals made up only of bacteria that can coexist.

        Thought Process:
        - Since bacteria are arranged from 1 to n, we can process them in order.
        - We need to account for conflicts between bacteria.
        - For each position, we track the earliest position where a conflict could prevent
          an interval from starting.
        - We process each conflict and update an array that keeps track of conflict positions.
        - By iterating over each position and updating the minimum valid start position,
          we can calculate the number of valid intervals ending at each position.

        Time Complexity: O(n + m), where n is the number of bacteria and m is the number of conflicts.
        Space Complexity: O(n), due to the arrays used for conflict positions.
        """
        # Initialize an array to keep track of conflict positions
        conflict_positions = [0] * (n + 1)  # 1-based indexing

        # Process each conflict
        for a, p in zip(allergic, poisonous):
            pos_a = a
            pos_p = p
            max_pos = max(pos_a, pos_p)
            min_pos = min(pos_a, pos_p)
            conflict_positions[max_pos] = max(conflict_positions[max_pos], min_pos)

        min_valid_start = 0
        total_intervals = 0

        # Iterate over each position to compute the number of valid intervals
        for i in range(1, n + 1):
            min_valid_start = max(min_valid_start, conflict_positions[i])
            valid_intervals_ending_here = i - min_valid_start
            total_intervals += valid_intervals_ending_here

        return total_intervals

# Sample usage
solution = Solution()

# Sample Input 0
n0 = 3
allergic0 = [2, 1, 3]
poisonous0 = [3, 3, 1]
result0 = solution.bioHazard(n0, allergic0, poisonous0)
print(f"Sample Output 0: {result0}")  # Expected Output: 4

# Sample Input 1
n1 = 4
allergic1 = [1, 2]
poisonous1 = [3, 4]
result1 = solution.bioHazard(n1, allergic1, poisonous1)
print(f"Sample Output 1: {result1}")  # Expected Output: 7

# Sample Input 2
n2 = 5
allergic2 = [1, 2]
poisonous2 = [3, 5]
result2 = solution.bioHazard(n2, allergic2, poisonous2)
print(f"Sample Output 2: {result2}")  # Expected Output: 11
