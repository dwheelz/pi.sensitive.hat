"""Wrappers around SenseHat set pixels"""

from pathlib import Path
from json import loads

# only importable on a RPi
from sense_hat import SenseHat  # pylint: disable=import-error


CLEAR = [[0, 0, 0] for _ in range(64)]


# pylint: disable=too-few-public-methods
class SetPattern:
    """Base Pattern class"""

    def __init__(self, pattern: list) -> None:
        """init"""
        self.pattern = pattern
        self.hat = SenseHat()

    def set(self) -> None:
        "sets the pattern to the display"
        self.hat.set_pixels(self.pattern)

    def clear(self) -> None:
        "clears the display"
        self.hat.set_pixels(CLEAR)


class SetPatternFromJsonFile(SetPattern):
    """Patterns from Json files"""

    def __init__(self, filepath: str) -> None:
        """init"""
        super().__init__(loads(Path(filepath).read_text(encoding="utf-8")))
