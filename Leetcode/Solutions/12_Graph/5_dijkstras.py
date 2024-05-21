## Dijkstrastra's Algorithm
# Single Source Shortest Path for Weighted Directed Graph
# we have a source and a destination in this Algorithm

import heapq
from collections import defaultdict

# This is a Greedy Approach
# hence we try to find the minimum untill we reach destination
# greedy : SRC => MIN => MIN => MIN => DST (break i DST or Heap empty)
# T.C. : O(E*logV)
def Dijkstras(graph, src, dst):
    h = []

    # heap keeps a track record of all vertices ith cost
    # and updates them as well
    # heap pop will return verte with least cost
    path = [src]
    heapq.heappush(h, (0, src, path))


    while len(h)!=0:
        curr_cost, curr_v, path = heapq.heappop(h)
        if curr_v is dst: 
            print("path found from {} to {}, with cost : {} and path : {}".format(src, dst, curr_cost, path))
            break
        else:
            for neighbour, neighbour_cost in graph[curr_v]:
                tempPath = path.copy()
                tempPath.append(neighbour)
                heapq.heappush(h, (curr_cost+neighbour_cost, neighbour, tempPath))



graph = defaultdict(list)
v, e = map(int, input().split())
for i in range(e):
    x, y, w = map(str, input().split())
    graph[x].append((y, int(w)))    

src, dst = map(str, input().split())

Dijkstras(graph, src, dst)

# # Test Case
# 6 7
# A B 4
# A C 2
# B C 5
# B D 10
# C E 3  
# D F 11
# E D 4
# A D
