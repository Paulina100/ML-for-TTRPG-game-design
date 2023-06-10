import math

import pandas as pd


def _round_monster_level(level: float) -> int:
    """
    Rounds the monster's level based on a lower threshold.

    If the fractional part of the level is greater than 0.33, the level is rounded up to the nearest whole number.
    Otherwise, the level is rounded down to the nearest whole number.

    :param level: monster's level to round
    :return: rounded monster's level as int
    """

    if (level % 1) > 0.33:
        return math.ceil(level)
    else:
        return math.floor(level)


def calculate_level(monster_stats: dict, model) -> int:
    """
    Calculates the monster's level based on its statistics
    :param monster_stats: dict with the monster's statistics to load
    :param model: machine learning model used for prediction
    :return: int containing calculated monster's level
    """

    monster_X = pd.DataFrame.from_records([monster_stats])

    monster_y = model.predict(monster_X)
    monster_y = _round_monster_level(monster_y[0])

    return monster_y
