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
        raw_config: Dict[str, str] = {}
        with open(self.config_file, 'r') as f:
            for line_num, line in enumerate(f, 1):
                clean_line = line.strip()
                if not clean_line or clean_line.startswith('#'):
                    continue

                if '=' not in clean_line:
                    raise ParserError(f"Invalid line {line_num}: {line}")

                key, value = clean_line.split('=', 1)
                raw_config[key.strip()] = value.strip()

        parsed_config = self._validate_and_cast(raw_config)
        self._check_bounds(parsed_config)
        return parsed_config

    def _validate_and_cast(self, raw_config: Dict[str, str]) -> Dict[str, Any]:
        """Casts string values into native Python types based on schema."""
        parsed: Dict[str, Any] = {}

        schema_types = {
            'WIDTH': int,
            'HEIGHT': int,
            'RENDER_DELAY': float,
            'SEED': int,
            'OUTPUT_FILE': str
        }

        for key, value in raw_config.items():
            try:
                if key in schema_types:
                    parsed[key] = schema_types[key](value)
                elif key in ('ENTRY', 'EXIT'):
                    x, y = value.split(',')
                    parsed[key] = (int(x), int(y))
                elif key == 'PERFECT':
                    val = value.lower()
                    if val not in ('true', 'false'):
                        raise ParserError(f"Invalid boolean {value} for {key}")
                    parsed[key] = (val == 'true')
                elif key in ('ALGORITHM', 'ALGO'):
                    algo = value.lower()
                    if algo not in ALGORITHMS_REGISTRY:
                        raise ParserError(
                            f"Invalid value for key {key}. "
                            f"Available algorithms: "
                            f"{', '.join(ALGORITHMS_REGISTRY.keys())}"
                        )
                    parsed['ALGORITHM'] = algo
                else:
                    parsed[key] = value
            except ValueError:
                raise ParserError(f"Invalid value for key {key}")

        return parsed

    def _check_bounds(self, parsed: Dict[str, Any]) -> None:
        """Verifies missing keys and enforces logic constraints."""
        required = ['WIDTH', 'HEIGHT', 'ENTRY', 'EXIT', 'OUTPUT_FILE']
        for req in required:
            if req not in parsed:
                raise ParserError(f"Missing required key: {req}")

        parsed.setdefault('ALGORITHM', 'dfs')
        parsed.setdefault('RENDER_DELAY', 0.02)
        parsed.setdefault('PERFECT', True)
        parsed.setdefault('SEED', None)

        if parsed['WIDTH'] <= 0 or parsed['HEIGHT'] <= 0:
            raise ParserError("WIDTH and HEIGHT must be > 0.")

        for pt in ('ENTRY', 'EXIT'):
            x, y = parsed[pt]
            if not (0 <= x < parsed['WIDTH'] and 0 <= y < parsed['HEIGHT']):
                msg = (f"{pt} {parsed[pt]} is out of bounds.\n"
                       f"Expected: x from 0 to {parsed['WIDTH'] - 1} "
                       f"and y from 0 to {parsed['HEIGHT'] - 1}.")
                raise ParserError(msg)

        if parsed['ENTRY'] == parsed['EXIT']:
            raise ParserError("ENTRY and EXIT should not be equal.")

        out_file = parsed['OUTPUT_FILE']
        if not out_file.endswith('.txt') or len(out_file) <= 4:
            raise ParserError("OUTPUT_FILE must be a valid .txt file")
