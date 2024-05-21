# Ajacency Matrix representation as Directed/Undirected, Weighted/Unweighted

def printMat(matrix):
    r, c = len(matrix), len(matrix[0])
    for i in range(r):
        for j in range(c):
            print(matrix[i][j], end=" ")
        print()


v, e = map(int, input().split)
matrix = [ [0]*v for i in range(v) ]


# undirected and unweighted graph
for i in range(e):
    u, v = map(str, input().split())

    u = ord(u) - ord('A')
    v = ord(v) - ord('A')

    matrix[u][v] = 1

    # for undirected graph (for directed graphs we do not have this line)
    matrix[v][u] = 1  

printMat(matrix)

# directed and weighted graph
for i in range(e):
    u, v, w = map(str, input().split())

    u = ord(u) - ord('A')
    v = ord(v) - ord('A')
    w = int(w)

    matrix[u][v] = w  

printMat(matrix)