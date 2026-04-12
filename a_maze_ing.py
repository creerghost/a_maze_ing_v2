"""
Entry point for A-Maze-Ing.
Bootstraps parser and generator.
"""

import sys
import os
from typing import Dict, Any
from MazeGenerator.Parser import Parser, ParserError
from MazeGenerator.MazeEngine import MazeEngine


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
        engine = MazeEngine(
            config['WIDTH'],
            config['HEIGHT'],
            config['ENTRY'],
            config['EXIT'],
            config['OUTPUT_FILE'],
            config.get('ALGORITHM', 'dfs'),
            config.get('RENDER_DELAY', 0.02),
            config.get('PERFECT', True),
            config.get('SEED'),
        )
        engine.run()
    except ParserError as e:
        print(f"ParserError: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
