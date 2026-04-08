from enum import Enum, StrEnum
from dataclasses import dataclass


class Algorithms(StrEnum):
    DFS = "dfs"
    KRUSKAL = "kruskal"


@dataclass
class Theme:
    name: str
    wall_color: str
    path_color: str
    pattern_color: str


class Themes(Enum):
    CLASSIC = Theme("classic", "\033[97m", "\033[91m", "\033[90m")

    BIOHAZARD = Theme("biohazard", "\033[38;5;203m", "\033[38;5;39m",
                      "\033[38;5;88m")
    QUARANTINE = Theme("quarantine", "\033[38;5;159m", "\033[38;5;197m",
                       "\033[38;5;60m")
    VIRUS = Theme("virus", "\033[38;5;177m", "\033[38;5;51m",
                  "\033[38;5;90m")


class MazeSymbols(StrEnum):
    WALL = "██"
    PATH = "  "
    ENTRY = "●→"
    EXIT = "←●"
    SOLVED_PATH = "▒▒"


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


class Directions(Enum):
    N = (0, -1)
    S = (0, 1)
    E = (1, 0)
    W = (-1, 0)
