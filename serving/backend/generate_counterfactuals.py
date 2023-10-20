import json

import dice_ml
import pandas as pd
from dice_ml import Dice


characteristics = ["cha", "con", "dex", "int", "str", "wis", "ac", "hp"]
threshold = 0.33


def generate_counterfactuals(
    monster_stats: dict, model, new_level: int, df: pd.DataFrame, total_cf: int = 5
) -> dict[str, float]:
    """
    Generate counterfactual explanations for a monster's characteristics to achieve a new level.

    :param monster_stats: A dictionary containing the monster's current characteristics and values.
    :param model: The machine learning model used for prediction.
    :param new_level: The target level the monster should achieve.
    :param df: A pandas DataFrame containing other monsters' data for generating explanations.
    :param total_cf: The number of counterfactual explanations to generate.
    :return: A dictionary containing the generated counterfactual explanations *values* and information whether characteristic was *modified*.
    """
    query = pd.DataFrame.from_records([monster_stats])
    query = query[characteristics]
    df = df[characteristics + ["level"]]
    continuous_features = df.drop(columns=["level"]).columns.tolist()

    d = dice_ml.Data(
        dataframe=df, continuous_features=continuous_features, outcome_name="level"
    )
    m = dice_ml.Model(model=model, backend="sklearn", model_type="regressor")
    exp = Dice(d, m, method="genetic")

    desired_range = [new_level - 1 + threshold, new_level + threshold]

    genetic = exp.generate_counterfactuals(
        query, total_CFs=total_cf, desired_range=desired_range
    )

    cf_json = json.loads(genetic.to_json())

    result = {
        "values": [],
        "modified": [],
    }
    original = cf_json["test_data"][0][0]  # list(monster_stats.values())

    for cf in cf_json["cfs_list"][0]:
        cf = cf[:-1]
        result["values"].append(cf)
        cf_modified = [
            True if val != original[i] else False for i, val in enumerate(cf)
        ]
        result["modified"].append(cf_modified)

    return result
