# traversla using adjacency list
# DFS and BFS

from collections import defaultdict, deque

# pre-/post-/in- order traversal in trees
# uses recursion and stack
# T.C. = O(V+E)
# S.C. = O(V)  [because of 'visited' dict]
def dfs(graph, start, visited, path):
    path.append(start)
    visited[start] = True

    for neighbor in graph[start]: # O(V+E)
        if not visited[neighbor]:
            path.append(neighbor)
            dfs(graph, neighbor, visited, path)

    return path

# level-order traversal in trees
# uses queue and iterarion
# T.C. = O(V+E)
# S.C. = O(V)  [because of 'visited' dict]
def bfs(graph, start, visited, path):
    queue = deque()

    path.append(start)
    visited[start] = True
    queue.append(start)

    while not queue.empty():
        node = queue.popleft()

        for neighbor in graph[node]:
            if not visited[node]:
                path.append(neighbor)
                queue.appnd(node)
                visited[node] = True 

    return path


# creating graph
graph = defaultdict(list)

# taking number of vertices and edges
v, e = map(int, input.split())

# greating ajacency list of graph
for i in range(e):
    x, y = map(str, input.split())
    graph[x].append(y)
    graph[y].append(x)

start = 'A'

# initializing ds for dfs
visited_dfs = defaultdict(bool)
path_dfs = []
traversed_path_dfs = dfs(graph, start, visited_dfs, path_dfs)
print(traversed_path_dfs)

# initializing ds for bfs
visited_bfs = defaultdict(bool)
path_bfs = []
traversed_path_bfs = bfs(graph, start, visited_bfs, path_bfs)
print(traversed_path_bfs)

