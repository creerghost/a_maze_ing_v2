from enum import Enum
from typing import List, Tuple
from dataclasses import dataclass


class MazeConstants(Enum):
    N: int = 1
    S: int = 2
    E: int = 4
    W: int = 8

    P_42: List[List[int]] = [
        [1, 0, 0, 0, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 0, 1, 1, 1],
        [0, 0, 1, 0, 1, 0, 0],
        [0, 0, 1, 0, 1, 1, 1],
    ]


class MazeSymbols(Enum):
    WALL: str = "██"
    PATH: str = "  "
    ENTRY: str = "●→"
    EXIT: str = "←●"
    SOLVED_PATH: str = "░░"


class Directions(Enum):
    N: Tuple[int, int] = (0, -1)
    S: Tuple[int, int] = (0, 1)
    E: Tuple[int, int] = (1, 0)
    W: Tuple[int, int] = (-1, 0)


@dataclass
class Theme:
    name: str
    wall_color: str
    path_color: str


class Themes(Enum):
    CLASSIC: Theme = Theme("classic", "\033[97m", "\033[91m")
    NEON: Theme = Theme("neon", "\033[95m", "\033[92m")
    LIGHT: Theme = Theme("light", "\033[90m", "\033[93m")
