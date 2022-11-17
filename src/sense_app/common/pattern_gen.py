"""Generates patterns (RGB lists)"""

from random import randint


class RandPatternGen:
    """Generates Random patterns within specified broad predefined colours"""

    ORANGE: list = [[100, 50, 0], [180, 100, 0]]
    RED: list = [[100, 0, 0], [180, 40, 0]]
    BLUE: list = [[0, 0, 100], [0, 80, 180]]
    GREEN: list = [[0, 100, 0], [40, 180, 40]]
    DEATH: list = [[00, 200, 00], [0, 240, 0]]  # Death is now a colour, and its very red...

    def gen(self, colour: list) -> list:
        """Generates a random list of 64 nested RGB values within the specified bounds of
        the provided colour (i.e values between self.ORANGE[0], self.ORANGE[1]).
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
