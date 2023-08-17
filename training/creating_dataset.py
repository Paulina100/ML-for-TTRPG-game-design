import json
import os.path

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
    "immunities": "system.attributes.immunities",
}
"""dictionary with characteristics names (keys) and "path" to real columns in dataframe loaded from file (values)"""


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
    characteristics: list,
) -> tuple[set[str], set[str], set[str], set[str], list[str]]:
    """
    Split given characteristics list into five categories according to sets and dictionaries with characteristics.
    Categories depend on way of extracting data.
    :param characteristics: list of characteristics
    :return: sets and list of characteristics after split
    """
    speeds = OTHER_SPEEDS.intersection(characteristics)
    weaknesses = WEAKNESSES.intersection(characteristics)
    resistances = RESISTANCES.intersection(characteristics)
    special_characteristics = SPECIAL_CHARACTERISTICS.intersection(characteristics)
    characteristics_rename = [
        ch for ch in characteristics if ch in CHARACTERISTICS_RENAME.keys()
    ]

    return (
        speeds,
        weaknesses,
        resistances,
        special_characteristics,
        characteristics_rename,
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
    if not cell_value or np.all(pd.isnull(cell_value)):
        return 0

    result = [
        x.get("value") for x in cell_value if x.get("type") == characteristic_name
    ]
    return 0 if len(result) == 0 else result[0]


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
        if i.get("type") == "spell"
        and i.get("system").get("category").get("value") == "spell"
        # skip cantrip spells
        and "cantrip" not in i.get("system").get("traits").get("value")
        and i.get("system").get("level").get("value") == spell_level
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
        damage = value.get("damage")

        if "d" not in damage:
            # constant damage value
            total_expected_val += int(damage)
            continue
        # split dice roll
        roll_nr, dice_type = damage.split("d")
        add = 0
        if "+" in dice_type:
            # get possible positive additional value for damage
            dice_type, add = dice_type.split("+")
            add = int(add)
        if "-" in dice_type:
            # get possible negative additional value for damage
            dice_type, add = dice_type.split("-")
            add = -int(add)

        roll_nr, dice_type = int(roll_nr), int(dice_type)
        # count expected value with additional damages
        total_expected_val += roll_nr * (dice_type + 1) / 2 + add

    return total_expected_val


def get_max_melee_bonus_damage(
    items_list: list[dict], weaponType: str
) -> tuple[int, float]:
    """
    Function used for pd.Series.apply()\n
    Get the maximum damageRoll bonus and associated damage from a list of melee of a specific weaponType.
    :param items_list: A list of dictionaries representing melee weapons, each with relevant attributes.
    :param weaponType: The type of weapon to filter by.
    :return: A tuple containing the maximum bonus and the calculated damage associated with that bonus.
             If no matching melee weapons are found, returns (0, 0).
    """
    melee = [
        i.get("system")
        for i in items_list
        if i.get("type") == "melee"
        and i.get("system").get("weaponType").get("value") == weaponType
    ]

    if not melee:
        return 0, 0

    max_bonus_indx, max_bonus = max(
        [(inx, val.get("bonus").get("value")) for inx, val in enumerate(melee)],
        key=lambda x: x[1],
    )

    return max_bonus, count_damage_expected_value(
        melee[max_bonus_indx].get("damageRolls")
    )


def load_and_preprocess_data(
    paths_to_books: list[str],
    characteristics: list[str],
) -> pd.DataFrame:
    """
    Creates dataframe containing chosen characteristics, level and source book of monsters from chosen books

    :param paths_to_books: list of paths of books to load
    :param characteristics: list of characteristics to load
    :return: DataFrame with monsters (NPC) from chosen books and with chosen characteristics and their origin book
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
    # only system column (all characteristics are there)
    # bestiary = bestiary.filter(regex="system", axis="columns")
    (
        speeds,
        weaknesses,
        resistances,
        special_characteristics,
        characteristics_rename,
    ) = split_characteristics_into_groups(characteristics)

    if "immunities" in characteristics_rename:
        with pd.option_context("mode.chained_assignment", None):
            immunities_path = CHARACTERISTICS_RENAME.get("immunities")
            bestiary[immunities_path] = bestiary[immunities_path].apply(
                lambda x: 0 if np.all(pd.isnull(x)) else len(x)
            )

    COLS_TO_EXTRACT = pd.DataFrame(
        data=[
            (characteristic, CHARACTERISTICS_RENAME.get(characteristic))
            for characteristic in characteristics_rename + ["book", "level"]
        ],
        columns=["target_name", "raw_name"],
    )

    raw_names = COLS_TO_EXTRACT["raw_name"]
    target_names = COLS_TO_EXTRACT["target_name"]

    # to not have Series names as a part of final df
    target_names.name = None

    df = bestiary[raw_names]
    df.columns = target_names

    for resistance in resistances:
        with pd.option_context("mode.chained_assignment", None):
            # silent warning (SettingWithCopyWarning) about view and copy
            # we don't need to go back to the original df - no matter if it is a view
            df[resistance] = bestiary[RESISTANCE_PATH].apply(
                lambda x: get_characteristic_from_list(
                    cell_value=x,
                    characteristic_name=resistance.replace("_resistance", ""),
                )
            )

    for weakness in weaknesses:
        with pd.option_context("mode.chained_assignment", None):
            df[weakness] = bestiary[WEAKNESSES_PATH].apply(
                lambda x: get_characteristic_from_list(
                    cell_value=x, characteristic_name=weakness.replace("_weakness", "")
                )
            )

    for speed in speeds:
        with pd.option_context("mode.chained_assignment", None):
            df[speed] = bestiary[OTHER_SPEED_PATH].apply(
                lambda x: get_characteristic_from_list(x, speed)
            )

    if "spells" in special_characteristics:
        MAX_SPELL_LVL = 9
        with pd.option_context("mode.chained_assignment", None):
            for i in range(1, MAX_SPELL_LVL + 1):
                df[f"spells_nr_lvl_{i}"] = bestiary["items"].apply(
                    lambda X: get_nr_of_spells_with_lvl(X, i)
                )

    if "melee" in special_characteristics:
        with pd.option_context("mode.chained_assignment", None):
            df["melee_max_bonus"], df["melee_damage_exp_val"] = zip(
                *bestiary["items"].apply(
                    lambda x: get_max_melee_bonus_damage(x, "melee")
                )
            )

    if "melee" in special_characteristics:
        with pd.option_context("mode.chained_assignment", None):
            df["ranged_max_bonus"], df["ranged_damage_exp_val"] = zip(
                *bestiary["items"].apply(
                    lambda x: get_max_melee_bonus_damage(x, "ranged")
                )
            )

    if "focus" in df.columns:
        with pd.option_context("mode.chained_assignment", None):
            df["focus"] = df["focus"].fillna(0)
            df["focus"] = df["focus"].astype(int)

    if "land_speed" in df.columns:
        with pd.option_context("mode.chained_assignment", None):
            df["land_speed"] = df["land_speed"].fillna(0)

    df.loc[df["level"] > 20, "level"] = 21

    return df
