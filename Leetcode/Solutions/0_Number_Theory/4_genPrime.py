# generating prime numbers from 0 to 'n'


# initial approach => T.C. : O(n) x O(sqrt(n)) : O(nsqrt(n)) 
# for each number from 1 to n, 
# traverse and check for every number to be prime or not 

# Sieve of Eratosthenes
# T.C. : O(nlog(log(n)))
# first we generate a list of all numbers from 1 to n
# we first disregard 1 and 0 as they are not prime numbers
# then we tke the first prime i.e. 2 and mark all multiples 
# of 2 (startig from its square i.e. 4) as non-prime 
# this removes numbers such as 6, 8, 10, ...
# the next prime is 3, so we mark all multiples of 3 
# (startig from its square i.e. 9) as non-prime
# this removes numbers such as 6, 8, 10, ...
# finally when the square of a number becomes greater than n, 
# we get our prime numbers
def genPrime(n):
    primeLst = list(range(2, n+1))
    prime = 2
    while prime < n:
        for i in range(prime*prime, n+1, prime):
            if i in primeLst:
                primeLst.remove(i)
        prime = primeLst[primeLst.index(prime)+1]
    
    return primeLst



# DRIVER code
t = int(input())
while t > 0:
    print()
    t -= 1