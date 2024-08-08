# When to Buy/Sell Stock

# Given a array of n integers, where each interger 
# represents the price of a stock at a particular day 
# we have to find out, when should we buy that stock 
# and when to sell it to maximize profit 

# # example 1 input
# house values
# 7 1 5 3 6 4 

# # example 1 output
# 5                 [max profit]
# max subarray :    [ buy at 1, sell at 6 ]


# T.C. : O(n^2)
def brute_force(arr):
    n = len(arr)

    maxProfit = -1000000
    # generating all possible sub arrays
    for i in range(n):
        for j in range(i+1, n):
            diff = arr[j] - arr[i]
            # checking array with max sum
            if diff > maxProfit:
                maxProfit = diff

    return maxProfit

# T.C. : O(n)
def dynamic(arr):
    n = len(arr)
    maxProfit = 0
    minPrice = float('inf')

    for i in range(1, n):
        minPrice = min(minPrice, arr[i])
        maxProfit = max(maxProfit, arr[i]-minPrice)

    return maxProfit

values = list(map(int, input("Enter Array Values : ").split()))

print("max profit is : {}".format(brute_force(values)))
print("max profit is : {}".format(dynamic(values)))