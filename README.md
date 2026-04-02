# A-Maze-Ing: Maze Generator

A modular, terminal-based, object-oriented Python maze generator and solver featuring dynamic 2D visual rendering and custom structural seeding (the "42" pattern).

## Project Setup & Execution
- **Run the program:** `make run`
- **Lint the codebase:** `make lint` and `make lint-strict`
- **Clean environment:** `make clean`

---

## TODO: Remaining Tasks (For Co-worker)

The core architecture, parsing, rendering pipeline, and base DFS algorithm are fully implemented, strictly typed, and cleanly linted. 

The following modules need to be completed to finish the project specifications:

### 1. `MazeEngine.py` Complete Interactive Loop
- Implement the core runtime engine logic to replace the simple linear loop currently hardcoded in `a_maze_ing.py`.
- Connect the `print_menu()` interface.
- Add dynamic runtime hot-swapping of configuration options:
  - Toggle between different algorithms (DFS vs Kruskal).
  - Toggle between visual color themes.
  - Generate new mazes dynamically without restarting the application.
  - Toggle solver paths on and off seamlessly.

### 2. Pathfinding Solver
- Create a solver module (e.g., BFS or A* algorithm) that computes the shortest path between the `ENTRY` and `EXIT` coordinates provided by the `Parser`.
- Pass the solved path back into the engine, instructing the `MazeRenderer` to cleanly overlay the route using the `MazeSymbols.SOLVED_PATH` ANSI tokens.

### 3. Alternative Generation Algorithm
- Implement a second generation algorithm subclass strictly inheriting from `MazeAlgorithm`.
- **Recommendation:** Implement **Kruskal's Algorithm** utilizing a Disjoint-Set (Union-Find) data structure to randomize a list of edges and merge disparate cell sets iteratively.
- **Requirement:** Make sure you seed the Kruskal class with `self.apply_42_pattern()` exactly like the `DFSAlgorithm` does so it cleanly routes around the solid block pattern!
