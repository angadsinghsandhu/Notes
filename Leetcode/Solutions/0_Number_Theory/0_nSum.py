# Find sum of 'n' numbers.
# n = 5
# 1+2+3+4+5 = 15

# T.C. : O(1)
def sum1(n):
    return n*(n+1)//2

# T.C. : O(n)
def sum2(n):
    sum = 0
    for i in range(1, n+1):
        sum += i
    return sum

# DRIVER code
t = int(input())
while t > 0:
    n = int(input())
    print("the sum output of %d is : %d".format(n ,sum1(n)))
