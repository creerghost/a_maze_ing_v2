import os
import time
import random
from typing import List, Optional, Tuple
from MazeGenerator.constants import Themes
from MazeGenerator.algorithms import MazeAlgorithm, ALGORITHMS_REGISTRY
from MazeGenerator.MazeRenderer import MazeRenderer
from MazeGenerator.MazeSolver import MazeSolver


class MazeEngine:
    ALL_THEMES: List[Themes] = list(Themes)

    def __init__(self,
                 width: int,
                 height: int,
                 entry: Tuple[int, int],
                 maze_exit: Tuple[int, int],
                 output_file: str,
                 algorithm_name: str,
                 render_delay: float = 0.01,
                 seed: Optional[int] = None
                 ) -> None:
        self.width = width
        self.height = height
        self.entry = entry
        self.maze_exit = maze_exit
        self.output_file = output_file
        self.render_delay = render_delay

        self.algorithm_name: str = algorithm_name.lower()
        self.theme_index: int = 0
        self.show_solution: bool = False
        self.solution_path: Optional[List[Tuple[int, int]]] = None
        self.current_maze: Optional[List[List[int]]] = None
        self.initial_seed = seed
        self.current_seed: Optional[int] = None

    @property
    def theme(self) -> Themes:
        return self.ALL_THEMES[self.theme_index]

    def cycle_theme(self) -> None:
        self.theme_index = (self.theme_index + 1) % len(self.ALL_THEMES)

    def toggle_algorithm(self) -> None:
        algos = list(ALGORITHMS_REGISTRY.keys())
        current_idx = algos.index(self.algorithm_name)
        self.algorithm_name = algos[(current_idx + 1) % len(algos)]

    def toggle_solution_visibility(self) -> None:
        self.show_solution = not self.show_solution

    def _build_algorithm(self) -> MazeAlgorithm:
        """Returns the selected algorithm instance."""
        algo_class = ALGORITHMS_REGISTRY.get(self.algorithm_name,
                                             ALGORITHMS_REGISTRY["dfs"])
        return algo_class(self.width, self.height)

    def _render_frame(self, maze_state: List[List[int]]) -> None:
        """Clears screen and renders one maze state using current theme."""
        os.system("clear")
        renderer = MazeRenderer(
            maze_state,
            self.theme,
            self.entry,
            self.maze_exit,
            self.solution_path if self.show_solution else None,
        )
        output = renderer.render()
        for row in output:
            print("".join(row))
        print(
            f"\nAlgorithm: {self.algorithm_name.upper()} | "
            f"Grid: {self.width}x{self.height} | "
            f"Theme: {self.theme.value.name} | "
            f"Solution: {'ON' if self.show_solution else 'OFF'} | "
            f"Seed: {self.current_seed}"
        )

    def generate_new_maze(self, animate: bool = True) -> None:
        """Generates a new maze and stores in self.current_maze."""
        if self.current_seed is None and self.initial_seed is not None:
            self.current_seed = self.initial_seed
        else:
            self.current_seed = random.randint(0, 999999999)

        random.seed(self.current_seed)

        algorithm = self._build_algorithm()
        previous_solution_state = self.show_solution

        # Keep the user's toggle choice, but hide the overlay while carving.
        if animate:
            self.show_solution = False

        # Loop through each intermediate maze state
        for maze_state in algorithm.generate():
            # Store the current state (make a copy so we don't lose it)
            self.current_maze = [row[:] for row in maze_state]
            if animate:
                self._render_frame(self.current_maze)
                time.sleep(self.render_delay)

        if self.current_maze is not None:
            solver = MazeSolver(
                self.current_maze,
                self.entry,
                self.maze_exit,
            )
            self.solution_path = solver.solve()
            self.export_maze()
            self.show_solution = previous_solution_state
            self._render_frame(self.current_maze)

    def export_maze(self) -> None:
        """Exports the maze state and solution into the specified text file."""
        if not self.current_maze:
            return

        with open(self.output_file, 'w') as f:
            for row in self.current_maze:
                line = "".join(f"{cell:X}" for cell in row)
                f.write(line + "\n")

            f.write("\n")
            f.write(f"{self.entry[0]},{self.entry[1]}\n")
            f.write(f"{self.maze_exit[0]},{self.maze_exit[1]}\n")

            if self.solution_path:
                path_str = ""
                for i in range(len(self.solution_path) - 1):
                    cx, cy = self.solution_path[i]
                    nx, ny = self.solution_path[i+1]
                    if nx > cx:
                        path_str += "E"
                    elif nx < cx:
                        path_str += "W"
                    elif ny > cy:
                        path_str += "S"
                    elif ny < cy:
                        path_str += "N"
                f.write(path_str + "\n")
            else:
                f.write("\n")

    def print_menu(self) -> None:
        print("\n=== A-Maze-Ing ===")
        print("a - Change algorithm")
        print("g - Generate new maze")
        print("s - Show/Hide solution path")
        print("t - Next theme")
        print("q - Quit")
        print("====================")

    def run(self) -> None:
        """Main interactive loop that handles user commands."""
        self.generate_new_maze(animate=True)

        while True:
            if self.current_maze is not None:
                self._render_frame(self.current_maze)
            self.print_menu()
            command = input("Select an option: ").strip().lower()

            if command == "q":
                break
            elif command == "a":
                self.toggle_algorithm()
                self.generate_new_maze(animate=True)
            elif command == "g":
                self.generate_new_maze(animate=True)
            elif command == "s":
                self.toggle_solution_visibility()
            elif command == "t":
                self.cycle_theme()
            else:
                print("Unknown command. Try again.")
