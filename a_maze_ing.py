import sys
import os
from MazeGenerator.Parser import Parser
from MazeGenerator.exceptions import ParserError
from MazeGenerator.MazeRenderer import MazeRenderer
from typing import Dict, Any


def print_menu() -> None:
    print("\n=== A-Maze-Ing ===")
    print("a - Change algorithm")
    print("g - Generate new maze")
    print("s - Show/Hide solution path")
    print("t - Next theme")
    print("q - Quit")
    print("====================")


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python a_maze_ing.py <config_file>")
        sys.exit(1)

    config_file: str = sys.argv[1]

    if not os.path.exists(config_file):
        print(f"Error: Config file '{config_file}' not found.")
        sys.exit(1)

    try:
        parser: Parser = Parser(config_file)
        config: Dict[str, Any] = parser.parse()
        print(config)
    except ParserError as e:
        print(f"ParserError: {e}")
        sys.exit(1)

    from MazeGenerator.constants import Themes
    from MazeGenerator.algorithms import DFSAlgorithm
    import time

    algorithm: DFSAlgorithm = DFSAlgorithm(config['WIDTH'], config['HEIGHT'])

    theme = Themes.CLASSIC

    for maze_state in algorithm.generate():
        renderer: MazeRenderer = MazeRenderer(
            maze_state, theme,
            config.get('ENTRY'), config.get('EXIT')
        )
        output = renderer.render()

        os.system('cls' if os.name == 'nt' else 'clear')

        for row in output:
            print("".join(row))

        time.sleep(0.01)


if __name__ == "__main__":
    main()
