# Kadane's Algo and Counting Bits

# This is a very common Interview Question, 
# we do not directly take the DP approach, 
# first we take the direct approach, then we 
# make our approach more efficient and them we use DP ay last.

# Sample Question text : For a list from 1..to..n returen a list 
# of number of 1's in the binary representation of those numbers

# # Sample input
# 5 

# # Sample output
# [ 0 1 1 2 1 2 ]
# number of 1s in (i.e. 0 1 2 3 4 5)

# T.C. : O(n^2)
from itertools import count


def base_approach(n):
    res = []

    for i in range(n+1):                # n loop
        binary = str(bin(i)[2:])
        res.append(binary.count("1"))   # n loop

    return res

# T.C. : O(nlogn)
def eff_base_approach(n):
    res = []
        
    for i in range(n+1):
        count = 0
        while i:
            count += 1
            # using hamming code
            i = i & (i-1)

        res.append(count)

    return res

# T.C. : O(n)
def dp_approach(n):
    # base case
    res = [0]
    for i in range(1, n+1):
        res.append( res[i//2] + i%2 )
    
    return res

# taking input
n = int(input("Enter Num : "))

print(base_approach(n))
print(eff_base_approach(n))
print(dp_approach(n))