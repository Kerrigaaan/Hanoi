import random

from pygame import Color


def random_color() -> Color:
    return Color(
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
    )
