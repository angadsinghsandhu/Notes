# House Robber Problem / Maximum Possible Stolen Value from N houses

# There are 'n' houses in a row, a robber steals from all of them, 
# but he cannot steal from adjacent homes, 
# what is the maximum value he can steal

# # example 1 input
# house values
# 6 7 1 3 8 2 4

# # example 1 output
# 19
# order : 6 -> 1 -> 8 -> 4

# # example 2 input
# house values
# 5 3 4 11 2

# # example 2 output
# 16
# order : 5 -> 11

# T.C. : O(n)
def dynamic(arr):
    n = len(arr)
    
    if n <= 0:
        print("Incoreecet Input, Retry")
        exit()
    
    if n == 0:
        return arr[0]

    # having to steal from 2 houses
    if n == 2:
        return max(arr)

    # having to steal from more than 1 house (use dp)
    arr[1] = max(arr[0], arr[1])    # initialize to larger value
    for i in range(2, n):
        arr[i] = max(arr[i-1], arr[i] + arr[i-2])

    return arr[-1]
    

values = list(map(int, input("Enter House Values : ").split()))

print("max value that can be stolen is : {}".format(dynamic(values)))
