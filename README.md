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
# config.txt
WIDTH=40
HEIGHT=20
ENTRY=0,0
EXIT=39,19
OUTPUT_FILE=maze.txt
PERFECT=True
ALGO=dfs
SEED=42
RENDER_DELAY=0.01
ANIMATE=True
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
| `ANIMATE` | (Optional) Whether to animate the maze generation process. |

---

## Framework & Structural Design

The Strategy Pattern is a design pattern that allows you to define a family of algorithms, put each of them into a separate class, and make their objects interchangeable. 

In our project, we successfully implemented this pattern primarily inside `MazeGenerator/algorithms.py` and it is managed by the `MazeEngine`. Here is exactly how and where we used it:

### 1. The Strategy Interface (`MazeAlgorithm`)
The `MazeAlgorithm` abstract base class acts as our **Strategy Interface**. It defines the blueprint that *any* generation algorithm must follow. Specifically, it dictates that every algorithm must have a `.generate()` method that `yields` updates to the visual engine, and it provides inherited utilities like `.apply_42_pattern()` or bitmask tools.

### 2. Concrete Strategies (`DFS` & `Kruskal`)
The individual algorithms we built—DFS and Kruskal's—are our **Concrete Strategies**. They inherit from `MazeAlgorithm` and implement the actual logic for path carving. Because they both use the exact same interface `(the .generate() method)`, they can be treated identically.

### 3. The Registration Subsystem (`@register_algorithm`)
We used the `@register_algorithm` python decorator to dynamically log our Concrete Strategies (DFS and Kruskal) into an algorithmic registry exactly when the program boots up. This is a very clean way to make the strategies easily interchangeable. 

### 4. The Context (`MazeEngine` & Config parsing)
Our `MazeEngine` acts as the **Context**, which utilizes the Strategy Pattern. 
- When the program reads `ALGO=dfs` from `config.txt` (or a user presses `a` during live visualization), the engine looks at the registry and instantly swaps out the active algorithm generation object.
- Because of the Strategy Pattern, the visualizer loop inside our engine doesn't need to have a giant `if algo == 'dfs': ... elif algo == 'kruskal': ...` block full of complex math. 
- The engine simply says: `"I don't care which algorithm is currently active, just give me the active initialized object and I will passively call .generate() on it."`

**Why this is reusable**: 
If a developer decides to add a completely new algorithm (like Prim's Algorithm) next year, they do not have to rewrite or touch the `MazeEngine` interface or visualization logic *at all*. They simply create a new `class Prim(MazeAlgorithm):`, throw `@register_algorithm('prim')` on top of it, and the engine will immediately and flawlessly know how to use it!

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
We selected the recursive backtracker because it is fundamentally the easiest and most understandable algorithm for initial implementation. Additionally, it exhibits a bias toward generating highly extended, singular "river-like" corridors and far fewer branching pathways, which is mathematically optimal for building classic labyrinths.

### 2. Kruskal's Algorithm (Randomized)
A robust modernized minimum-spanning-tree builder that leverages a rapid Disjoint-Set (`Union-Find`) grouping structure utilizing rank-merging and path compressions.

**Why we chose it**: 
Based on our architectural research into spanning tree methodologies (referenced below), we chose Kruskal's simply because the resulting maze topology "looks cool". It creates a highly jagged map clustered entirely out of countless minuscule dead-ends, structurally and visually contrasting the long, winding rivers produced by DFS.

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

## Code Reusability

Our architecture was intentionally built with extensibility and reusability in mind. Key reusable components include:

- **Algorithm Registration System (`@register_algorithm` and `MazeAlgorithm` base class)**: The core algorithmic engine is highly decoupled from the main execution process. Any developer can implement a new maze generation algorithm (e.g., Prim's, Wilson's) by simply extending the `MazeAlgorithm` base class and injecting it using the `@register_algorithm` decorator. This system is entirely self-contained and reusable for any graph-generation project.
- **Configuration Parser (`Parser.py`)**: The parser is designed with single-responsibility methods for validation, error handling, and default value generation. It easily adapts to ingest arbitrary `KEY=VALUE` data structures for other Python applications simply by extending the expected keys.
- **Hexadecimal Bitmasking Engine**: The internal logic representing cell connections via binary values handles directional checks efficiently and outputs serialized string layers easily transferable to any external rendering tool independent of our display engine.

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

## Project Management

This architecture was developed collaboratively within the scope of the 42 curriculum.

### 1. Roles of Each Team Member

| Contributor | Roles & Responsibilities |
|-----|------|
| **vlnikola** | Engineered core generator architecture and dynamic decorators (`@register_algorithm`), built config parsing and ingestion routines (`Parser`), implemented the `DFS` algorithm and the structural 42-Pattern overlay logic, handled hex bitmask grid output formatting, and constructed execution binaries alongside automation in the `Makefile`. |
| **ngvo** | Designed the `MazeEngine` and asynchronous terminal event listeners, managed robust terminal UI updates alongside iterative dynamic mathematical rendering, built thematic array layouts, developed the algorithmic `Kruskal's` union-find sequence, and deployed recursive loop solving pathfinders. |

### 2. Anticipated Planning vs Evolution

Initially, we planned to build a static continuous-loop generation engine with hardcoded algorithms mapped directly to our CLI. We expected the rendering to simply loop print statements at the end of execution. 
However, as development evolved, we prioritized visual interactivity. We significantly refactored the execution process to decouple visual rendering logic natively from math processing functions. Wrapping generation arrays in native asynchronous Python iterators (`yield`) allowed simple frame-by-frame UI hooks, resulting in a live-updating visualization engine—a massive evolution from our original plan.

### 3. What Worked Well & What Could Be Improved

**What Worked Well:**
- The `@register_algorithm` decorator pattern effectively decoupled logic, allowing both contributors to implement completely isolated algorithms (DFS and Kruskal's) simultaneously without creating structural merge conflicts.
- Utilizing abstract generic models for validation kept the `Parser` strict and reliable.

**What Could Be Improved:**
- Heavy reliance on standard nested Python lists currently creates minor visual latency on grids larger than `100x100`. Migrating the underlying dynamic matrix mapping to strict static typed arrays (`NumPy`) would dramatically optimize performance.
- The terminal-bound UI restricts full cross-platform visual consistency depending on the user's local console configurations. Exporting the output to a standard web-canvas or graphical engine would resolve visual parity issues.

### 4. Specific Tools Used

- **Git/GitHub**: For source-version control and remote collaboration.
- **Makefile**: Built internally as a wrapper to securely automate virtual environment deployment and streamline execution.
- **Mypy**: Enabled aggressive static type-checking continuously during generation.
- **Flake8**: Used to uniformly restrict styling inconsistencies.
- **Agentic Code-Assistants (e.g., ChatGPT / Gemini)**: Leveraged safely as consultative platforms for structural Python optimization, parsing strategy reviews, and strict static-typing constraint checks.

---

## Resources 

- **Language Features**: [w3schools](https://www.w3schools.com/python/) and [GeeksforGeeks](https://www.geeksforgeeks.org/python-programming-language/) - for Python 3.10+ features and syntax.
    - [RealPython's introduction to python generators](https://realpython.com/introduction-to-python-generators/)
- **Underlying Logic Structure**: [Researched potential algorithms to implement](https://professor-l.github.io/mazes/) & [Standard Kruskal's Min Spanning Tree methodology](https://www.w3schools.com/dsa/dsa_algo_mst_kruskal.php)
- **Strategy Pattern**: [Strategy Pattern](https://refactoring.guru/design-patterns/strategy)
- **Bitmasking**: [Use of Tile Bitmasking to auto-tile level layouts](https://code.tutsplus.com/how-to-use-tile-bitmasking-to-auto-tile-your-level-layouts--cms-25673t)
- **AI Support Guidelines**: Agentic Code-Assistant tools were incorporated selectively strictly as rapid structural refactorization consultants and for documentation purposes (docstrings, README). AI tools explicitly helped us restructure monolithic ingestion code natively into single-responsibility standards, resolved rigid `mypy` static typing edge-case flags during decorator integrations, and assisted in tracking structural collision errors inside early Bitmask mapping serialization. All logic flow architecture, implementation concepts, and system states were designed intrinsically by humans.