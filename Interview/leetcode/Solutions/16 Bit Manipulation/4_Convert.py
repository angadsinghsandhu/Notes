# convert int to binary

# 
def Int2Bin(n):
    return str(bin(n))[2:]

def Bin2Int(n):
    return int(n, 2)

print()
n = int(input())
print(Int2Bin(n))
print(Bin2Int(Int2Bin(n)))

