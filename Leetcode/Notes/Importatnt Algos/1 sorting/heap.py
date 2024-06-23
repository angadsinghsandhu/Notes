"""
heap_sort.py
------------
This module implements the Heap Sort algorithm, an efficient sorting algorithm based on a binary heap data structure.
Heap Sort organizes the array into a binary heap structure, so it can repeatedly remove the largest element from the heap 
and then re-adjust the heap until the entire array is sorted.

Description and Analysis:
- Space Complexity: O(1). Heap Sort is an in-place sorting algorithm, requiring only a minimal, constant amount of additional 
  space beyond the original array for its operations.
- Time Complexity:
  - Best, Average, and Worst Case: O(n log n). The time complexity remains O(n log n) for all cases because the algorithm 
    always restructures the heap after removing the root element, which involves log(n) operations for n elements.
- In-Place or Out-of-Place: Heap Sort is an in-place sorting algorithm, as it rearranges the numbers within the array itself 
  without requiring additional memory proportional to the input size.
"""

def heapify(arr, n, i):
    """
    To heapify a subtree rooted with node i which is an index in arr[].
    n is size of heap.
    
    Parameters:
    arr (list): The array to be heapified.
    n (int): Number of elements in the heap.
    i (int): The index of the current root.
    """
    largest = i  # Initialize largest as root
    left = 2 * i + 1     # left = 2*i + 1
    right = 2 * i + 2    # right = 2*i + 2

    # See if left child of root exists and is greater than root
    if left < n and arr[largest] < arr[left]:
        largest = left

    # See if right child of root exists and is greater than root
    if right < n and arr[largest] < arr[right]:
        largest = right

    # Change root, if needed
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]  # swap

        # Heapify the root.
        heapify(arr, n, largest)

def heap_sort(arr):
    """
    The main function that implements HeapSort.
    
    Parameters:
    arr (list): The array to be sorted.
    """
    n = len(arr)

    # Build a maxheap.
    for i in range(n//2 - 1, -1, -1):
        heapify(arr, n, i)

    # One by one extract elements
    for i in range(n-1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]  # swap
        heapify(arr, i, 0)

# Example usage
if __name__ == "__main__":
    sample_array = [12, 11, 13, 5, 6, 7]
    heap_sort(sample_array)
    print("Sorted array is:", sample_array)
