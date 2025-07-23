"""
bubble_sort.py
--------------
This module implements the Bubble Sort algorithm, which is a simple comparison-based sorting algorithm.
The algorithm repeatedly steps through the list, compares adjacent elements, and swaps them if they are in the wrong order.
This process is repeated until the list is sorted.

Description and Analysis:
- Space Complexity: O(1). Bubble Sort is an in-place sorting algorithm, requiring only a small, constant amount of additional space for its operations.
- Time Complexity:
  - Best Case: O(n). This occurs when the array is already sorted, and the algorithm makes one pass through the array to confirm no swaps are needed.
  - Average and Worst Case: O(n^2). These occur when the array is randomly arranged or sorted in reverse, respectively. Each element may need to be compared with every other element.
- In-Place or Out-of-Place: Bubble Sort is an in-place sorting algorithm, as it rearranges the numbers within the array itself without requiring additional memory scaling with input size.
"""

def bubble_sort(arr):
    """
    Sorts an array using the bubble sort algorithm.
    
    Parameters:
    arr (list): The list of elements to be sorted.
    
    Returns:
    list: The sorted list.
    """
    n = len(arr)
    # Traverse through all elements in the list
    for i in range(n):
        # Track whether a swap was made during this iteration
        swapped = False
        # Last i elements are already in place, no need to check them
        for j in range(0, n-i-1):
            # Compare the adjacent elements
            if arr[j] > arr[j+1]:
                # Swap if elements are in the wrong order
                arr[j], arr[j+1] = arr[j+1], arr[j]
                swapped = True
        # If no swap occurred, list is sorted
        if not swapped:
            break
    return arr

# Example usage
if __name__ == "__main__":
    sample_array = [64, 34, 25, 12, 22, 11, 90]
    sorted_array = bubble_sort(sample_array)
    print("Sorted array is:", sorted_array)
