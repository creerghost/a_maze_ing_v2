*This project has been created as part of the 42 curriculum by vlnikola, ngvo.*

# A-Maze-Ing 

## Description

This project is an advanced, terminal-based procedural Maze Generator developed in Python. It is designed to logically generate and visually render complex grid layouts in real-time. The engine is capable of producing both "perfect" mazes—where a single unique path connects any two points with no isolated areas or loops—and non-perfect mazes containing alternative pathways and loops.

The system utilizes an external configuration file for initialization, features a modular algorithmic Strategy Pattern that seamlessly supports multiple generation techniques, and provides an interactive UI for live visualization. Once generated, the maze architectures are serialized into a dense hexadecimal bitmask text format for standardized export and storage.

---

## Configuration File Structure

The generator is driven by a `.txt` configuration file utilizing a clear `KEY=VALUE` dictionary structure.

### Example Configuration:
```env
WIDTH=40
HEIGHT=20
ENTRY=0,0
EXIT=39,19
OUTPUT_FILE=maze.txt
PERFECT=True
ALGO=dfs
SEED=48956984659734
RENDER_DELAY=0.01
```

### Parameters
| Parameter | Description |
|-----------|-------------|
| `WIDTH` | Width of the maze grid (number of columns). |
| `HEIGHT` | Height of the maze grid (number of rows). |
| `ENTRY` | Coordinates of the maze entrance (`x,y` format, zero-indexed). |
| `EXIT` | Coordinates of the maze exit (`x,y` format, zero-indexed). |
| `OUTPUT_FILE` | Target file where the resulting hex layout will be saved. |
| `PERFECT` | Enforces mathematical perfection (no loops, one path) if set to `True`. |
| `ALGO` | (Optional) Bound generator logic to instantiate initially (`dfs` or `kruskal`). |
| `SEED` | (Optional) Random seed mapping for deterministic recreation of mazes. |
| `RENDER_DELAY`| (Optional) Animation frame latency applied per cell during live visualization. |

---

## Framework & Structural Design

To ensure optimal decoupling and modularity, the core generation logic heavily leverages a **Strategy Architecture** combined with a dynamic **Python Decorator injection system** (`@register_algorithm`).

All generation mechanics extend from the `MazeAlgorithm` abstract base class, which standardizes:
- Generator iterating (`generate()`) to bridge logic frames directly to the visual engine.
- Shared modular methods for directional bitmask manipulation.
- Native injection of fixed obstacles (`apply_42_pattern()`).
- Non-perfect layout loop carving natively applied as algorithmic post-processing.

### Direction Encoding
Cell connections are managed in memory dynamically via binary bitmasking. A fully walled cell starts with the value `15` (`1111` in binary).

| Direction | Value |
|-----------|------|
| North | 1 |
| East | 2 |
| South | 4 |
| West | 8 |

Engine loops merely execute iterative bitwise inversions (`& ~wall`) to carve passages openly and efficiently.

---

## Maze Generation Algorithms & Implementation Choices

We opted to deploy two vastly dissimilar graph-traversal algorithms. This structural variety provides drastically different maze topologies on demand.

### 1. Depth-First Search (Recursive Backtracker)
DFS tunnels consistently into the grid matrix until encountering a structural dead-end, arbitrarily choosing unexplored adjacent squares, and mathematically backtracking to construct subsequent branching paths.

**Why we chose it**: 
Recursive backtracking exhibits an overwhelming bias toward generating highly extended, singular "river-like" corridors and far fewer branching pathways. This is statistically highly optimal for building classic, frustrating labyrinths that challenge sequential human navigation.

### 2. Kruskal's Algorithm (Randomized)
A robust modernized minimum-spanning-tree builder that leverages a rapid Disjoint-Set (`Union-Find`) grouping structure utilizing rank-merging and path compressions.

**Why we chose it**: 
Treating the environment mathematically, it pseudo-randomly processes a universally shuffled grid list of orthogonal connections. Crucially, it exclusively merges disconnected node groups and rejects cyclical links. This creates a highly jagged map, clustered entirely out of countless minuscule dead-ends, structurally contrasting the long, winding rivers produced by DFS.

---

## Environmental Constraints & Map Generation Rules

### 42 Pattern Static Overlays
Before algorithmic carving actively instantiates, the system strictly calculates boundaries mapping to a solid `42` structural binary pattern. Placed safely inside the map center, these designated areas are forcefully avoided by both generic algorithms during dynamic execution, rendering static maze environments organically enclosing logical obstacles.

### Imperfect Loop Injection (Cycles)
When configuration parameters flag `PERFECT=False`, the application initiates an isolated loop injection pattern entirely separate from the active tree pathing. 
After primary execution logic resolves, it pools all unused protected walls. Relying on an explicit target density fraction calculation, walls linking adjacent structural paths are forcefully severed. 
This process seamlessly embeds:
- Redundant bypass trails.
- Complicated circular architecture loops.
- Dense path-finding options more reflective of natural geographic layouts.

---

## Interactive Live Visualization 

Differing functionally from static generator scripts, our architecture organically binds iterative algorithmic computation directly to an active console rendering window. Generators periodically yield layout updates natively back to `MazeEngine.py`, refreshing visuals incrementally to show users paths being carved directly within the console window.

During idle loops or active generation, users manipulate the environment logically using keyboard interactions:
- `a`: Dynamically switches the active underlying generation algorithm.
- `g`: Force-starts an entirely new randomized layout sequence.
- `s`: Toggles rendering of the underlying mathematical exit solution.
- `t`: Iterates logical environment rendering themes (`Classic`, `Biohazard`, `Virus`).
- `q`: Gracefully aborts rendering, finalizing active states to serialize the layout text mapping.

---

## Instructions

We've automated the orchestration wrapper securely into a `Make` structure to ease virtual environment mapping and package requirements dynamically.

### System Requirements
- Python 3.10+
- `make` pipeline

### Installation & Setup

Set up the project container and required local repository configurations natively:
```bash
make install
```

### Execution

Execute the fully built environment natively invoking the config parameters:
```bash
make run
```
Which explicitly wraps:
```bash
python3 a_maze_ing.py config.txt
```

---

## Project Management & Roles

This architecture was developed collaboratively within the scope of the 42 curriculum.

| Contributor | Roles & Responsibilities |
|-----|------|
| **vlnikola** | Engineered core generator architecture and dynamic decorators (`@register_algorithm`), built config parsing and ingestion routines (`Parser`), implemented the `DFS` algorithm and the structural 42-Pattern overlay logic, handled hex bitmask grid output formatting, and constructed execution binaries alongside automation in the `Makefile`. |
| **ngvo** | Designed the `MazeEngine` and asynchronous terminal event listeners, managed robust terminal UI updates alongside iterative dynamic mathematical rendering, built thematic array layouts, developed the algorithmic `Kruskal's` union-find sequence, and deployed recursive loop solving pathfinders. |

### Development Retrospective
Starting initially as a static, continuous-loop Python rendering script with hardcoded logic, execution shifted massively to decouple visual rendering logic natively from math processing functions entirely. Wrapping generation arrays in native asynchronous Python iterators (`yield`) allowed simple frame-by-frame UI hooks over previously inaccessible matrix functions.
In the future, migrating heavy generic iterative Python list nesting onto strict static array mapping (`NumPy` integration) could scale up live map calculations from basic grids up to `10,000`x`10,000` cells instantly without frame lag.

---

## Resources 

- **Language Features**: [Python 3.10 Official Documentation](https://docs.python.org/3/) & the `abc` standard module logic mapping for abstract structural layouts. 
- **Underlying Logic Structure**: Researched standard Kruskal's Min Spanning Trees methodology and optimal Disjoint-Set / Union-Find optimizations (`Union By Rank`, `Path Compression`). 
- **AI Support Guidelines**: Agentic Code-Assistant tools (e.g. ChatGPT) were incorporated selectively strictly as rapid structural refactorization consultants. AI tools explicitly helped us restructure monolithic ingestion code natively into single-responsibility standards, resolved rigid `mypy` static typing edge-case flags during decorator integrations, and assisted in tracking structural collision errors inside early Bitmask mapping serialization. All logic flow architecture, implementation concepts, and system states were designed intrinsically by humans.