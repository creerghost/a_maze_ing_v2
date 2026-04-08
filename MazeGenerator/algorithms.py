from abc import ABC, abstractmethod
from typing import Callable, Dict, Generator, List, Tuple, Deque, Type
from MazeGenerator.constants import MazeConstants, Directions, Algorithms
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
                    self.maze[my][mx] = 15
        return cells


ALGORITHMS_REGISTRY: Dict[str, Type['MazeAlgorithm']] = {}

def register_algorithm(algo_name: str) -> Callable[[Type['MazeAlgorithm']], Type['MazeAlgorithm']]:
    def decorator(cls: Type['MazeAlgorithm']) -> Type['MazeAlgorithm']:
        ALGORITHMS_REGISTRY[algo_name] = cls
        return cls
    return decorator


@register_algorithm(Algorithms.DFS)
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

            start_x = random.randint(0, self.width - 1)
            start_y = random.randint(0, self.height - 1)
            while visited[start_y][start_x]:
                start_x = random.randint(0, self.width - 1)
                start_y = random.randint(0, self.height - 1)

            stack.append((start_x, start_y))
            visited[start_y][start_x] = True
        else:
            start_x = random.randint(0, self.width - 1)
            start_y = random.randint(0, self.height - 1)
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


class _UnionFind:
    """
    Groups cells together so Kruskal can avoid loops.

    Kruskal Algo builds a tree:
    Union-Find instantly checks if two cells are connected.
    Union-by-rank + path compression together keep trees shallow.
    """
    def __init__(self, nodes: List[Tuple[int, int]]) -> None:
        self.parent: Dict[Tuple[int, int], Tuple[int, int]] = {
            node: node for node in nodes
        }
        # rank = height estimate (used for union-by-rank)
        # not exact node-to-root distance
        self.rank: Dict[Tuple[int, int], int] = {node: 0 for node in nodes}

    def find(self, node: Tuple[int, int]) -> Tuple[int, int]:
        """
        Finds the group leader (root) for a cell.
        Also compresses the path to optimize speed.
        """
        root = node
        while self.parent[root] != root:
            root = self.parent[root]

        # Path compression: point every node on this find path directly to root
        while node != root:
            parent = self.parent[node]
            self.parent[node] = root
            node = parent

        return root

    def union(self, a: Tuple[int, int], b: Tuple[int, int]) -> bool:
        """Joins two groups"""
        root_a = self.find(a)
        root_b = self.find(b)

        if root_a == root_b:  # Already in the same set; no merge needed
            return False

        # Merge by rank; caller can use True to carve passage
        rank_a = self.rank[root_a]
        rank_b = self.rank[root_b]

        if rank_a < rank_b:
            self.parent[root_a] = root_b
        elif rank_a > rank_b:
            self.parent[root_b] = root_a
        else:
            self.parent[root_b] = root_a
            self.rank[root_a] += 1

        return True


@register_algorithm(Algorithms.KRUSKAL)
class KruskalAlgorithm(MazeAlgorithm):
    """
    Randomized Kruskal-based structural generator using Union-Find.

    It shuffles possible links between neighbor cells and opens a wall only
    when the two cells are in different groups.
    """
    def __init__(self, width: int, height: int) -> None:
        super().__init__(width, height)

    def generate(self) -> Generator[List[List[int]], None, None]:
        for y in range(self.height):
            for x in range(self.width):
                self.maze[y][x] = 15

        blocked = set(self.apply_42_pattern())

        nodes: List[Tuple[int, int]] = []
        for y in range(self.height):
            for x in range(self.width):
                if (x, y) not in blocked:
                    nodes.append((x, y))

        if not nodes:
            yield self.maze
            return

        uf = _UnionFind(nodes)
        edges: List[Tuple[Tuple[int, int], Tuple[int, int], int, int]] = []

        # Find candidate walls to carve a path
        for y in range(self.height):
            for x in range(self.width):
                if (x, y) in blocked:
                    continue

                if x + 1 < self.width and (x + 1, y) not in blocked:
                    edges.append(
                                ((x, y), (x + 1, y),
                                    MazeConstants.E.value,
                                    MazeConstants.W.value)
                            )

                if y + 1 < self.height and (x, y + 1) not in blocked:
                    edges.append(
                        ((x, y), (x, y + 1),
                            MazeConstants.S.value, MazeConstants.N.value)
                    )

        random.shuffle(edges)

        carved = False
        for (ax, ay), (bx, by), wall_a, wall_b in edges:
            # Carve only if cells are in different groups
            if uf.union((ax, ay), (bx, by)):
                self.maze[ay][ax] &= ~wall_a
                self.maze[by][bx] &= ~wall_b
                carved = True
                yield self.maze

        if not carved:
            # Engine still receives final state for tiny mazes
            yield self.maze
