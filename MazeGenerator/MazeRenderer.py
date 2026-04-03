from typing import List, Tuple, Optional
from MazeGenerator.constants import Themes, MazeConstants, MazeSymbols


class MazeRenderer:
    """
    Renders bitmasked maze logically using ASCII graphics over a 2x canvas.
    """
    def __init__(self, maze: List[List[int]], theme: Themes,
                 entry: Optional[Tuple[int, int]] = None,
                 maze_exit: Optional[Tuple[int, int]] = None,
                 solution_path: Optional[List[Tuple[int, int]]] = None):
        self.maze = maze
        self.theme = theme
        self.entry = entry
        self.maze_exit = maze_exit
        self.solution_path = solution_path

    def render(self) -> List[List[str]]:
        """
        Translates maze array into a 2D string matrix array for console print.

        Returns:
            List[List[str]]: Grid string map containing walls, pattern blocks.
        """
        if not self.maze or not self.maze[0]:
            return []

        height: int = len(self.maze)
        width: int = len(self.maze[0])
        grid_h: int = height * 2 + 1
        grid_w: int = width * 2 + 1

        wall_c: str = self.theme.value.wall_color
        path_c: str = self.theme.value.path_color
        reset_c: str = "\033[0m"

        wall_char: str = f"{wall_c}{MazeSymbols.WALL.value}{reset_c}"
        path_char: str = f"{path_c}{MazeSymbols.PATH.value}{reset_c}"
        pattern_color: str = "\033[90m"
        fill_char: str = f"{pattern_color}{MazeSymbols.WALL.value}{reset_c}"

        output: List[List[str]] = [[wall_char for _ in range(grid_w)]
                                   for _ in range(grid_h)]

        for y in range(height):
            for x in range(width):
                cell: int = self.maze[y][x]
                cy: int = y * 2 + 1
                cx: int = x * 2 + 1
                if cell == 15:
                    output[cy][cx] = fill_char
                    if y > 0 and self.maze[y-1][x] == 15:
                        output[cy-1][cx] = fill_char
                    if x > 0 and self.maze[y][x-1] == 15:
                        output[cy][cx-1] = fill_char
                    if (y > 0 and x > 0 and self.maze[y-1][x-1] == 15
                            and self.maze[y-1][x] == 15
                            and self.maze[y][x-1] == 15):
                        output[cy-1][cx-1] = fill_char
                else:
                    output[cy][cx] = path_char

                    if not (cell & MazeConstants.N.value):
                        output[cy - 1][cx] = path_char
                    if not (cell & MazeConstants.S.value):
                        output[cy + 1][cx] = path_char
                    if not (cell & MazeConstants.E.value):
                        output[cy][cx + 1] = path_char
                    if not (cell & MazeConstants.W.value):
                        output[cy][cx - 1] = path_char

        if self.solution_path:
            solved_char: str = (
                f"\033[96m{MazeSymbols.SOLVED_PATH.value}{reset_c}"
            )
            for sx, sy in self.solution_path:
                if 0 <= sy < height and 0 <= sx < width:
                    output[sy * 2 + 1][sx * 2 + 1] = solved_char

        if self.entry:
            ex, ey = self.entry
            if 0 <= ey < height and 0 <= ex < width:
                output[ey * 2 + 1][ex * 2 + 1] = (f"\033[95m"
                                                  f"{MazeSymbols.ENTRY.value}"
                                                  f"{reset_c}")

        if self.maze_exit:
            ex, ey = self.maze_exit
            if 0 <= ey < height and 0 <= ex < width:
                output[ey * 2 + 1][ex * 2 + 1] = (f"\033[91m"
                                                  f"{MazeSymbols.EXIT.value}"
                                                  f"{reset_c}")

        return output
