# euclid algorithm
# time complexity: O(log(max(a,b)))
def gcd(a, b):
    if b == 0:
        return a
    else:
        return gcd(b, a % b)

# numerical solution
# time complexity: O(1)
def lcm(a, b):
        return a * b // gcd(a, b)

# DRIVER code
t = int(input())
while t > 0:
    m, n = map(int, input().split())
    print("the lcm of %d and %d is %d and the gcd is %d".format(m, n, lcm(m, n), gcd(m, n)))
