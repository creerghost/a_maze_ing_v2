*This project has been created as part of the 42 curriculum by vlnikola, ngvo.*

# A-Maze-Ing 

## Description
A-Maze-Ing is a highly modular, terminal-based procedural maze generator constructed in Python. The project's primary goal is to provide a visually captivating interactive environment capable of rendering mathematically perfect generated mazes in real-time. It leverages advanced algorithmic approaches to build pathways and seamlessly display them utilizing unique visual text palettes right in depth of your console. 

## Instructions

**Installation**
Ensure you have Python 3.10+ installed on your system. 
Clone the repository:
```bash
git clone git@github.com:creerghost/a_maze_ing_v2.git
cd a_maze_ing_v2
```

**Execution**
The application natively hooks into `Make` workflows for ease of automated virtual environment orchestration and execution. You only need a standard configuration configuration structurally matching the schema format.
```bash
make run
```
Which essentially abstracts:
```bash
venv/bin/python a_maze_ing.py config.txt
```

Once running, you can utilize the interactive UI during the terminal render output:
- `a`: Change algorithm
- `g`: Generate new maze randomly (next sequence)
- `s`: Show/Hide maze solution path
- `t`: Next color theme palette
- `q`: Quit

## Config File Structure
The project dictates generation boundaries utilizing an explicit `.txt` map format consisting of native `KEY=VALUE` variables. All coordinates map logically to `0`-indexed parameters.

```env
WIDTH=10               # Integer: Grid width.
HEIGHT=10              # Integer: Grid height.
ENTRY=0,0              # Tuple(x, y): Starting entry coordinates.
EXIT=9,9               # Tuple(x, y): Exit target.
OUTPUT_FILE=maze.txt   # String: File target for serializing final map bitmasks.
PERFECT=True           # Boolean: (Optional) Enforce perfect loops mathematically.
RENDER_DELAY=0.01      # Float: (Optional) UI animation lag modifier per cell.
ALGO=dfs               # String: (Optional) Bound generator logic (dfs, kruskal)
SEED=12345             # Integer: (Optional) Explicit randomizer binding for replication. 
```

## Maze Generation Algorithms

We deployed two natively distinct maze algorithms to support vast architectural variance dynamically: **Depth-First Search (Recursive Backtracker)** and **Randomized Kruskal's Algorithm**.

**Why we chose them:**
- **DFS**: Generating deeply winding "river" patterns with notably long singular corridors inherently limits branching. This was ideal for building classic confusing labyrinths. 
- **Kruskal's**: Operates heavily off randomized subset aggregations (Union-Find) leaving a highly jagged layout comprised of immense branching dead-ends everywhere, providing entirely disparate map structures than DFS natively, enriching the scope.

## Reusability & Architecture Features
The generation topology is extremely decoupled. 
By utilizing the abstract `MazeAlgorithm` base class, all backend data states orchestrating structural components (`generate()` yields, 42-Pattern overlay configurations, bound injections) are natively inherited globally. 

Additionally, the project employs a dynamic Python decorator pipeline (`@register_algorithm()`). To instantiate entirely new maze features (Prim's, Eller's, etc.), developers only need to map out the algorithm natively within `algorithms.py` and assign a new Enum pointer in `constants.py`. The internal `MazeEngine` absorbs it inherently on run initialization, meaning you can plug new algorithms continuously with zero changes to the underlying engine loop.

## Team & Project Management

**Roles**
- **vlnikola**: Core backend architecture (Engine event handling, `Parser` data validations module, deterministic generation `SEED` flows, AI agent scaffolding).
- **ngvo**: Maze mathematical algorithm implementations, recursive visual bindings, themes UI array structures (colors), structural bitmask serialization schema outputs.

**Planning & Evolution**
Initially, the project was mapped to simply brute-force DFS uniformly over a static looping render array. However, this heavily penalized code reuse when integrating Kruskal. We subsequently pivoted architecture actively allocating specific runtime data abstractions explicitly to a separated `MazeEngine.py`, scaling out logic gracefully.

**Retrospective**
The abstraction architecture succeeded wonderfully; merging mathematical arrays over UI structures became seamless. Next time, optimizing iterative Python nested list mapping dynamically during large grids (`200x200` width maps) with NumPy backend references might severely bump native compute ceiling levels to handle gigantic maps instantly. 

**Tools Used**
We natively executed Python alongside standard `Make` structures for pipeline wrappers.

## Advanced Features
- **Deterministic Replication**: Explicit `SEED` mappings serialize generation states flawlessly so you can recreate beautiful mazes perfectly sequentially to friends.
- **Dynamic Theming**: Interactive command injections mapping vibrant live colors universally across DFS and Kruskal (`Biohazard`, `Virus`, `Classic`) without pausing the engine loop.
- **Hexadecimal Bitmask Exporting**: Converts map arrays natively to exact numerical specification rules, spitting perfect logical structures iteratively upon every generation cycle cleanly.

## Resources
- **Algorithms overview**: Maze generation logic was researched mathematically leveraging wikipedia's standard algorithmic paths (https://en.wikipedia.org/wiki/Maze_generation_algorithm).
- **AI Usage**: will lie for no reason