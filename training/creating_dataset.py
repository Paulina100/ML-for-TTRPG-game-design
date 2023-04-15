import os.path
import traceback
from copy import deepcopy
from typing import List

import pandas as pd

from training.analysis_functions import (
    get_merged_bestiaries,
    unpack_column,
    DataFrameType,
)


def create_dataframe(
    books: List[str] = [
        "../pathfinder_2e_data/pathfinder-bestiary.db",
        "../pathfinder_2e_data/pathfinder-bestiary-2.db",
        "../pathfinder_2e_data/pathfinder-bestiary-3.db",
    ],
    characteristics: List[str] = [
        "system/abilities",
        "system/attributes/ac",
        "system/attributes/hp",
    ],
) -> DataFrameType:
    """
    Creates dataframe containing chosen characteristics, level (CR) and source book of monsters from chosen books
    :param books: list of paths of books to load
    :param characteristics: list of characteristics to load
    :return: DataFrame with monsters (NPC) form chosen books and with chosen characteristics and their origin book
    """
    loading_methods = {
        "system/abilities": move_values_level_up(value_name="mod"),
        "system/attributes/ac": load_subcolumn_as_value("ac"),
        "system/attributes/hp": load_subcolumn_as_value("hp"),
    }
    for i in range(len(books) - 1, -1, -1):
        if not is_path_correct(books[i]):
            books.pop(i)

    bestiary = get_merged_bestiaries(books)
    bestiary = bestiary[bestiary["type"] == "npc"]
    df = _create_df_with_basic_values(bestiary)

    for characteristic in characteristics:
        if (loading_method := loading_methods.get(characteristic)) is not None:
            part = loading_method(get_subcolumn(bestiary, characteristic))
            df = pd.concat(
                [
                    df,
                    part,
                ],
                axis=1,
            )

    return df


def is_path_correct(path: str) -> bool:
    """
    Throws exception if file does not exist or has a wrong extension
    :param path: path to book to load
    :return: True if path is correct otherwise False
    """
    if not os.path.isfile(path):
        print(f"Path {path} does not exist")
        return False
    if not (path.endswith(".db") or path.endswith(".json")):
        print(f"Expected db or json file, got {path}")
        return False
    return True


def move_values_level_up(value_name: str):
    """
    Assigns values of chosen key in columns' dictionaries to that columns
    :param value_name: name of value that should be moved one level up as value of current column/columns
    :return: function which create DataFrame with values of current column(s) changed to value of chosen sub column
    """

    def inner_move_values_level_up(df: DataFrameType):
        return df.applymap(lambda x: x.get(value_name), na_action="ignore")

    return inner_move_values_level_up


def get_subcolumn(book: DataFrameType, subcolumn_path: str) -> DataFrameType:
    """
    Gets subcolumn of given DataFrame according to given path
    :param book: DataFrame with all data from book(s)
    :param subcolumn_path: path to subcolumn
    :return: chosen sub column as DataFrame
    """
    subcol = deepcopy(book)
    for col in subcolumn_path.split("/"):
        subcol = pd.DataFrame(data=unpack_column(subcol, col))

    return subcol


def load_subcolumn_as_value(original_column_name: str, value_name: str = "value"):
    """
    Returned function creates DataFrame with chosen value_name of given DataFrame and changes column name to chosen one
    :param original_column_name: name that should be given to result dataframe column
    :param value_name: name of sub column which value will be returned
    :return: function to create Dataframe with chosen column name and values from a chosen sub column of current column
    """

    def subcolumn_as_value(df: DataFrameType):
        result_df = pd.DataFrame(data=df[value_name])
        result_df.columns = [original_column_name]
        return result_df

    return subcolumn_as_value


def _create_df_with_basic_values(df: DataFrameType) -> DataFrameType:
    """
    Creates Dataframes which are obligatory for every dataset
    :param df: DataFrame with all information about monsters
    :return: DataFrame with two obligatory values from df
    """
    lvl = load_subcolumn_as_value("level")(get_subcolumn(df, "system/details/level"))
    book = load_subcolumn_as_value("book")(get_subcolumn(df, "system/details/source"))

    return pd.concat([lvl, book], axis=1)
