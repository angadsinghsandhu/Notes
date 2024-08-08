# Staircase Problem
# 2 step
# 3 step

# (for 2 step staircase problem) we can take either 1 step or 2 steps forward, 
# so in how may ways can we reach the nth (given by user) step 

# # example 1 input
# 5 2

# # example 1 output
# 5
# array : [1, 1, 2, 3, 5]

'''
2 STEP STAIRCASE - BASE CASES
0 steps : [ 0 ] num ways => 1
1 steps : [ 1 ] num ways => 1
2 steps : [ 1+1, 2 ] num ways => 2
3 steps : [ 1+1+1, 1+2, 2+1 ] num ways => 3
4 steps : [ 1+1+1+1, 1+1+2, 1+2+1, 2+1+1, 2+2 ] num ways => 5
array = [1, 1, 2, 3]

3 STEP STAIRCASE - BASE CASES
0 steps : [ 0 ] num ways => 1
1 steps : [ 1 ] num ways => 1
2 steps : [ 1+1, 2 ] num ways => 2
3 steps : [ 1+1+1, 1+2, 2+1, 3 ] num ways => 4
4 steps : [ 1+1+1+1, 1+1+2, 1+2+1, 2+1+1, 2+2, 3+1, 1+3 ] num ways => 7
array = [1, 1, 2, 4]
'''

# T.C. : O(n)
def dynamic(n, step):
    arr = [1, 1, 2]

    for i in range(3, n):
        arr.append(sum(arr[-step:]))

    print(arr)

    return arr[-1]


values, steps = list(map(int, input("Enter number of Values and Step Size : ").split()))

print("max value that can be stolen is : {}".format(dynamic(values, steps)))