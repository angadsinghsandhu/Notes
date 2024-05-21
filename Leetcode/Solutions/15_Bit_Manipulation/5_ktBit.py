# finding out if the kth bit (from right) 
# of the given integer in binary is 1 or not

def kthBit(n, k):
    print(str(bin(n))[2:])
    if n & (1 << (k-1)):
        print("SET")
    else:
        print("UNSET")

print()
n, k = map(int, input().split())
kthBit(n, k)
