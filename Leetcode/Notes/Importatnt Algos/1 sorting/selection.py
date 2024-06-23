"""
selection_sort.py
-----------------
This module implements the Selection Sort algorithm, which is a simple comparison-based sorting algorithm.
The algorithm sorts an array by repeatedly finding the minimum element from the unsorted part and moving it to the beginning.
This process is repeated for each position in the array until the entire array is sorted.

Description and Analysis:
- Space Complexity: O(1). Selection Sort is an in-place sorting algorithm, requiring only a minimal, constant amount of additional space for its operations.
- Time Complexity:
  - Best, Average, and Worst Case: O(n^2). The time complexity is quadratic for all cases because the algorithm always makes n-1 comparisons for each of the n elements in the list, regardless of the initial order of the elements.
- In-Place or Out-of-Place: Selection Sort is an in-place sorting algorithm, as it rearranges the numbers within the array itself without requiring additional memory that scales with the input size.
"""

def selection_sort(arr):
    """
    Sorts an array using the selection sort algorithm.
    
    Parameters:
    arr (list): The list of elements to be sorted.
    
    Returns:
    list: The sorted list.
    """
    n = len(arr)
    # Traverse through all elements in the array
    for i in range(n):
        # Find the minimum element in the remaining unsorted part of the array
        min_idx = i
        for j in range(i+1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        
        # Swap the found minimum element with the first element of the unsorted part
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    
    return arr

# Example usage
if __name__ == "__main__":
    sample_array = [64, 25, 12, 22, 11]
    sorted_array = selection_sort(sample_array)
    print("Sorted array is:", sorted_array)
