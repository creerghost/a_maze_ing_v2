import os
import time
from typing import List, Optional, Tuple
from MazeGenerator.constants import Themes
from MazeGenerator.algorithms import MazeAlgorithm, ALGORITHMS_REGISTRY
from MazeGenerator.MazeRenderer import MazeRenderer
from MazeGenerator.solver import MazeSolver


class MazeEngine:
    ALL_THEMES: List[Themes] = list(Themes)

    def __init__(self,
                 width: int,
                 height: int,
                 entry: Tuple[int, int],
                 maze_exit: Tuple[int, int],
                 algorithm_name: str = "dfs",
                 render_delay: float = 0.01
                 ) -> None:
        self.width = width
        self.height = height
        self.entry = entry
        self.maze_exit = maze_exit
        self.render_delay = render_delay

        self.algorithm_name: str = algorithm_name.lower()
        if self.algorithm_name not in ALGORITHMS_REGISTRY:
            self.algorithm_name = "dfs"
        self.theme_index: int = 0
        self.show_solution: bool = False
        self.solution_path: Optional[List[Tuple[int, int]]] = None
        self.current_maze: Optional[List[List[int]]] = None

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
            f"Solution: {'ON' if self.show_solution else 'OFF'}"
        )

    def generate_new_maze(self, animate: bool = True) -> None:
        """Generates a new maze and stores in self.current_maze."""
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
            self.show_solution = previous_solution_state
            self._render_frame(self.current_maze)

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
