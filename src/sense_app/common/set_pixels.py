"""Wrappers around SenseHat set pixels"""

from pathlib import Path
from json import loads
from typing import Union
from asyncio import Event, sleep

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

    def set(self):
        """Sets the display"""
        raise NotImplementedError("please implement me")

    async def rotater(self, async_event: Event, wait_time: int = 1) -> None:
        """rotates the display until the async event is set"""
        while not async_event.is_set():
            for r in [0, 90, 180, 270]:
                # A double check here so we don't continue the full loop if the async event has
                # been set. Its a little whiffy, but I think its still the cleanest option.
                if not async_event.is_set():
                    self.hat.set_rotation(r, redraw=True)
                    await sleep(wait_time)
                else:
                    break
        self.hat.set_rotation(0, redraw=True)  # Set back to default

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
