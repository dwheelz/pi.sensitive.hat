"""Generates patterns (RGB lists)"""

from random import randint, choice
from typing import Callable


# pylint: disable=too-few-public-methods
class ConstrainedRandPatternGen:
    """Generates Random patterns within specified broad predefined colours"""

    ORANGE: list = [[100, 50, 0], [180, 100, 0]]
    RED: list = [[90, 0, 0], [180, 40, 30]]
    BLUE: list = [[0, 0, 100], [0, 80, 180]]
    GREEN: list = [[10, 100, 10], [60, 180, 60]]
    # Death is now a colour, and its surprisingly pretty...
    DEATH: list = [[190, 0, 0], [235, 235, 235]]

    pool : list = [ORANGE, RED, BLUE, GREEN, DEATH]

    @staticmethod
    def _gen_pixel_colour(colour) -> list:
        """Returns a random RGB array from a defined colour range"""
        return [
            randint(colour[0][0], colour[1][0]),
            randint(colour[0][1], colour[1][1]),
            randint(colour[0][2], colour[1][2])
        ]

    def _rgb_generator(self, _callable: Callable) -> list[list]:
        """generates the full 64 element RGB array"""
        generated_list = []
        for _ in range(64):
            generated_list.append(self._gen_pixel_colour(_callable()))
        return generated_list

    def gen_single_colour(self, colour: list) -> list[list]:
        """Generates a random list of 64 nested RGB values within the specified bounds of
        the provided colour (i.e values between ConstrainedRandPatternGen.ORANGE[0] and
        ConstrainedRandPatternGen.ORANGE[1]).
        """
        def _static_colour():
            """simply returns the provided colour value"""
            return colour
        return self._rgb_generator(_static_colour)

    def gen(self) -> list[list]:
        """totally ruddy mental"""
        def _return_random_choice():
            """returns a random choice from the available colours"""
            return choice(self.pool)
        return self._rgb_generator(_return_random_choice)
