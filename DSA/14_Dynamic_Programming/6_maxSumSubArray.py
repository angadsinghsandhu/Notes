# Maximum Sum Sub-Array

# Given a array of n integers, we have to splice the 
# array to find the subarray that gives out the 
# maximim value on summission

# # example 1 input
# house values
# -2 -3 4 -1 -2 1 5 -3 

# # example 1 output
# 7                 [max sum]
# max subarray :    [ 4 -1 -2 1 5 ]


# T.C. : O(n^3)
def brute_force(arr):
    n = len(arr)

    maxSum = -1000000
    # generating all possible sub arrays
    for i in range(n+1):
        for j in range(i+1, n+1):
            sub = arr[i:j]
            # checking array with max sum
            if sum(sub) > maxSum:
                maxSum = sum(sub)

    return maxSum

# T.C. : O(n)
def dynamic(arr):
    n = len(arr)

    for i in range(1, n):
        arr[i] = max(arr[i], arr[i] + arr[i-1])

    return max(arr)

values = list(map(int, input("Enter Array Values : ").split()))

print("max value subarray is : {}".format(brute_force(values)))
print("max value subarray is : {}".format(dynamic(values)))