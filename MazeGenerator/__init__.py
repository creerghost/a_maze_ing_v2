"""
Maze Generator and Solver Library (mazegen)
-------------------------------------------
This module provides a standalone, reusable procedural maze generation engine.
It leverages a Strategy Pattern to decouple logic, allowing for diverse
recursive carving rules.

Usage Example
-------------
    from MazeGenerator import MazeEngine

    # 1. Instantiate the generator and pass custom parameters
    generator = MazeEngine(
        width=20,
        height=20,
        entry=(0, 0),
        maze_exit=(19, 19),
        output_file="exported_maze.txt",
        algorithm_name="dfs",  # 'dfs' or 'kruskal'
        perfect=True,
        animate=False, # Disable terminal rendering for silent generation
        seed=12345
    )

    # 2. Generate the maze and auto-solve
    generator.generate_new_maze(animate=False)

    # 3. Access the generated grid structure
    # (Returns a List of lists representing grid bitmasks)
    maze_structure = generator.current_maze
    print(f"Top-Left Cell bitmask: {maze_structure[0][0]}")

    # 4. Access the calculated solution path (List of (x,y) tuples)
    solution = generator.solution_path
    if solution:
        print(f"Solution steps: {len(solution)}")
"""

from MazeGenerator.MazeEngine import MazeEngine
from MazeGenerator.Parser import Parser

__all__ = ['MazeEngine', 'Parser']
