from enum import Enum
from dataclasses import dataclass


class MazeConstants(Enum):
    N = 1
    S = 2
    E = 4
    W = 8

    P_42 = [
        [1, 0, 0, 0, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 0, 1, 1, 1],
        [0, 0, 1, 0, 1, 0, 0],
        [0, 0, 1, 0, 1, 1, 1],
    ]


class MazeSymbols(Enum):
    WALL = "██"
    PATH = "  "
    ENTRY = "●→"
    EXIT = "←●"
    SOLVED_PATH = "░░"


class Directions(Enum):
    N = (0, -1)
    S = (0, 1)
    E = (1, 0)
    W = (-1, 0)


@dataclass
class Theme:
    name: str
    wall_color: str
    path_color: str


class Themes(Enum):
    CLASSIC = Theme("classic", "\033[97m", "\033[91m")
    NEON = Theme("neon", "\033[95m", "\033[92m")
    LIGHT = Theme("light", "\033[90m", "\033[93m")
