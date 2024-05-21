# # Two pointer in Unsorted Array and Binary Search

# binary search in sorted array

import bisect

# T.C. = O(logn)
# S.C. = O(logn)    [recursive]
# S.C. = O(1)    [iterartive]
def bin_search(arr, left, right, key):
    while left <= right:
        mid = (left+right)//2
        if arr[mid] == key:
            return mid
        elif arr[mid] < key:
            left = mid+1
        else:
            right = mid
    return -1


arr = [ 25, 35, 80, 96, 200, 500, 850, 999 ]
key = 25

print("position : ", bin_search(arr, 0, len(arr)-1, key)+1)

# using python in-built functions
print("position : ", bisect.bisect_left(arr, key, 0, len(arr))+1)





# # find a pair whose sum is equal to target k **unsorted array

def findTargetPair(arr, target):
    st = set()
    for i in range(len(arr)):
        comp = target - arr[i]
        if comp in st:
            return (comp, arr[i])
        else:
            st.add(arr[i])

arr = [ 5, 100, 50, 10, 30, 5, 7, 85, 90, 100 ]     # unsorted list
target = 17

print("the pair of nums to produce, {} is {}".format(target, findTargetPair(arr, target)))