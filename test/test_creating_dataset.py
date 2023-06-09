import pathlib

import pandas as pd
import pytest

from training.analysis_functions import get_merged_bestiaries, get_subcolumn
from training.creating_dataset import is_path_correct, load_and_preprocess_data


DATASETS_DIR = pathlib.Path(__file__).parent.parent / "pathfinder_2e_data"
DATASET_FILES = [
    "pathfinder-bestiary.db",
    "pathfinder-bestiary-2.db",
    "pathfinder-bestiary-3.db",
]
DATASET_PATHS = [f"{DATASETS_DIR}/{file}" for file in DATASET_FILES]
BESTIARY = get_merged_bestiaries(DATASET_PATHS)


# is_path_correct
def test_is_path_correct():
    with pytest.raises(ValueError):
        # case: path does not exist
        is_path_correct("pathfinder_2e_data/pathfinder-bestiar.db")

    with pytest.raises(ValueError):
        # case: wrong file type
        is_path_correct("requirements.txt")

    # case: correct path
    assert is_path_correct(DATASET_PATHS[0])


# load_and_preprocess_data
def test_load_and_preprocess_data():
    test_dataframe = pd.read_json("../output/bestiary_system_basic.json")

    test_dataframe["book"] = get_subcolumn(BESTIARY, "system/details/source")["value"]
    test_dataframe["level"] = get_subcolumn(BESTIARY, "system/details/level")["value"]
    test_dataframe["focus"] = get_subcolumn(BESTIARY, "system/resources/focus")["value"]
    test_dataframe["focus"] = test_dataframe["focus"].fillna(-1)
    test_dataframe = test_dataframe.reset_index(drop=True)
    test_dataframe.loc[test_dataframe["level"] > 20, "level"] = 21

    bestiary_dataframe = load_and_preprocess_data(
        DATASET_PATHS, characteristics=["abilities", "ac", "hp", "focus"]
    )

    pd.testing.assert_frame_equal(
        test_dataframe.sort_index(axis=1),
        bestiary_dataframe.sort_index(axis=1),
        check_dtype=False,
    )
