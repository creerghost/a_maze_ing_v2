import os
import time
from typing import Callable, List, Optional, Tuple
from MazeGenerator.constants import Themes
from MazeGenerator.algorithms import MazeAlgorithm
from MazeGenerator.algorithms import DFSAlgorithm
from MazeGenerator.MazeRenderer import MazeRenderer
from MazeGenerator.solver import solve_maze


class MazeEngine:
    def __init__(self,
                 width: int,
                 height: int,
                 entry: Tuple[int, int],
                 maze_exit: Tuple[int, int]
                 ) -> None:
        self.width = width
        self.height = height
        self.entry = entry
        self.maze_exit = maze_exit

        self.algorithm_name: str = "dfs"
        self.theme_options: List[Themes] = list(Themes)
        self.theme_index: int = 0
        self.show_solution: bool = False
        self.solution_path: Optional[List[Tuple[int, int]]] = None
        self.current_maze: Optional[List[List[int]]] = None

    @property
    def theme(self) -> Themes:
        return self.theme_options[self.theme_index]

    def cycle_theme(self) -> None:
        self.theme_index = (self.theme_index + 1) % len(self.theme_options)

    def toggle_algorithm(self) -> None:
        self.algorithm_name = (
            "kruskal" if self.algorithm_name == "dfs" else "dfs"
        )

    def toggle_solution_visibility(self) -> None:
        self.show_solution = not self.show_solution

    def _build_algorithm(self) -> MazeAlgorithm:
        """Returns the selected algorithm instance."""
        if self.algorithm_name == "dfs":
            return DFSAlgorithm(self.width, self.height)
        else:
            raise NotImplementedError("Kruskal not ready yet")

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
        output = renderer.render()  # Returns a 2D list of strings
        for row in output:
            print("".join(row))

    def generate_new_maze(self, animate: bool = True) -> None:
        """Generates a new maze and stores in self.current_maze."""
        algorithm = self._build_algorithm()

        # Loop through each intermediate maze state
        for maze_state in algorithm.generate():
            # Store the current state (make a copy so we don't lose it)
            self.current_maze = [row[:] for row in maze_state]
            if animate:
                self._render_frame(self.current_maze)
                time.sleep(0.01)

        if self.current_maze is not None:
            self.solution_path = solve_maze(
                self.current_maze,
                self.entry,
                self.maze_exit,
            )
            self._render_frame(self.current_maze)

    def run(self, print_menu: Callable[[], None]) -> None:
        """Main interactive loop that handles user commands."""
        self.generate_new_maze(animate=True)

        # Interactive command loop
        while True:
            if self.current_maze is not None:
                self._render_frame(self.current_maze)
            print_menu()
            command = input("Select an option: ").strip().lower()

            if command == "q":
                break
            elif command == "a":
                self.toggle_algorithm()
                if self.show_solution is True:
                    self.toggle_solution_visibility()
                self.generate_new_maze(animate=True)
            elif command == "g":
                if self.show_solution is True:
                    self.toggle_solution_visibility()
                self.generate_new_maze(animate=True)
            elif command == "s":
                self.toggle_solution_visibility()
            elif command == "t":
                self.cycle_theme()
            else:
                print("Unknown command. Try again.")
