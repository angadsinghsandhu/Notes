# DP with 2D Tabulation
# Min Path Sum

# this is similar to the last problem of calculating the number 
# of unique paths in a matrix, just the difference 
# being that now instead of calculating all possiblities, we 
# try to calculate the length of the shortest path required 
# to reach from the top-left point to the bottom-right

def printMat(m):
    for i in range(len(m)):
        print(m[i])

# taking input
r, c = map(int, input("Enter Dimentions : ").split())
dp = []
for i in range(r):
    dp.append(list(map(int, input("Input to row {} : ".format(i+1)).split())))

# min cost (row-wise)
for j in range(1, r):
    dp[0][j] += dp[0][j-1] 

# min cost (col-wise)
for i in range(1, c):
    dp[i][0] += dp[i][0] 

# all other columns
for i in range(1, r):
    for j in range(1, c):
        dp[i][j] += min(dp[i-1][j], dp[i][j-1])

printMat(dp)

print(dp[-1][-1])

# # input
# 3 3
# 1 3 1
# 1 5 1
# 4 2 1

# # expected output
# 7

