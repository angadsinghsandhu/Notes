# generating 'n' Fibonacci Numbers

# Fibinacci using Recursion
# re-occrance relation : T(n) = T(n-1) + T(n-2)
# T.C. : O(2^n)
def fib_rec(n):
    if n==0 or n==1:
        return n
    else: return fib_rec(n-1) + fib_rec(n-2)

# global list for all test cases
FIBNUM = [0, 1]

# Fibinacci using DP
# re-occrance relation : T(n) = T(n-1) + T(n-2)
# T.C. : O(n)
# S.C. : O(n)
def fib_dp(n):
    # already computed
    if n < len(FIBNUM):
        return FIBNUM[n]

    # if not computed
    else:
        for i in range(len(FIBNUM), n+1):
            last = FIBNUM[-1]
            prevLast = FIBNUM[-2]
            FIBNUM.append(last+prevLast)
        return FIBNUM[n]
    

num = int(input("Enter Num : "))
print(fib_dp(num))
