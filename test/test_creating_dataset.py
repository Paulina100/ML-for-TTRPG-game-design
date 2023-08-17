import pathlib

import numpy as np
import pandas as pd
import pytest

from training.analysis_functions import get_merged_bestiaries, get_subcolumn
from training.creating_dataset import (
    count_damage_expected_value,
    get_characteristic_from_list,
    get_max_melee_bonus_damage,
    get_nr_of_spells_with_lvl,
    is_path_correct,
    load_and_preprocess_data,
    split_characteristics_into_groups,
)


DATASETS_DIR = pathlib.Path(__file__).parent.parent / "pathfinder_2e_data"
DATASET_FILES = [
    "pathfinder-bestiary.db",
    "pathfinder-bestiary-2.db",
    "pathfinder-bestiary-3.db",
]
DATASET_PATHS = [f"{DATASETS_DIR}/{file}" for file in DATASET_FILES]
BESTIARY = get_merged_bestiaries(DATASET_PATHS)


def test_is_path_correct():
    with pytest.raises(ValueError):
        # case: path does not exist
        is_path_correct("pathfinder_2e_data/pathfinder-bestiar.db")

    with pytest.raises(ValueError):
        # case: wrong file type
        is_path_correct("requirements.txt")

    # case: correct path
    assert is_path_correct(DATASET_PATHS[0])


def test_split_characteristics_into_groups():
    test_speeds = {"fly"}
    test_weaknesses = {"good_weakness"}
    test_resistances = {"fire_resistance"}
    test_special_characteristics = {"ranged"}
    test_characteristics_rename = ["immunities", "int"]

    input_characteristics = [
        "wrong_one",
        "fly",
        "good_weakness",
        "fire_resistance",
        "ranged",
        "immunities",
        "int",
    ]

    (
        speeds,
        weaknesses,
        resistances,
        special_characteristics,
        characteristics_rename,
    ) = split_characteristics_into_groups(input_characteristics)

    assert (
        speeds,
        weaknesses,
        resistances,
        special_characteristics,
        characteristics_rename,
    ) == (
        test_speeds,
        test_weaknesses,
        test_resistances,
        test_special_characteristics,
        test_characteristics_rename,
    )


def test_get_characteristic_from_list():
    test_data = pd.Series(
        data=[
            [{"type": "fire", "value": 5}, {"type": "cold", "value": 2}],
            [{"type": "cold", "value": 2}],
            np.nan,
        ]
    )
    results = pd.Series(data=[5, 0, 0])

    pd.testing.assert_series_equal(
        results, test_data.apply(lambda x: get_characteristic_from_list(x, "fire"))
    )


def test_get_nr_of_spells_with_lvl():
    test_data = pd.Series(
        data=[
            [
                {
                    "system": {
                        "category": {"value": "spell"},
                        "traits": {"value": []},
                        "level": {"value": 1},
                    },
                    "type": "spell",
                },
                {"type": "melee"},
            ],
            [
                {"system": {"category": {"value": "not spell"}}, "type": "spell"},
                {
                    "system": {
                        "category": {"value": "spell"},
                        "traits": {"value": ["cantrip"]},
                    },
                    "type": "spell",
                },
                {
                    "system": {
                        "category": {"value": "spell"},
                        "traits": {"value": []},
                        "level": {"value": 2},
                    },
                    "type": "spell",
                },
            ],
        ]
    )

    results = pd.Series(data=[1, 0])

    pd.testing.assert_series_equal(
        results, test_data.apply(lambda x: get_nr_of_spells_with_lvl(x, 1))
    )


def test_count_damage_expected_value():
    test_data = pd.Series(
        data=[
            {"not important key": {"damage": "2d8"}},
            {"not important key": {"damage": "2d8 + 4"}},
            {"not important key": {"damage": "2d8 - 3"}},
            {"not important key": {"damage": "2d8"}, "different key": {"damage": "5"}},
        ]
    )
    result = pd.Series(data=[9, 13, 6, 14])

    pd.testing.assert_series_equal(
        result, test_data.apply(count_damage_expected_value), check_dtype=False
    )


def test_get_max_melee_bonus_damage():
    test_data = pd.Series(
        data=[
            [
                {
                    "system": {
                        "weaponType": {"value": "melee"},
                        "bonus": {"value": 24},
                        "damageRolls": {"not important key": {"damage": "2d8"}},
                    },
                    "type": "melee",
                },
                {
                    "system": {
                        "weaponType": {"value": "melee"},
                        "bonus": {"value": 20},
                        "damageRolls": {"not important key": {"damage": "2d6"}},
                    },
                    "type": "melee",
                },
                {"type": "spell"},
            ],
            [
                {
                    "system": {
                        "weaponType": {"value": "ranged"},
                        "bonus": {"value": 20},
                        "damageRolls": {"not important key": {"damage": "2d6"}},
                    },
                    "type": "melee",
                },
            ],
        ]
    )

    results = pd.DataFrame(
        data=[
            {"melee_bonus": 24, "melee_exp_val": 9},
            {"melee_bonus": 0, "melee_exp_val": 0},
        ]
    )

    test_results = pd.DataFrame()
    test_results["melee_bonus"], test_results["melee_exp_val"] = zip(
        *test_data.apply(lambda x: get_max_melee_bonus_damage(x, "melee"))
    )

    pd.testing.assert_frame_equal(test_results, results, check_dtype=False)


def test_load_and_preprocess_data():
    test_dataframe = pd.read_json("../output/bestiary_system_basic.json")

    column_paths = {
        "book": "system/details/source",
        "focus": "system/resources/focus",
        "fortitude": "system/saves/fortitude",
    }

    for colum_name, path in column_paths.items():
        test_dataframe[colum_name] = get_subcolumn(BESTIARY, path)["value"]

    test_dataframe["immunities"] = get_subcolumn(
        BESTIARY, "system/attributes"
    ).immunities.apply(lambda x: 0 if x is np.nan else len(x))

    test_dataframe["good_weakness"] = get_subcolumn(
        BESTIARY, "system/attributes"
    ).weaknesses.apply(lambda x: get_characteristic_from_list(x, "good"))
    test_dataframe["fire_resistance"] = get_subcolumn(
        BESTIARY, "system/attributes"
    ).resistances.apply(lambda x: get_characteristic_from_list(x, "fire"))
    test_dataframe["fly"] = get_subcolumn(
        BESTIARY, "system/attributes/speed"
    ).otherSpeeds.apply(lambda x: get_characteristic_from_list(x, "fly"))

    test_dataframe["focus"] = test_dataframe["focus"].fillna(0)
    test_dataframe.loc[test_dataframe["level"] > 20, "level"] = 21
    test_dataframe = test_dataframe.reset_index(drop=True)

    bestiary_dataframe = load_and_preprocess_data(
        DATASET_PATHS,
        characteristics=[
            "cha",
            "con",
            "dex",
            "int",
            "str",
            "wis",
            "ac",
            "hp",
            "focus",
            "fortitude",
            "immunities",
            "good_weakness",
            "fire_resistance",
            "fly",
        ],
    )

    pd.testing.assert_frame_equal(
        test_dataframe.sort_index(axis=1),
        bestiary_dataframe.sort_index(axis=1),
        check_dtype=False,
    )
