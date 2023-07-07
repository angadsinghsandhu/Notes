# DP with 2D Tabulation
# Unique Path

# here the inputs are given by the user that come out to be the size of the DP matrix
# let us take an inut of 3 and 2, hece creating a DP matix o size 3x2

# hence we have to output the number of path from the top-left 
# [0, 0] position to the bottom-right position [2, 1] (no diagnal movement allowed)

def printMat(m):
    for i in range(len(m)):
        print(m[i])

r, c = map(int, input().split())
dp = [ [0]*c for i in range(r) ]


# T.C. : O(n^2)
for i in range(r):
    for j in range(c):
        # move either right or down
        if i==0 or j==0:
            dp[i][j] = 1
        # move right or down
        else:
            dp[i][j] = dp[i-1][j] + dp[i][j-1]

printMat(dp)
print(dp[-1][-1])
