"""
insertion_sort.py
-----------------
This module implements the Insertion Sort algorithm, a simple and efficient comparison-based sorting algorithm.
Insertion sort iterates through the list, consuming one input element at each repetition, and growing a sorted output list.
Each iteration, insertion sort removes one element from the input data, finds the location it belongs within the sorted list, and inserts it there.
It repeats until no input elements remain.

The algorithm is efficient for small data sets and even more efficient for data sets that are already substantially sorted.

Description and Analysis:
- Space Complexity: O(1). Insertion Sort is an in-place sorting algorithm that only requires a constant amount of additional storage space.
- Time Complexity:
  - Best Case: O(n). Occurs when the input list is already sorted. Each element only needs to be compared with the element before it; no swaps are needed.
  - Average and Worst Case: O(n^2). Occurs when the list is randomly arranged or sorted in reverse. Each new element may need to be compared to all the sorted elements before it finds its correct position.
- In-Place or Out-of-Place: This is an in-place sorting algorithm, as it rearranges the numbers within the array without requiring additional memory that scales with input size.
"""

def insertion_sort(arr):
    """
    Sorts an array using the insertion sort algorithm.
    
    Parameters:
    arr (list): The list of elements to be sorted.
    
    Returns:
    list: The sorted list.
    """
    # Traverse through 1 to len(arr)
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        # Move elements of arr[0..i-1], that are greater than key, to one position ahead of their current position
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr

# Example usage
if __name__ == "__main__":
    sample_array = [22, 27, 16, 9, 3, 17]
    sorted_array = insertion_sort(sample_array)
    print("Sorted array is:", sorted_array)
