# A-Maze-ing Project Implementation Plan

This document outlines the architecture, tasks, and collaboration plan for the A-Maze-ing project. The goal is to build a robust, OOP-based maze generator and visualization engine in Python 3.10+, complete with algorithms (Prim's and Kruskal's), an exhaustive configuration parser, and an interactable terminal UI/visualization.

## User Review Required

> [!IMPORTANT]
> Please review the updated plan! I have explicitly set the visualization to **Terminal ASCII only** according to your instructions, and assigned the algorithm choice feature to the **Interactive Terminal Menu** (Interface) instead of a config file flag. Let me know if you are ready to proceed with these steps.

## Proposed Architecture and Best Practices

The project will strictly follow Python best practices:
- **Virtual Environments & Package Management**: Setup using `venv` and standard python tools.
- **Code Quality**: Enforced via a `Makefile` with `lint` targets running `flake8` and `mypy` (with strict type hinting rules).
- **Documentation**: All functions/classes will include PEP-257 compliant docstrings.
- **Object-Oriented Programming**: 
  - An Abstract Base Class (ABC) `BaseMazeGenerator` to define the interface for different algorithms (Prim, Kruskal).
  - An Abstract Base Class `BaseRenderer` to define rendering interfaces (Terminal output, Hex File output).

### Directory Structure

```text
.
├── Makefile
├── README.md
├── a_maze_ing.py               # Main entry point (CLI usage)
├── config.txt                  # Default configuration file
└── mazegen/                    # The reusable module to be packed (mazegen-*)
    ├── __init__.py
    ├── config_parser.py        # Parses config files safely 
    ├── maze.py                 # Core Maze data structure
    ├── solver.py               # Pathfinding logic (BFS)
    ├── generators/
    │   ├── __init__.py
    │   ├── base.py             # Abstract BaseMazeGenerator
    │   ├── prim.py             # Prim's Algorithm implementation
    │   └── kruskal.py          # Kruskal's Algorithm implementation
    └── renderers/
        ├── __init__.py
        ├── base.py             # Abstract BaseRenderer
        ├── hex_file.py         # Output to hexadecimal file format
        └── terminal.py         # Terminal ASCII rendering & interactive menu
```

---

## Workload Distribution

The work is split to ensure that **Student A** (stronger) tackles the core architectural patterns, packaging, and the more rigorous graph logic, while **Student B** (weaker) tackles self-contained algorithmic tasks, formatting, visual rendering, and procedural scripting.

### Student A (Stronger Student)

**1. Core Architecture, Abstractions, and OOP:**
- Create the core `Maze` class for storing the grid (handling dimensions, walls, entries/exits).
- Define the Abstract Base Classes (`BaseMazeGenerator` and `BaseRenderer`) to ensure polymorphic behavior.
- Use context managers and error handling schemas throughout the core logic.

**2. Parsing and Config Engine:**
- Build `config_parser.py` to robustly read `config.txt` and map `KEY=VALUE` pairs into a typed configuration object (handling edge cases and malformed files).

**3. Kruskal's Algorithm:**
- Implement `KruskalMazeGenerator` using a Disjoint Set (Union-Find) data structure to guarantee mathematical correctness for generating a randomized perfect maze.

**4. Maze Solver Module:**
- Implement `solver.py` utilizing BFS algorithm to reliably find and format the shortest path (in `N, E, S, W` coordinates).

**5. Packaging and Build System:**
- Configure `pyproject.toml` to generate the `.whl` and `.tar.gz` package (`mazegen-*`).

---

### Student B (Weaker Student)

**1. Project Setup and Linters:**
- Draft the `Makefile` with the required commands: `install`, `run`, `debug`, `clean`, `lint`, and `lint-strict`.
- Create a `.gitignore` to keep the repository clean.

**2. Prim's Algorithm:**
- Implement `PrimMazeGenerator`. The randomized Prim's algorithm is straightforward to implement using a frontier list of cells to naturally grow the maze.

**3. "42" Generator Logic:**
- Write a procedural function that statically carves/draws a "42" shape in the interior cells of the grid when regenerating the maze.

**4. Hexadecimal File Output:**
- Implement `hex_file.py`. Write a renderer that evaluates the N(1), E(2), S(4), W(8) bits for walls, translates them to Hex string formatting, appends the path, and writes to the output file using context managers.

**5. Terminal Visualization and Interactive Menu:**
- **No Graphical Libraries**: Implement `terminal.py` as an exclusively CLI ASCII renderer to visually display the maze wall structure.
- **Interactive Menu Features**: 
  - Ask the user to select the **Algorithm** (Prim or Kruskal) when regenerating a new maze. This is done dynamically in the interactive interface.
  - Show/hide the shortest path from entrance to exit.
  - Change colors of the labyrinth lines and pattern highlighting.

---

## Verification Plan

### Automated Tests
- Running `make lint` and `make lint-strict` to ensure `flake8` and `mypy` compliance.

### Manual Verification
- Invoking `python3 a_maze_ing.py config.txt` to verify execution.
- Verifying the interactive terminal prompts directly via the CLI, testing algorithm switching between Prim and Kruskal.
