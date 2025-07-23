"""
binary_search.py
----------------
This module implements the Binary Search algorithm, an efficient method for finding a target value within a sorted array.
Binary Search compares the target value to the middle element of the array; if they are not equal, the half in which the target cannot lie is eliminated, and the search continues on the remaining half until the target is found or the search space is empty.

Description and Analysis:
- Space Complexity: O(1) for iterative implementation; O(log n) for recursive implementation due to call stack.
- Time Complexity:
  - Best Case: O(1). Occurs when the central element is the target.
  - Average and Worst Case: O(log n). The algorithm divides the search space in half with each step, reducing the amount of time needed to find the target logarithmically.
"""

def binary_search(arr, x):
    """
    Performs a binary search for a target value in a sorted list.

    Parameters:
    arr (list): The sorted list to search.
    x (any): The target value to search for.

    Returns:
    int: The index of the target value if found, otherwise -1.
    """
    low = 0
    high = len(arr) - 1

    while low <= high:
        mid = (low + high) // 2
        # Check if x is present at mid
        if arr[mid] == x:
            return mid
        # If x is greater, ignore left half
        elif arr[mid] < x:
            low = mid + 1
        # If x is smaller, ignore right half
        else:
            high = mid - 1

    return -1

# Example usage
if __name__ == "__main__":
    sample_array = [2, 3, 4, 10, 40]
    target = 10
    result = binary_search(sample_array, target)
    if result != -1:
        print("Element is present at index", result)
    else:
        print("Element is not present in array")
