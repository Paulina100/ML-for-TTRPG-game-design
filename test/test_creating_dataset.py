import pathlib
from copy import deepcopy

import pandas as pd
import pytest

from training.analysis_functions import get_merged_bestiaries, unpack_column
from training.creating_dataset import (
    _create_df_with_basic_values,
    create_dataframe,
    get_subcolumn,
    is_path_correct,
    load_data_with_nan_val,
    load_subcolumn_as_value,
    move_values_level_up,
)


DATASETS_DIR = pathlib.Path(__file__).parent.parent / "pathfinder_2e_data"
DATASET_FILES = [
    "pathfinder-bestiary.db",
    "pathfinder-bestiary-2.db",
    "pathfinder-bestiary-3.db",
]
DATASET_PATHS = [f"{DATASETS_DIR}/{file}" for file in DATASET_FILES]
BESTIARY = get_merged_bestiaries(DATASET_PATHS)


# is_path_correct
def test_check_paths_wrong_path():
    assert not is_path_correct("pathfinder_2e_data/pathfinder-bestiar.db")


def test_check_paths_wrong_file_type():
    assert not is_path_correct("requirements.txt")


def test_check_right_path():
    assert is_path_correct(DATASET_PATHS[0])


# get_subcolumn
def test_get_subcolumn():
    system = unpack_column(BESTIARY, "system")
    pd.testing.assert_frame_equal(system, get_subcolumn(BESTIARY, "system"))

    abilities = unpack_column(system, "abilities")
    pd.testing.assert_frame_equal(
        abilities, get_subcolumn(BESTIARY, "system/abilities")
    )


def test_wrong_key_get_subcolumn():
    with pytest.raises(KeyError):
        get_subcolumn(BESTIARY, "abilities/system")


# move_values_level_up
def test_move_values_level_up():
    level_up_function = move_values_level_up("mod")
    abilities = get_subcolumn(BESTIARY, "system/abilities")
    test_abilities = deepcopy(abilities)

    level_up_abilities = level_up_function(abilities)
    for col in test_abilities.columns:
        for i, row in test_abilities.iterrows():
            row[col] = row[col].get("mod")

    test_abilities = test_abilities.apply(pd.to_numeric)

    pd.testing.assert_frame_equal(level_up_abilities, test_abilities)


# load_subcolumn_as_value
def test_load_subcolumn_as_value():
    ac = get_subcolumn(BESTIARY, "system/attributes/ac")
    ac_test = deepcopy(ac)

    load_ac = load_subcolumn_as_value("ac")
    ac = load_ac(ac)
    ac_test = pd.DataFrame(data=ac_test.value)
    ac_test.columns = ["ac"]

    pd.testing.assert_frame_equal(ac, ac_test)


# load_data_with_nan_val
def test_load_data_with_nan_val():
    df = get_subcolumn(BESTIARY, "system/resources/focus")

    get_focus_func = load_data_with_nan_val(
        column_name="focus", original_column_name="max", nan_replace_val=-1
    )
    focus = get_focus_func(df)

    assert list(focus.columns) == ["focus"]  # right column name

    assert (
        focus[df["max"].isnull()]["focus"] == -1
    ).all()  # all rows with null have nan_replace_val

    pd.testing.assert_series_equal(
        df[df["max"].notnull()]["max"].rename("focus"),
        focus[focus["focus"] != -1]["focus"],
    )
    # rows with non-null values have values from original df


# _create_df_with_basic_values
def test_create_df_with_basic_values():
    basic_bestiary = _create_df_with_basic_values(BESTIARY)

    books = load_subcolumn_as_value("book")(
        get_subcolumn(BESTIARY, "system/details/source")
    )
    levels = load_subcolumn_as_value("level")(
        get_subcolumn(BESTIARY, "system/details/level")
    )
    levels.loc[levels["level"] > 20, "level"] = 21

    pd.testing.assert_frame_equal(pd.DataFrame(data=basic_bestiary["book"]), books)

    pd.testing.assert_frame_equal(pd.DataFrame(data=basic_bestiary["level"]), levels)


# create_dataframe
def test_create_dataframe():
    test_dataframe = pd.read_json("../output/bestiary_system_basic.json")
    books = load_subcolumn_as_value("book")(
        get_subcolumn(BESTIARY, "system/details/source")
    )

    test_dataframe["book"] = books["book"]
    test_dataframe = test_dataframe.reset_index(drop=True)
    test_dataframe.loc[test_dataframe["level"] > 20, "level"] = 21

    bestiary_dataframe = create_dataframe(DATASET_PATHS)
    pd.testing.assert_frame_equal(
        test_dataframe.sort_index(axis=1), bestiary_dataframe.sort_index(axis=1)
    )
