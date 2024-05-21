# Finding all divisos of a given number
# n = 24
# divisors = [1, 2, 3, 4, 6, 8, 12, 24]

from math import *

# T.C. : O(n)
def getDiv(n):
    divs = [1]
    for i in range(2, n//2+1):
        if n%i == 0:
            divs.append(i)
    divs.append(n)

# T.C. : O(root(n))
def getDiv2(n):
    divs = set()
    for i in range(1, int(sqrt(n))+1):
        if n%i == 0:
            divs.add(i)
            divs.add(n//1)
    return list(divs)
    

# DRIVER code
t = int(input())
while t > 0:
    n = int(input())
    print("the divisors of %d are : %s".format(n , getDiv(n)))
    t -= 1