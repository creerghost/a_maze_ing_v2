from typing import Dict, Any
from MazeGenerator.algorithms import ALGORITHMS_REGISTRY


class ParserError(Exception):
    pass


class Parser:
    """
    Parses configuration files containing map bounds and runtime variables.
    """
    def __init__(self, config_file: str):
        """
        Initializes the parser targeting a specific configuration text file.

        Args:
            config_file (str): System path to configuration text file.
        """
        self.config_file = config_file

    def parse(self) -> Dict[str, Any]:
        """
        Ingests config text line by line and outputs a validated config dict.

        Returns:
            Dict[str, Any]: Dict storing parsed config params.

        Raises:
            ParserError: If syntax, types, or bounds are structurally invalid.
        """
        result: Dict[str, Any] = {}
        with open(self.config_file, 'r') as f:

            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line or line.startswith('#'):
                    continue

                if '=' in line:
                    key: str = ""
                    value: str = ""
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip()

                    try:
                        if key in ('WIDTH', 'HEIGHT'):
                            result[key] = int(value)

                        elif key in ('ENTRY', 'EXIT'):
                            x: str = ""
                            y: str = ""
                            x, y = value.split(',')
                            result[key] = (int(x), int(y))

                        elif key == 'PERFECT':
                            if value.lower() not in ('true', 'false'):
                                raise ParserError(f"Invalid value "
                                                  f"for boolean key {key}")
                            result[key] = value.lower() == 'true'

                        elif key == 'OUTPUT_FILE':
                            result[key] = str(value)

                        elif key == 'ALGORITHM' or key == 'ALGO':
                            algo = value.lower()
                            if algo not in ALGORITHMS_REGISTRY:
                                raise ParserError(
                                    f"Invalid value for key {key}. "
                                    f"Available algorithms: "
                                    f"{', '.join(ALGORITHMS_REGISTRY.keys())}"
                                )
                            result[key] = algo

                        elif key == 'RENDER_DELAY':
                            result[key] = float(value)

                        elif key == 'SEED':
                            result[key] = int(value)

                        else:
                            result[key] = value
                    except ValueError:
                        raise ParserError(f"Invalid value for key {key}")
                else:
                    raise ParserError(f"Invalid line {line_num}: {line}")

        expected_schema: Dict[str, type] = {
            'WIDTH': int,
            'HEIGHT': int,
            'ENTRY': tuple,
            'EXIT': tuple,
            'PERFECT': bool,
            'OUTPUT_FILE': str,
            'RENDER_DELAY': float
        }

        for key, expected_type in expected_schema.items():
            if key not in result:
                raise ParserError(f"Missing required key: {key}")
            if not isinstance(result[key], expected_type):
                raise ParserError(f"Invalid type for key {key}")
            if key == 'WIDTH' or key == 'HEIGHT':
                if result[key] <= 0:
                    raise ParserError(f"Invalid value for key {key}")
            if key == 'ENTRY' or key == 'EXIT':
                if not (0 <= result[key][0] < result['WIDTH'] and
                        0 <= result[key][1] < result['HEIGHT']):
                    msg: str = (f"{key} {result[key]} is out of bounds.\n"
                                f"Expected: x from 0 to {result['WIDTH'] - 1} "
                                f"and y from 0 to {result['HEIGHT'] - 1}.")
                    raise ParserError(msg)
                if key == 'EXIT' and result['ENTRY'] == result['EXIT']:
                    raise ParserError("ENTRY and EXIT should not be equal.")
            if key == 'OUTPUT_FILE':
                if not result[key].endswith('.txt') or len(result[key]) <= 4:
                    raise ParserError(f"Invalid value for key {key}")

        return result
