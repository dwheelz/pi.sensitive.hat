"""Wrappers around SenseHat set pixels"""

from pathlib import Path
from json import loads
from typing import Union

# only importable on a RPi
from sense_hat import SenseHat  # pylint: disable=import-error


class RawSenseHat:
    """Doesn't have any pattern wrappers"""

    def __init__(self) -> None:
        """init"""
        self.hat = SenseHat()

    def enable_low_light(self) -> None:
        """sets the display to low light"""
        self.hat.low_light = True

    def disable_low_light(self) -> None:
        """sets the display back to normal light mode"""
        self.hat.low_light = False

    def clear(self) -> None:
        "clears the display"
        self.hat.clear()

    def set(self, rgb_list: list[list]):
        """Sets the display"""
        self.hat.set_pixels(rgb_list)


# pylint: disable=too-few-public-methods
class SetPattern(RawSenseHat):
    """Base Pattern class"""

    def __init__(self, pattern: Union[list, None] = None) -> None:
        """init"""
        self.pattern = pattern
        super().__init__()

    def set(self) -> None:
        "sets the pattern to the display. Overrides the inherited method"
        self.hat.set_pixels(self.pattern)


class SetPatternFromJsonFile(SetPattern):
    """Patterns from Json files"""

    def __init__(self, filepath: str) -> None:
        """init"""
        super().__init__(loads(Path(filepath).read_text(encoding="utf-8")))
