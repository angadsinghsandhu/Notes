# check if the given number is a power of 2

# T.C. = O(1)
def isPow2(n):
    if n<1:
        return False
        
    x = n
    y = not(n & (n-1))  # if n is a power of 2, y=1
    return (x and y)    # checking if x is even

num = int(input())
print(isPow2(num))