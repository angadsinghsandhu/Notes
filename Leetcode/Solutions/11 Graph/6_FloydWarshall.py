## Floyd Warshall Algorithm
# All Source Shortest Path for Weighted Directed Graph
# this gives the shortest paths between all pairs of vertices (2^V pairs)

# if we had computed Dijkstras for each 2 vertices, the T.C. would be : O(V^logV)

# from collections import defaultdict
# graph = defaultdict(list)

INF = float('inf')

def printMatrix(graph):
    r, c = len(graph), len(graph[0])
    print()
    for i in range(r):
        for j in range(c):
            print(graph[i][j], end="\t")
        print()
    print()

def printMatrix_Anno(graph, loop1, loop2, loop3):
    r, c = len(graph), len(graph[0])
    print()
    for i in range(r):
        for j in range(c):
            if (i, j) == loop1:             # i, k
                print("🔴", end="")
            if (i, j) == loop2:             # k, j
                print("🟡", end="")
            if (i, j) == loop3:             # i, j
                print("🟢", end="")
            print(graph[i][j], end="\t")
        print()
    print()

# This is a DP Approach
# T.C. : O(V^3)
def FloydWarshall(graph):
    v = len(graph)

    for k in range(v):
        print("kkkk")
        for i in range(v):
            print("iiii")
            for j in range(v):
                print("jjjj")
                printMatrix_Anno(graph, (i, k), (k, j), (i, j))
                # print("---")
                # print("[(i, k), val] : [({}, {}), {}]".format(i, k, graph[i][k]))
                # print("[(k, j), val] : [({}, {}), {}]".format(k, j, graph[k][j]))
                # print("[(i, j), val] : [({}, {}), {}]".format(i, j, graph[i][j]))
                # print("---")
                
                # cost of temp path is less, then update 
                if graph[i][k] + graph[k][j] < graph[i][j]:
                    graph[i][j] = graph[i][k] + graph[k][j]


# getting number of vertices an dedges
v, e = map(int, input().split())

# creting graph
graph = [ [INF]*v for i in range(v) ]
for i in range(v): graph[i][i] = 0      # the distace from node to itself is 0 (no edge exists)

# getting input
for i in range(e):
    x, y, w = map(int, input().split())
    graph[x][y] = w

# before
printMatrix(graph)

# executing algo
FloydWarshall(graph)

# after
printMatrix(graph)

# # TEST case
# 4 4
# 0 3 10
# 0 1 5
# 1 2 3
# 2 3 1

