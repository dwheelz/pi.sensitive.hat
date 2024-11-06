"""Wrappers around SenseHat set pixels"""

from pathlib import Path
from json import loads

# only importable on a RPi
from sense_hat import SenseHat  # pylint: disable=import-error


CLEAR = [[0, 0, 0] for _ in range(64)]


class SetPattern:

    def __init__(self, pattern: list) -> None:
        self.pattern = pattern
        self.hat = SenseHat()

    def clear(self):
        self.hat.set_pixels(CLEAR)


class SetPatternFromJsonFile(SetPattern):

    def __init__(self, filepath: str) -> None:
        super().__init__(loads(Path(filepath).read_text(encoding="utf-8")))

    def set(self):
        self.hat.set_pixels(self.pattern)
