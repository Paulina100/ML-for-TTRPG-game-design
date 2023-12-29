import json

import dice_ml
import pandas as pd
from constants import ORDERED_CHARACTERISTICS_FULL, THRESHOLD
from dice_ml import Dice


def generate_counterfactuals(
    monster_stats: dict,
    model,
    new_level: int,
    df: pd.DataFrame,
    total_cf: int = 5,
    ordered_characteristics: list[str] = ORDERED_CHARACTERISTICS_FULL,
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
    # cfs - CounterfactualExplanations object
    # cfs.to_json() returns json string (type: str)
    # example:
    #     '{"test_data": [[[3.0, 2.0, 2.0, -4.0, 1.0, -1.0, 17.0, 17.0, 1.0001450258428668]]],
    #     "cfs_list": [[[3.0, 2.0, 3.0, -4.0, 1.0, 1.0, 15.0, 18.0, -6.624720117542893e-05]]],
    #     "local_importance": null, "summary_importance": null,
    #     "data_interface": {"outcome_name": "level", "data_df": "dummy_data"},
    #     "feature_names": ["str", "dex", "con", "int", "wis", "cha", "ac", "hp"],
    #     "feature_names_including_target": ["str", "dex", "con", "int", "wis", "cha", "ac", "hp", "level"],
    #     "model_type": "regressor", "desired_class": "opposite", "desired_range": [-0.67, 0.33],
    #     "metadata": {"version": "2.0"}}'

    cfs = cf_json["cfs_list"][0]
    # Query can consist of more than one instance
    # so each data about original stats and counterfactuals is given as a list of lists - we always have one instance
    # "cfs_list": [[[1.0, 5.0, 2.0, 1.0, 7.0, 2.0, 29.0, 215.0, 10.231964445152919]]]

    cfs.sort(key=lambda x: abs(new_level - x[-1]), reverse=True)

    # If the predicted level is equal to `new_level - 1 + THRESHOLD`,
    # `calculate_level` would qualify this counterfactual for new_level - 1, not new_level.
    cfs = [cf[:-1] for cf in cfs if cf[-1] != new_level - 1 + THRESHOLD]

    result = {"values": cfs}

    return result
