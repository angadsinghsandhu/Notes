# Here we count the number of 1s in the binary representation in the representation of n

# T.C. = O(logn)
def cntOnes(n):
    num = n
    count = 0
    while(True):
        num, rem = map(int, divmod(num, 2))
        count += rem
        if num < 1: break

        ## bitwise implementation
        # count += 1
        # n = n & (n-1)
        # if num < 1: break

    return count


n = int(input())
print(cntOnes(n))
    