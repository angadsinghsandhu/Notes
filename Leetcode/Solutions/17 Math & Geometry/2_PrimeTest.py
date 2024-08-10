# Find if a number is prime or not.

from math import *

# normal approach
# T.C. : O(n)
def isPrime1(n):
    for i in range(2, n):
        if n%i == 0:
            return False
        else:
            return True

# otimized approach 
# T.C. : O(1) - O(root(n))
def isPrime2(n):
    if n==0 or n==1:
        return False
    if n==2 or n==3:
        return True
    if n%2==0 or n%3==0:
        return False

    for i in range(5, int(sqrt(n)+1)):
        if n%i == 0:
            return False
    else:
        return True

# DRIVER code
# Taking input from user
t = int(input())
while t > 0:
    n = int(input())
    print(isPrime1(n))
    print(isPrime2(n))
    t -= 1