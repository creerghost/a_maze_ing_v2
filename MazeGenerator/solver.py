from collections import deque
from typing import List, Tuple, Optional

from MazeGenerator.constants import MazeConstants


def solve_maze(
    maze: List[List[int]],
    entry: Tuple[int, int],
    exit: Tuple[int, int],
) -> Optional[List[Tuple[int, int]]]:
    height = len(maze)
    width = len(maze[0]) if maze else 0

    queue = deque([entry])
    visited = {entry}
    parent: dict[Tuple[int, int], Tuple[int, int]] = {}

    while queue:
        current = queue.popleft()

        if current == exit:
            break

        x, y = current
        cell = maze[y][x]

        # north
        if y > 0 and not (cell & MazeConstants.N.value):
            nx, ny = x, y - 1
            if maze[ny][nx] != 15 and (nx, ny) not in visited:
                visited.add((nx, ny))
                parent[(nx, ny)] = (x, y)
                queue.append((nx, ny))

        # south
        if y < height - 1 and not (cell & MazeConstants.S.value):
            nx, ny = x, y + 1
            if maze[ny][nx] != 15 and (nx, ny) not in visited:
                visited.add((nx, ny))
                parent[(nx, ny)] = (x, y)
                queue.append((nx, ny))

        # east
        if x < width - 1 and not (cell & MazeConstants.E.value):
            nx, ny = x + 1, y
            if maze[ny][nx] != 15 and (nx, ny) not in visited:
                visited.add((nx, ny))
                parent[(nx, ny)] = (x, y)
                queue.append((nx, ny))

        # west
        if x > 0 and not (cell & MazeConstants.W.value):
            nx, ny = x - 1, y
            if maze[ny][nx] != 15 and (nx, ny) not in visited:
                visited.add((nx, ny))
                parent[(nx, ny)] = (x, y)
                queue.append((nx, ny))

    if exit not in visited:
        return None

    path: List[Tuple[int, int]] = [exit]
    current = exit
    while current != entry:
        current = parent[current]
        path.append(current)

    path.reverse()
    return path
