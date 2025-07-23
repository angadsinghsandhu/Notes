"""
File: matrix_matching.py

Images are stored in the form of a grid. Image recognition is possible by comparing grids of two images and checking if they have any *matching regions*.

There are two grids where each cell of the grids contains either *0* or *1*. If two cells share a side, then they are adjacent. Cells that contain *1* form a *connected region* if any cell of that region can be reached by moving by row or column through the adjacent cells that contain *1*. Overlay the first grid onto the second and if a region of the first grid completely matches a region of the second grid, the regions are matched. Count the total number of such matched regions in the second grid.

Example:
Given two 3x3 grids grid1 and grid2:

grid1 = ['111', '100', '100']
grid2 = ['111', '100', '101']

Regions in Grid 1 and 2:
- Matching Regions: (shown as green in the image)
- Non-Matching Regions: (shown as red in the image)

There are 2 regions in the second grid: [(0,0), (0,1), (0,2), (1,0), (2,0)] and [(2,2)].
Regions in grid1 cover the first region of grid2, but not the second region. There is 1 matching region.

Function Description:
Complete the function countMatches below.

countMatches has the following parameter(s):
- string grid1[n]: an array of bit strings representing the rows of image 1
- string grid2[n]: an array of bit strings representing the rows of image 2

Returns:
- int: number of matching regions.

Constraints:
- 1 ≤ n ≤ 100
- n is the size of both grid1[] and grid2[]
- Grid cells contain only '0' or '1'

Sample Input 0:
3
001
011
100

3
001
011
101

Sample Output 0:
1

Explanation:
The first grid forms 2 regions: [(0,2), (1,1), (1,2)] and [(2,0)]
The second grid forms 2 regions: [(0,2), (1,1), (1,2)] and [(2,2)]
So, only one region matches.

Sample Input 1:
4
0100
1001
0011
0011

4
0100
1001
0011
0011

Sample Output 1:
2

Sample Input 2:
4
0010
0111
0100
1111

4
0010
0111
0110
1111

Sample Output 2:
0
"""

class Solution:
    """
    The Solution class contains methods to compare two grids and count the number of matching regions.
    The general approach is to identify all regions in the second grid and, for each region, verify if the
    corresponding cells in the first grid form a region that matches exactly in shape and connectivity.
    This involves performing depth-first searches to explore connected regions and ensure they match perfectly.
    """

    def countMatches(self, grid1, grid2):
        """
        Counts the number of regions in grid2 that completely match corresponding regions in grid1.

        Args:
            grid1 (List[str]): An array of bit strings representing the rows of image 1.
            grid2 (List[str]): An array of bit strings representing the rows of image 2.

        Returns:
            int: The number of matching regions.
        
        Time Complexity: O(n^2), where n is the size of the grid.
        Space Complexity: O(n^2), due to the space used for visited matrices and recursion stack.
        """
        n = len(grid1)
        m = len(grid1[0]) if n > 0 else 0

        grid1 = [list(row) for row in grid1]
        grid2 = [list(row) for row in grid2]

        visited2 = [[False]*m for _ in range(n)]
        visited1 = [[False]*m for _ in range(n)]
        matching_regions = 0

        def dfs2(x, y, region_positions):
            if x < 0 or x >= n or y < 0 or y >= m:
                return
            if visited2[x][y] or grid2[x][y] != '1':
                return
            visited2[x][y] = True
            region_positions.add((x, y))
            dfs2(x+1, y, region_positions)
            dfs2(x-1, y, region_positions)
            dfs2(x, y+1, region_positions)
            dfs2(x, y-1, region_positions)

        def dfs1(x, y, region_positions, visited_positions):
            if x < 0 or x >= n or y < 0 or y >= m:
                return True  # Reached boundary without issues
            if (x, y) in visited_positions:
                return True  # Already visited
            if grid1[x][y] != '1':
                return True  # Not a '1' in grid1, no extra region
            if (x, y) not in region_positions:
                return False  # Found an extra '1' outside the expected region
            visited_positions.add((x, y))
            up = dfs1(x+1, y, region_positions, visited_positions)
            down = dfs1(x-1, y, region_positions, visited_positions)
            right = dfs1(x, y+1, region_positions, visited_positions)
            left = dfs1(x, y-1, region_positions, visited_positions)
            return up and down and right and left

        for i in range(n):
            for j in range(m):
                if not visited2[i][j] and grid2[i][j] == '1':
                    region_positions = set()
                    dfs2(i, j, region_positions)
                    # Check if all positions are '1' in grid1
                    all_ones = all(grid1[x][y] == '1' for x, y in region_positions)
                    if not all_ones:
                        continue  # Region does not match
                    # Check connectivity and absence of extra '1's in grid1
                    visited_positions = set()
                    match = dfs1(i, j, region_positions, visited_positions)
                    if match and visited_positions == region_positions:
                        matching_regions += 1

        return matching_regions

# Sample usage
solution = Solution()

grid1_sample = [
    "001",
    "011",
    "100"
]
grid2_sample = [
    "001",
    "011",
    "101"
]

result = solution.countMatches(grid1_sample, grid2_sample)
print(f"Number of matching regions: {result}")
