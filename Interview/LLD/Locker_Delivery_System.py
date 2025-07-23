# TODO: new

# FILE: Leetcode/Solutions/Amazon/LLD/Locker_Delivery_System.py

'''
# Amazon's "Locker Delivery System" Problem

Below is a sample Python solution that follows the four steps approach. In this problem, you are given:
- A "city block" represented as an `m x n` matrix.
- A list of `(x, y)` coordinates for existing locker locations.

## Problem Interpretation & Approach

### Clarifying Questions:
- **Q:** What exactly should the system do?
  - **A:** Compute, for every block (cell) in the city grid, the Manhattan distance to the nearest locker.
- **Q:** What movements are allowed?
  - **A:** We assume movement is allowed in four directions (up, down, left, right).

### Assumptions:
- The city is represented as a grid with `m` rows and `n` columns.
- Locker coordinates are given as a list of `(x, y)` tuples.
- If a cell contains a locker, its distance is `0`.
- All cells are reachable via 4-directional movement.
- No obstacles exist in the grid.

### Short-Term Fix:
- Initialize distances for all locker cells.
- Use a multi-source Breadth-First Search (BFS) to calculate the shortest (Manhattan) distance from every cell to the nearest locker.

### Long-Term Fix:
- The solution can be extended to support additional features (e.g., obstacles, weighted distances, or diagonal movements) by modifying the BFS accordingly.
'''

from collections import deque

def compute_distance_to_lockers(city, lockers):
    """
    Computes the Manhattan distance from each cell in the city grid to the nearest locker.
    
    Parameters:
    - city: A 2D list (m x n matrix) representing the city blocks.
            (The values inside the matrix are not used, as the grid is defined by its dimensions.)
    - lockers: A list of tuples (x, y) indicating the positions of the lockers.
    
    Returns:
    - A 2D list of the same dimensions where each cell contains the Manhattan distance to the nearest locker.
    
    Assumptions:
    - The grid is 0-indexed.
    - Movement is allowed only in four directions: up, down, left, right.
    - Every cell is reachable and there are no obstacles.
    """
    if not city or not city[0]:
        return []

    m, n = len(city), len(city[0])
    # Initialize all distances to -1 (indicating not yet computed)
    distances = [[-1 for _ in range(n)] for _ in range(m)]
    queue = deque()

    # Step 1 (Clarification): We assume the lockers list contains valid positions within the grid.
    # Step 2 (Assumptions): For each locker position, set the distance to 0.
    for x, y in lockers:
        if 0 <= x < m and 0 <= y < n:
            distances[x][y] = 0
            queue.append((x, y))
    
    # Define movements: up, down, left, right
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    # Step 3 (Short-term fix): Multi-source BFS to fill in distances.
    while queue:
        x, y = queue.popleft()
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < m and 0 <= ny < n and distances[nx][ny] == -1:
                distances[nx][ny] = distances[x][y] + 1
                queue.append((nx, ny))
    
    # Step 4 (Long-term fix): The system now provides a base that can be extended (e.g., handling obstacles).
    return distances

# Example usage:
if __name__ == "__main__":
    # Define a sample city grid (for demonstration purposes, only the dimensions matter).
    m, n = 5, 5  # City grid of 5 rows and 5 columns.
    city = [[0] * n for _ in range(m)]
    
    # Given locker locations (example assumptions):
    # Assumption: Locker exists at top-left, center, and bottom-right.
    lockers = [(0, 0), (2, 2), (4, 4)]
    
    # Compute the distance from each block to the nearest locker.
    distances = compute_distance_to_lockers(city, lockers)
    
    # Print the resulting distance matrix.
    print("Distance matrix (Manhattan distance to nearest locker):")
    for row in distances:
        print(row)
