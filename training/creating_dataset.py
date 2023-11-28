import json
import os.path
from dataclasses import dataclass

import numpy as np
import pandas as pd


OTHER_SPEEDS = {
    "fly",
    "swim",
    "climb",
}
"""set of other speeds that can be added to dataset"""
OTHER_SPEED_PATH = "system.attributes.speed.otherSpeeds"
"""path to other speeds that are in OTHER_SPEEDS in original json_normalize bestiaries"""

RESISTANCES = {
    "fire_resistance",
    "cold_resistance",
    "electricity_resistance",
    "acid_resistance",
    "piercing_resistance",
    "slashing_resistance",
    "physical_resistance",
    "bludgeoning_resistance",
    "mental_resistance",
    "poison_resistance",
    "all-damage_resistance",
}
"""set of resistances that can be added to dataset"""
RESISTANCE_PATH = "system.attributes.resistances"
"""path to resistances that are in RESISTANCES in original json_normalize bestiaries"""

WEAKNESSES = {
    "cold-iron_weakness",
    "good_weakness",
    "fire_weakness",
    "cold_weakness",
    "area-damage_weakness",
    "splash-damage_weakness",
    "evil_weakness",
    "slashing_weakness",
}
"""set of weaknesses that can be added to dataset"""
WEAKNESSES_PATH = "system.attributes.weaknesses"
"""path to weaknesses that are in WEAKNESSES in original json_normalize bestiaries"""

SPECIAL_CHARACTERISTICS = {
    "melee",
    "ranged",
    "spells",
}
"""set of characteristics with specific way of extracting information"""

CHARACTERISTICS_RENAME = {
    "con": "system.abilities.con.mod",
    "dex": "system.abilities.dex.mod",
    "cha": "system.abilities.cha.mod",
    "int": "system.abilities.int.mod",
    "str": "system.abilities.str.mod",
    "wis": "system.abilities.wis.mod",
    "ac": "system.attributes.ac.value",
    "hp": "system.attributes.hp.value",
    "perception": "system.attributes.perception.value",
    "fortitude": "system.saves.fortitude.value",
    "reflex": "system.saves.reflex.value",
    "will": "system.saves.will.value",
    "focus": "system.resources.focus.value",
    "level": "system.details.level.value",
    "book": "system.details.source.value",
    "land_speed": "system.attributes.speed.value",
    "num_immunities": "system.attributes.immunities",
}
"""dictionary with characteristics names (keys) and "path" to real columns in dataframe loaded from file (values)"""


@dataclass
class CharacteristicsGroups:
    speeds: set[str]
    weaknesses: set[str]
    resistances: set[str]
    special_characteristics: set[str]
    characteristics_rename: set[str]


def is_path_correct(path: str) -> bool:
    """
    Checks whether given path is correct: file exists and correct file extension - json or db

    :param path: path to book to load
    :return: True if path is correct
    """
    if not os.path.isfile(path):
        raise ValueError(f"Path {path} does not exist")

    if not (path.endswith(".db") or path.endswith(".json")):
        raise ValueError(f"Expected db or json file, got {path}")

    return True


def split_characteristics_into_groups(
    characteristics: set[str],
) -> CharacteristicsGroups:
    """
    Split given characteristics list into five categories according to sets and dictionaries with characteristics.
    Categories depend on way of extracting data.

    :param characteristics: list of characteristics
    :return: sets and list of characteristics after split
    """
    speeds = OTHER_SPEEDS & characteristics
    weaknesses = WEAKNESSES & characteristics
    resistances = RESISTANCES & characteristics
    special_characteristics = SPECIAL_CHARACTERISTICS & characteristics
    characteristics_rename = characteristics & CHARACTERISTICS_RENAME.keys()

    return CharacteristicsGroups(
        speeds=speeds,
        weaknesses=weaknesses,
        resistances=resistances,
        special_characteristics=special_characteristics,
        characteristics_rename=characteristics_rename,
    )


def get_characteristic_from_list(cell_value, characteristic_name: str) -> int:
    """
    Function used for pd.Series.apply()\n
    Retrieve the value associated with a specific characteristic from a list of dictionaries.

    :param cell_value: Value of cell from df. A list of dictionaries, where each dictionary represents a characteristic
            with 'type' and 'value' keys.
    :param characteristic_name: The characteristic name to search for.
    :return: The value associated with the specified characteristic if found, or 0 if not found.
    """
    if not cell_value or cell_value is np.nan:
        return 0

    for dictionary in cell_value:
        if dictionary["type"] == characteristic_name:
            return dictionary["value"]

    # required characteristic was not found
    return 0


def extract_and_assign_chars(
    char_group: set,
    path_to_char: str,
    bestiary: pd.DataFrame,
    df: pd.DataFrame,
    replace_val: str,
):
    """
    Extract and assign values for a group of characteristics from `bestiary` DataFrame to another `df` DataFrame.

    :param char_group: A set of characteristic names to extract and assign.
    :param path_to_char: The path to the column containing the characteristic values in the `bestiary` DataFrame.
    :param bestiary: The DataFrame containing data from which to extract characteristic values.
    :param df: The DataFrame to which the extracted values will be assigned.
    :param replace_val:  A string to replace in characteristic names to determine the target column names in `df`.
    """
    # there are books where all monsters don't have weaknesses
    if path_to_char not in bestiary.columns:
        for char in char_group:
            df[char] = pd.Series(0, index=bestiary.index)
        return

    for char in char_group:
        characteristic_name = char.replace(replace_val, "")
        get_value = lambda x: get_characteristic_from_list(x, characteristic_name)
        df[char] = bestiary[path_to_char].apply(get_value)


def get_nr_of_spells_with_lvl(items_list: list[dict], spell_level: int) -> int:
    """
    Function used for pd.Series.apply()\n
    Count the number of spells in the given list that match the specified level.

    :param items_list: A list of dictionaries representing items, each with relevant attributes.
    :param spell_level: The level to filter spells by.
    :return: The count of spells in the list that match the specified level.
    """
    # get only spell items
    spells = [
        i
        for i in items_list
        if i["type"] == "spell" and i["system"]["category"]["value"] == "spell"
        # skip cantrip spells
        and "cantrip" not in i["system"]["traits"]["value"]
        and i["system"]["level"]["value"] == spell_level
    ]

    return len(spells)


def count_damage_expected_value(damage_dict: dict[dict]) -> float:
    """
    Calculate the total expected value of damage based on a dictionary of damage specifications.

    :param damage_dict: A dictionary where keys represent different sources of damage,
                        and values are dictionaries with the "damage" key containing damage specifications.
                        Damage can be a constant value or a dice roll in the format 'NdM', 'NdM+X', or 'NdM-X',
                        where N is the number of dice, M is the number of sides on the dice, and X is an optional
                        positive or negative constant.
    :return: The calculated total expected value of damage.
    """
    total_expected_val = 0

    # chance that one melee item have multiple damage types
    for key, value in damage_dict.items():
        damage = value["damage"]

        if not damage or damage == "varies by":
            return 0

        if "d" not in damage:
            # constant damage value
            total_expected_val += int(damage)
            continue
        # split dice roll
        roll_nr, dice_type = damage.split("d")
        add = 0
        if "+" in dice_type:
            # get possible positive additional value for damage
            dice_type, all_additional_values = dice_type.split("+", 1)
            # there are monsters with damage like: 3d10+12+2
            all_additional_values = all_additional_values.split("+")
            add = 0
            for add_value in all_additional_values:
                add += int(add_value)
        if "-" in dice_type:
            # get possible negative additional value for damage
            dice_type, add = dice_type.split("-")
            add = -int(add)

        roll_nr, dice_type = int(roll_nr), int(dice_type)
        # count expected value with additional damages
        total_expected_val += roll_nr * (dice_type + 1) / 2 + add

    return total_expected_val


def get_max_melee_bonus_damage(
    items_list: list[dict], weapon_type: str
) -> tuple[int, float]:
    """
    Function used for pd.Series.apply()\n
    Get the maximum damageRoll bonus and associated damage from a list of melee of a specific weaponType.

    :param items_list: A list of dictionaries representing melee weapons, each with relevant attributes.
    :param weapon_type: The type of weapon to filter by.
    :return: A tuple containing the maximum bonus and the calculated damage associated with that bonus.
             If no matching melee weapons are found, returns (0, 0).
    """
    melee = [
        i["system"]
        for i in items_list
        if i["type"] == "melee" and i["system"]["weaponType"]["value"] == weapon_type
    ]

    if not melee:
        return 0, 0

    idx_val = [(val["bonus"]["value"], idx) for idx, val in enumerate(melee)]
    # find melee with the highest bonus: bonus and idx
    max_bonus, max_bonus_idx = max(idx_val)
    # get damage information about max_bonus melee
    best_bonus_melee_damage = melee[max_bonus_idx]["damageRolls"]
    # get expected value of chosen melee
    damage_expected_value = count_damage_expected_value(best_bonus_melee_damage)
    return max_bonus, damage_expected_value


def load_data(paths_to_books: list[str]) -> pd.DataFrame:
    """
    Load and normalize monsters' data from a list of book paths.

    :param paths_to_books: A list of file paths to books containing monsters (NPCs) data in JSON format.
    :return: A pandas DataFrame containing information about monsters extracted from the specified books.
    """
    data = []

    for path in paths_to_books:
        is_path_correct(path)
        with open(path) as file:
            # loading json strings from files
            data += [json.loads(line) for line in file]
            file.close()

    bestiary = pd.json_normalize(data)
    # only npc monsters
    bestiary = bestiary[bestiary["type"] == "npc"]

    return bestiary


def preprocess_data(bestiary: pd.DataFrame, characteristics: list[str]) -> pd.DataFrame:
    """
    Creates dataframe containing chosen characteristics, level and source book of monsters from given bestiary.

    :param bestiary: A pandas DataFrame containing information about monsters.
    :param characteristics: A list of characteristics to load.
    :return: DataFrame with monsters from chosen books and with chosen characteristics and their origin book.
    """
    pd.options.mode.chained_assignment = None
    # silent warning (SettingWithCopyWarning) about view and copy
    # we don't need to go back to the original df - no matter if it is a view

    characteristics_groups = split_characteristics_into_groups(set(characteristics))

    if "num_immunities" in characteristics_groups.characteristics_rename:
        immunities_path = CHARACTERISTICS_RENAME.get("num_immunities")
        # There are books where all monsters don't have immunities
        if immunities_path not in bestiary.columns:
            bestiary[immunities_path] = pd.Series(0, index=bestiary.index)
        else:
            count_immunities = lambda x: 0 if x is np.nan else len(x)
            bestiary[immunities_path] = bestiary[immunities_path].apply(
                count_immunities
            )

    # There are books where all monsters don't have focus value
    if "focus" in characteristics_groups.characteristics_rename:
        if CHARACTERISTICS_RENAME.get("focus") not in bestiary.columns:
            bestiary[CHARACTERISTICS_RENAME.get("focus")] = pd.Series(
                0, index=bestiary.index
            )

    COLS_TO_EXTRACT = pd.DataFrame(
        data=[
            (characteristic, CHARACTERISTICS_RENAME.get(characteristic))
            for characteristic in characteristics_groups.characteristics_rename.union(
                {"book", "level"}
            )
        ],
        columns=["target_name", "raw_name"],
    )

    raw_names = COLS_TO_EXTRACT["raw_name"]
    target_names = COLS_TO_EXTRACT["target_name"]

    # to not have Series names as a part of final df
    target_names.name = None

    df = bestiary[raw_names]
    df.columns = target_names

    if "hp" in characteristics_groups.characteristics_rename:
        df["hp"] = df["hp"].astype(int)

    extract_and_assign_chars(
        characteristics_groups.resistances, RESISTANCE_PATH, bestiary, df, "_resistance"
    )

    extract_and_assign_chars(
        characteristics_groups.weaknesses, WEAKNESSES_PATH, bestiary, df, "_weakness"
    )

    extract_and_assign_chars(
        characteristics_groups.speeds, OTHER_SPEED_PATH, bestiary, df, ""
    )

    if "spells" in characteristics_groups.special_characteristics:
        MAX_SPELL_LVL = 9
        for i in range(1, MAX_SPELL_LVL + 1):
            df[f"spells_nr_lvl_{i}"] = bestiary["items"].apply(
                lambda x: get_nr_of_spells_with_lvl(x, i)
            )

    if "melee" in characteristics_groups.special_characteristics:
        df["melee_max_bonus"], df["avg_melee_dmg"] = zip(
            *bestiary["items"].apply(lambda x: get_max_melee_bonus_damage(x, "melee"))
        )

    if "ranged" in characteristics_groups.special_characteristics:
        df["ranged_max_bonus"], df["avg_ranged_dmg"] = zip(
            *bestiary["items"].apply(lambda x: get_max_melee_bonus_damage(x, "ranged"))
        )

    if "focus" in df.columns:
        df["focus"] = df["focus"].fillna(0)
        df["focus"] = df["focus"].astype(int)

    if "land_speed" in df.columns:
        df["land_speed"] = df["land_speed"].fillna(0)

    df.loc[df["level"] > 20, "level"] = 21

    pd.reset_option("mode.chained_assignment")

    return df


def load_and_preprocess_data(
    paths_to_books: list[str],
    characteristics: list[str],
) -> pd.DataFrame:
    """
    Creates dataframe containing chosen characteristics, level and source book of monsters from chosen books

    :param paths_to_books: A list of file paths to books containing monster data in JSON format.
    :param characteristics: A list of characteristics to load.
    :return: DataFrame with monsters (NPC) from chosen books and with chosen characteristics and their origin book
    """

    bestiary = load_data(paths_to_books)

    return preprocess_data(bestiary, characteristics)
