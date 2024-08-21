# Generate All Paths in a Matrix Top-Left To Right Bottom
# this is done using DFS recursively
# 
# first we need to check if the current index [i][j] is valid
# then check if we can move left/right/diagnonally
# else backtrack

# Finding all possible paths from [0][0] position 
# of a matrix to [n-1][n-1] position of a matrix

def findPaths(mat , path, i, j):
    r, c = len(mat), len(mat[0])

    # destination reached
    if i == r-1 and j == c-1:
        print(path + mat[i][j])
        return

    # explore
    path.append(mat[i][j])

    # move down
    if 0 <= i+1 <= r-1 and 0 <= j <= c-1:
        findPaths(mat, path, i+1, j)

    # move right
    if 0 <= i <= r-1 and 0 <= j+1 <= c-1:
        findPaths(mat, path, i, j+1)
    
    # move diagnol
    if 0 <= i+1 <= r-1 and 0 <= j+1 <= c-1:
        findPaths(mat, path, i+1, j+1)

    # invalid index or non-explorable the back tracking
    path.pop()
    return


matrix = []
n = int(input())

for i in range(n):
    row = list(map(int, input().split()))
    matrix.append(row)

path = []
findPaths(matrix, path, 0, 0)
