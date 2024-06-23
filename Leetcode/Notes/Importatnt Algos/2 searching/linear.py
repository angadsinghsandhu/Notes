"""
linear_search.py
----------------
This module implements the Linear Search algorithm, a straightforward method of finding a particular value in a list.
Linear Search checks each element of the list in order from the first to the last, looking for the specified target value.

Description and Analysis:
- Space Complexity: O(1). Linear Search is an in-place searching algorithm that requires minimal additional space.
- Time Complexity:
  - Best Case: O(1). Occurs when the target value is at the first position of the list.
  - Average and Worst Case: O(n). Average case occurs when the target is found around the middle of the list or not found, and worst case occurs when the target is at the end of the list or not present at all.
"""

def linear_search(arr, x):
    """
    Performs a linear search for a target value in a list.

    Parameters:
    arr (list): The list to search.
    x (any): The target value to search for.

    Returns:
    int: The index of the target value if found, otherwise -1.
    """
    for i in range(len(arr)):
        if arr[i] == x:
            return i
    return -1

# Example usage
if __name__ == "__main__":
    sample_array = [10, 23, 45, 70, 11, 15]
    target = 70
    result = linear_search(sample_array, target)
    if result != -1:
        print("Element is present at index", result)
    else:
        print("Element is not present in array")
