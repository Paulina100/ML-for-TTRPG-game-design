import json
import os
import sys

import dice_ml
import pandas as pd
from dice_ml import Dice


sys.path.insert(0, os.sep.join(os.path.normpath(__file__).split(os.sep)[:-1]))
from constants import ORDERED_CHARACTERISTICS, THRESHOLD


def generate_counterfactuals(
    monster_stats: dict,
    model,
    new_level: int,
    df: pd.DataFrame,
    total_cf: int = 5,
    ordered_characteristics: list[str] = ORDERED_CHARACTERISTICS,
) -> dict[str, list]:
    """
    Generate counterfactual explanations for a monster's characteristics to achieve a new level.

    :param ordered_characteristics: The order of characteristics in the given model.
    :param monster_stats: A dictionary containing the monster's current characteristics and values.
    :param model: The machine learning model used for prediction.
    :param new_level: The target level the monster should achieve.
    :param df: A pandas DataFrame containing other monsters' data for generating explanations.
    :param total_cf: The number of counterfactual explanations to generate.
    :return: A dictionary containing the generated counterfactual explanations *values*.
    """
    query = pd.DataFrame.from_records([monster_stats])
    query = query[ordered_characteristics]
    df = df[ordered_characteristics + ["level"]]
    continuous_features = df.drop(columns=["level"]).columns.tolist()

    d = dice_ml.Data(
        dataframe=df, continuous_features=continuous_features, outcome_name="level"
    )
    m = dice_ml.Model(model=model, backend="sklearn", model_type="regressor")
    exp = Dice(d, m, method="kdtree")

    desired_range = [new_level - 1 + THRESHOLD, new_level + THRESHOLD]

    cfs = exp.generate_counterfactuals(
        query, total_CFs=total_cf, desired_range=desired_range
    )

    cf_json = json.loads(cfs.to_json())

    result = {
        "values": sorted(
            cf_json["cfs_list"][0], key=lambda x: abs(new_level - x[-1]), reverse=True
        )
    }
    # Query can consist of more than one instance
    # so each data about original stats and counterfactuals is given as a list of lists - we always have one instance
    # "cfs_list": [[[1.0, 5.0, 2.0, 1.0, 7.0, 2.0, 29.0, 215.0, 10.231964445152919]]]

    result["values"] = [
        cf[:-1] for cf in result["values"] if cf[-1] != new_level - 1 + THRESHOLD
    ]
    # If the predicted level is equal to `new_level - 1 + THRESHOLD`,
    # `calculate_level` would qualify this counterfactual for new_level - 1, not new_level.

    return result
