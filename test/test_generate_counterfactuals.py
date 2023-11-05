from test.constants import DATASET_PATHS

import joblib
import pytest

from serving.backend.calculate_level import calculate_level
from serving.backend.constants import ORDERED_CHARACTERISTICS
from serving.backend.generate_counterfactuals import generate_counterfactuals
from training.creating_dataset import load_and_preprocess_data


df = load_and_preprocess_data(
    DATASET_PATHS,
    characteristics=ORDERED_CHARACTERISTICS,
)

testdata = [
    (
        {
            "str": 7,
            "dex": 2,
            "con": 5,
            "int": 1,
            "wis": 2,
            "cha": 1,
            "ac": 29,
            "hp": 215,
        },
        9,
    ),
    (
        {
            "str": -5,
            "dex": 3,
            "con": 1,
            "int": -1,
            "wis": 1,
            "cha": 1,
            "ac": 16,
            "hp": 20,
        },
        3,
    ),
    (
        {
            "str": 12,
            "dex": 9,
            "con": 11,
            "int": 7,
            "wis": 8,
            "cha": 8,
            "ac": 54,
            "hp": 550,
        },
        18,
    ),
]

model = joblib.load(filename="../saved_models/current_model.pkl")


@pytest.mark.parametrize("monster,new_level", testdata)
def test_generate_counterfactuals_t(monster, new_level):
    cfs = generate_counterfactuals(
        monster_stats=monster, model=model, new_level=new_level, df=df
    )

    prev_distance_to_new_level = 0  # check sort
    for cf_nr in range(len(cfs["values"])):
        test_monster = {
            characteristic: cfs["values"][cf_nr][i]
            for i, characteristic in enumerate(monster.keys())
        }
        predicted_level = calculate_level(test_monster, model)
        assert predicted_level == new_level
        distance_to_new_level = abs(predicted_level - new_level)
        assert distance_to_new_level >= prev_distance_to_new_level
        prev_distance_to_new_level = distance_to_new_level
