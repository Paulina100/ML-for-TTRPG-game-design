from copy import deepcopy

import pytest
import pandas as pd
from training.creating_dataset import (
    get_sub_column,
    move_values_level_up,
    check_paths,
    load_sub_column_as_value,
    create_df_with_basic_values,
    create_dataframe,
)
from training.analysis_functions import import_merged_bestiaries, unpack_column

paths = [
    "../pathfinder_2e_data/pathfinder-bestiary.db",
    "../pathfinder_2e_data/pathfinder-bestiary-2.db",
    "../pathfinder_2e_data/pathfinder-bestiary-3.db",
]
bestiaries = import_merged_bestiaries(paths)


# check_paths


def test_check_paths_wrong_path():
    path = "../pathfinder_2e_data/pathfinder-bestiar.db"
    with pytest.raises(Exception) as excinfo:
        check_paths([path])
    # print(excinfo.value)
    assert f"Path {path} does not exist" in str(excinfo.value)


def test_check_paths_wrong_file_type():
    path = "../requirements.txt"
    with pytest.raises(Exception) as excinfo:
        check_paths([path])
    # print(excinfo.value)
    assert f"Expected db or json file, got {path}" in str(excinfo.value)


def test_check_right_path():
    path = "../pathfinder_2e_data/pathfinder-bestiary.db"
    assert check_paths([path]) is None


# get_sub_column
def test_get_sub_column():
    system = unpack_column(bestiaries, "system").reset_index(drop=True)
    pd.testing.assert_frame_equal(system, get_sub_column(bestiaries, "system"))

    abilities = unpack_column(system, "abilities").reset_index(drop=True)
    pd.testing.assert_frame_equal(
        abilities, get_sub_column(bestiaries, "system/abilities")
    )


# move_values_level_up
def test_move_values_level_up():
    level_up_results = move_values_level_up("mod")
    abilities = get_sub_column(bestiaries, "system/abilities")
    test_abilities = deepcopy(abilities)

    level_up_abilities = level_up_results(abilities)
    for col in test_abilities.columns:
        for i, row in test_abilities.iterrows():
            row[col] = row[col].get("mod")

    test_abilities = test_abilities.apply(pd.to_numeric)

    pd.testing.assert_frame_equal(level_up_abilities, test_abilities)


# load_sub_column_as_value
def test_load_sub_column_as_value():
    ac = get_sub_column(bestiaries, "system/attributes/ac")
    ac_test = deepcopy(ac)

    load_ac = load_sub_column_as_value("ac")
    ac = load_ac(ac)
    ac_test = pd.DataFrame(data=ac_test.value)
    ac_test.columns = ["ac"]

    pd.testing.assert_frame_equal(ac, ac_test)


# create_df_with_basic_values
def test_create_df_with_basic_values():
    basic_bestiary = create_df_with_basic_values(bestiaries)

    books = load_sub_column_as_value("book")(
        get_sub_column(bestiaries, "system/details/source")
    )
    levels = load_sub_column_as_value("level")(
        get_sub_column(bestiaries, "system/details/level")
    )

    pd.testing.assert_frame_equal(pd.DataFrame(data=basic_bestiary["book"]), books)

    pd.testing.assert_frame_equal(pd.DataFrame(data=basic_bestiary["level"]), levels)


# create_dataframe
def test_create_dataframe():
    test_dataframe = pd.read_json("../output/bestiary_system_basic.json")
    books = load_sub_column_as_value("book")(
        get_sub_column(bestiaries, "system/details/source")
    )

    test_dataframe["book"] = books["book"]

    bestiary_dataframe = create_dataframe()
    pd.testing.assert_frame_equal(
        test_dataframe.sort_index(axis=1), bestiary_dataframe.sort_index(axis=1)
    )
