## bitwise operators
# bitwise 'and' operator : '&'
# bitwise 'or' operator : '|'
# bitwise 'not' operator : '~'
# bitwise 'xor' operator : '^'
# bitwise 'shift-right' operator : '>>'
# bitwise 'shift-left' operator : '<<'


## "&" operator
# even numbers with 1
# 2 & 1 = 0
# 4 & 1 = 0
# 324 & 1 = 0
# odd numbers with 1
# 3 & 1 = 1
# 9 & 1 = 1
# 325 & 1 = 1

def evenOdd(n):
    if n&1 == 1:
        print("even")
    else:
        print("odd")


## ">>" and "<<" operator
## right-shift(>>) is division by 2
## left-shift(<<) is multiplication by 2
# 32 >> 2 = 8       [32 is divided by 2^2]
# 32 << 2 = 128     [32 is multiplied by 2^2]
# 200 >> 3 = 25     [200 is divided by 2^3]
# 200 << 1 = 400    [200 is multiplied by 2^1]



