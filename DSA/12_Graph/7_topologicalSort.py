## Topological Sort Algorithm (via source removal)
# Sorting Algo for Acyclic Directed Graph

# for U -> V, V comes after U [ this is called topological ordering/sort ]
# Indegree = Incoming edges
# Outdegree = Outgoing edges

# first we identify the node with the 
# minimum indegree (least amount of incoming edges)
# then we remove that node and all the assocted edges to and from it
# we identify the next node with minimum degrees and do the same
# then we remove all such nodes, the order in which the degrees 
# are removed is the toplogial sort

from collections import defaultdict
graph = defaultdict(list)

# were gonna implement it using BFS, hence
# T.C. : O(V+E)
def TopSort(graph, vertices):
    degree = [0]*vertices
    for node in graph:
        for adjNode in graph[node]:
            degree[adjNode] += 1

    bfs = [i for i in range(vertices) if degree[i] == 0]

    for node in bfs:
        for adjNode in graph[node]:
            degree[adjNode] -= 1

            if degree[adjNode] == 0:
                bfs.append(adjNode)

    return bfs

    

v, e = map(int, input().split())
for i in range(e):
    x, y = map(str, input().split())
    
    x = ord(x) - ord('A')
    y = ord(y) - ord('A')

    graph[x].append(y)

string = lambda x: chr(x + ord('A'))
print(list(map(string, TopSort(graph, v))))


# # Test Case
# 5 7
# A C
# A D
# B A
# B D
# C E
# D C
# D E

