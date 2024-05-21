## graph is data structure with vertices and edges
## Trees are like graphs, without cycles
## Trees are Undirected and Acyclic Graphs 


## weighted graphs and unweighted graphs
# here edges have costs associated to them 
# to from A to B and vicea-versa


## Directed Graph and Undirected Graph
# here edges are uidirectional and we can 
# only go from A to B and nor the other way around

## Graph Representation
# Adjacency List [ Space Complexity : O(V+E) ]
# [ Time Complexity (to check edge) : O(V) ]
# 
# A : [ B, F, C ]
# B : [  ]
# C : [ A, D, F, E ]
# D : [  ]
# E : [  ]

# Adjacency Matrix 
# [ Space Complexity : O(V^2) ]
# [ Time Complexity (to check edge) : O(1) ]
# 
#   A  B  C  D  E
# A    5        2   
# B
# C
# D
# E


## Tree Traversals
# Pre-Order, In-Order, Post-Order

## Graph Traversals
# DFS (Recursive Traversal using Stack) 
# BFS (Iterative Traversal using Queue)


## Scannig Adjacency List from user
# 
# 
# first input : (num vertices, num edges)
# all other inputs (newline separated) : (first node, second node) 
# [both nodes are connected to each other]
# 
# 7 9
# A B
# A C
# A F
# C E
# C F
# C D
# D E
# D G
# G F

from collections import defaultdict

graph = defaultdict(list)

v, e = map(int, input().split())

def printGraph():
    for v in graph:
        print(v, graph[v])

for i in range(e):
    u, v = map(str, input.split())
    
    # undirected graph
    graph[u].append(v)
    graph[v].append(u)
