"""
quick_sort.py
--------------
This module implements the Quick Sort algorithm, a highly efficient sorting algorithm based on the divide-and-conquer principle.
Quick Sort picks an element as a pivot and partitions the given array around the picked pivot. There are many different versions of quickSort that pick pivot in different ways:
1. Always pick the first element as pivot.
2. Always pick the last element as pivot.
3. Pick a random element as pivot.
4. Pick the median as the pivot.

The version implemented here uses the last element as the pivot.

Description and Analysis:
- Space Complexity: O(log n). This is due to the stack space taken up by recursive calls. The worst case space complexity is O(n).
- Time Complexity:
  - Best and Average Case: O(n log n). The array is divided into two roughly equal parts each time, leading to a logarithmic number of levels of recursion.
  - Worst Case: O(n^2). Occurs when the pivot element is always the smallest or largest element in the array, causing one of the recursive calls to process all remaining n-1 elements.
- In-Place or Out-of-Place: Quick Sort is an in-place sorting algorithm, as it rearranges the numbers within the array itself without requiring additional memory proportional to the array's size.
"""

def partition(arr, low, high):
    """
    This function takes the last element as pivot, places the pivot element at its correct position in sorted
    array, and places all smaller (smaller than pivot) to left of pivot and all greater elements to right
    of pivot.
    
    Parameters:
    arr (list): The array to be sorted.
    low (int): Starting index.
    high (int): Ending index.
    
    Returns:
    int: The index of the pivot element.
    """
    i = low - 1  # index of smaller element
    pivot = arr[high]  # pivot
    
    for j in range(low, high):
        # If current element is smaller than or equal to pivot
        if arr[j] <= pivot:
            i = i + 1  # increment index of smaller element
            arr[i], arr[j] = arr[j], arr[i]
    
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1

def quick_sort(arr, low, high):
    """
    The main function that implements QuickSort.
    
    Parameters:
    arr (list): The array to be sorted.
    low (int): Starting index.
    high (int): Ending index.
    """
    if low < high:
        # pi is partitioning index, arr[pi] is now at right place
        pi = partition(arr, low, high)
        
        # Separately sort elements before partition and after partition
        quick_sort(arr, low, pi - 1)
        quick_sort(arr, pi + 1, high)

# Example usage
if __name__ == "__main__":
    sample_array = [10, 7, 8, 9, 1, 5]
    quick_sort(sample_array, 0, len(sample_array) - 1)
    print("Sorted array is:", sample_array)
