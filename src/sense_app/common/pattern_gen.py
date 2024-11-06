"""Generates patterns (RGB lists)"""

from random import randint


# pylint: disable=too-few-public-methods
class ConstrainedRandPatternGen:
    """Generates Random patterns within specified broad predefined colours"""

    ORANGE: list = [[100, 50, 0], [180, 100, 0]]
    RED: list = [[90, 0, 0], [180, 40, 30]]
    BLUE: list = [[0, 0, 100], [0, 80, 180]]
    GREEN: list = [[10, 100, 10], [60, 180, 60]]
    # Death is now a colour, and its surprisingly pretty...
    DEATH: list = [[190, 0, 0], [235, 235, 235]]

    @staticmethod
    def gen(colour: list) -> list:
        """Generates a random list of 64 nested RGB values within the specified bounds of
        the provided colour (i.e values between ConstrainedRandPatternGen.ORANGE[0] and
        ConstrainedRandPatternGen.ORANGE[1]).
        """
        generated_list = []
        for _ in range(64):
            generated_list.append(
                [
                    randint(colour[0][0], colour[1][0]),
                    randint(colour[0][1], colour[1][1]),
                    randint(colour[0][2], colour[1][2])
                ]
            )
        return generated_list
