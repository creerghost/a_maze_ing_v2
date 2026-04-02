from abc import ABC, abstractmethod
from typing import List, Tuple, Deque, Generator
from MazeGenerator.constants import MazeConstants, Directions
import random
from collections import deque


class MazeAlgorithm(ABC):
    """
    Abstract base defining the contract for maze generation algorithms.
    """
    def __init__(self, width: int, height: int) -> None:
        """
        Initializes the base attributes for maze generation.

        Args:
            width (int): The number of cells horizontally.
            height (int): The number of cells vertically.
        """
        self.width = width
        self.height = height
        self.maze: List[List[int]] = [[0 for _ in range(width)]
                                      for _ in range(height)]

    @abstractmethod
    def generate(self) -> Generator[List[List[int]], None, None]:
        """
        Generates the maze iteratively, yielding intermediate maze states.

        Yields:
            List[List[int]]: 2D grid array of bitmasked cells or walls.
        """
        pass

    def apply_42_pattern(self) -> List[Tuple[int, int]]:
        """
        Injects a structural '42' pattern strictly into the maze center.

        Returns:
            List[Tuple[int, int]]: Pattern cells shielded from generation.
        """
        pattern: List[List[int]] = MazeConstants.P_42.value
        p_h: int = len(pattern)
        p_w: int = len(pattern[0])
        start_y: int = (self.height - p_h) // 2
        start_x: int = (self.width - p_w) // 2
        if start_y < 0 or start_x < 0:
            return []

        cells: List[Tuple[int, int]] = []

        for py in range(p_h):
            for px in range(p_w):
                if pattern[py][px] == 1:
                    my: int = start_y + py
                    mx: int = start_x + px
                    cells.append((mx, my))
                    self.maze[my][mx] = 15  # Solid, intact wall representation
        return cells


class DFSAlgorithm(MazeAlgorithm):
    """
    Standard Depth-First Search recursive backtracker structural generator.
    """
    def __init__(self, width: int, height: int) -> None:
        super().__init__(width, height)

    def generate(self) -> Generator[List[List[int]], None, None]:
        for y in range(self.height):
            for x in range(self.width):
                self.maze[y][x] = 15

        visited: List[List[bool]] = [[False] * self.width
                                     for _ in range(self.height)]
        stack: Deque[Tuple[int, int]] = deque()
        pattern_cells: List[Tuple[int, int]] = self.apply_42_pattern()

        if pattern_cells:
            for px, py in pattern_cells:
                visited[py][px] = True

            start_x: int = random.randint(0, self.width - 1)
            start_y: int = random.randint(0, self.height - 1)
            while visited[start_y][start_x]:
                start_x = random.randint(0, self.width - 1)
                start_y = random.randint(0, self.height - 1)

            stack.append((start_x, start_y))
            visited[start_y][start_x] = True
        else:
            start_x: int = random.randint(0, self.width - 1)
            start_y: int = random.randint(0, self.height - 1)
            stack.append((start_x, start_y))
            visited[start_y][start_x] = True

        while stack:
            cx: int = stack[-1][0]  # first value is position in q (last added)
            cy: int = stack[-1][1]  # second value is x or y
            directions: List[Tuple[Tuple[int, int], int, int]] = [
                (Directions.N.value,
                 MazeConstants.N.value, MazeConstants.S.value),

                (Directions.S.value,
                 MazeConstants.S.value, MazeConstants.N.value),

                (Directions.E.value,
                 MazeConstants.E.value, MazeConstants.W.value),

                (Directions.W.value,
                 MazeConstants.W.value, MazeConstants.E.value)
            ]
            random.shuffle(directions)

            moved: bool = False
            for (dx, dy), wall, opp_wall in directions:
                nx: int = cx + dx
                ny: int = cy + dy
                if (0 <= nx < self.width and 0 <= ny < self.height and
                        not visited[ny][nx]):
                    self.maze[cy][cx] &= ~wall
                    self.maze[ny][nx] &= ~opp_wall
                    visited[ny][nx] = True
                    stack.append((nx, ny))
                    moved = True
                    break
            if not moved:
                stack.pop()
            yield self.maze
