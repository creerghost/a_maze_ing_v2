"""
Solver array module computing optimal pathways recursively locally.
"""
from collections import deque
from typing import List, Tuple, Optional

from MazeGenerator.constants import MazeConstants


class MazeSolver:
    """
    Computes shortest path resolution arrays internally traversing grid spaces.
    """
    def __init__(self, maze: List[List[int]], entry: Tuple[int, int],
                 maze_exit: Tuple[int, int]) -> None:
        """Initialize solving algorithms securely onto target coordinates."""
        self.maze = maze
        self.entry = entry
        self.maze_exit = maze_exit

    def solve(self) -> Optional[List[Tuple[int, int]]]:
        """Execute pathfinding logic connecting mapped constraints securely."""
        height = len(self.maze)
        width = len(self.maze[0]) if self.maze else 0

        queue = deque([self.entry])
        visited = {self.entry}
        parent: dict[Tuple[int, int], Tuple[int, int]] = {}

        while queue:
            current = queue.popleft()

            if current == self.maze_exit:
                break

            x, y = current
            cell = self.maze[y][x]

            # north
            if y > 0 and not (cell & MazeConstants.N.value):
                nx, ny = x, y - 1
                if self.maze[ny][nx] != 15 and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    parent[(nx, ny)] = (x, y)
                    queue.append((nx, ny))

            # south
            if y < height - 1 and not (cell & MazeConstants.S.value):
                nx, ny = x, y + 1
                if self.maze[ny][nx] != 15 and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    parent[(nx, ny)] = (x, y)
                    queue.append((nx, ny))

            # east
            if x < width - 1 and not (cell & MazeConstants.E.value):
                nx, ny = x + 1, y
                if self.maze[ny][nx] != 15 and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    parent[(nx, ny)] = (x, y)
                    queue.append((nx, ny))

            # west
            if x > 0 and not (cell & MazeConstants.W.value):
                nx, ny = x - 1, y
                if self.maze[ny][nx] != 15 and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    parent[(nx, ny)] = (x, y)
                    queue.append((nx, ny))

        if self.maze_exit not in visited:
            return None

        path: List[Tuple[int, int]] = [self.maze_exit]
        current = self.maze_exit
        while current != self.entry:
            current = parent[current]
            path.append(current)

        path.reverse()
        return path
