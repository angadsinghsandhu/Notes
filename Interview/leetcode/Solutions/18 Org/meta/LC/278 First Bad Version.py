# FIRST BAD VERSION

# Problem number: 278
# Difficulty: Easy
# Tags: Binary Search
# Link: https://leetcode.com/problems/first-bad-version/

# The isBadVersion API is already defined for you.
# def isBadVersion(version: int) -> bool:

class Solution:
    """
    This problem is about finding the first bad version using the minimum number of API calls.
    Since each version after a bad one is also bad, we can use a Binary Search approach to 
    minimize the number of calls to the isBadVersion API.

    The idea is to search between versions 1 to n, dividing the search space by half
    with each iteration. Binary search ensures an optimal solution.

    Time Complexity: O(log n)
    Space Complexity: O(1)
    """

    def firstBadVersion(self, n: int) -> int:
        """
        Binary Search approach to find the first bad version.
        
        T.C. : O(log n) due to binary search
        S.C. : O(1) as we are using a constant amount of extra space
        """
        left, right = 1, n
        
        while left < right:
            mid = left + (right - left) // 2
            
            if isBadVersion(mid):
                right = mid  # Move towards the left half
            else:
                left = mid + 1  # Move towards the right half
        
        return left  # At the end, left will be at the first bad version
