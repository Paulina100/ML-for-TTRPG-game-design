import os.path
import traceback
from copy import deepcopy
from typing import List

import pandas as pd

from training.analysis_functions import (
    import_merged_bestiaries,
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

    :param books: list of paths of books to load
    :param characteristics: list of characteristics to load
    :return: DataFrame with monsters(nps) form chosen books and with chosen characteristics and their origin book
    """
    loading_methods = {
        "system/abilities": move_values_level_up(value_name="mod"),
        "system/attributes/ac": load_sub_column_as_value("ac"),
        "system/attributes/hp": load_sub_column_as_value("hp"),
    }
    try:
        check_paths(books)
    except:
        traceback.print_exc()

    bestiary = import_merged_bestiaries(books)
    bestiary = bestiary[bestiary["type"] == "npc"]
    df = create_df_with_basic_values(bestiary)

    for characteristic in characteristics:
        if (loading_method := loading_methods.get(characteristic)) is not None:
            part = loading_method(get_sub_column(bestiary, characteristic))
            df = pd.concat(
                [
                    df,
                    part,
                ],
                axis=1,
            )

    return df


def check_paths(paths: List[str]) -> None:
    """
    Throws exception if file does not exist or has a wrong extension
    :param paths: list of paths to books to load
    :return:
    """
    for path in paths:
        if not os.path.isfile(path):
            raise Exception(f"Path {path} does not exist")
        if not (path.endswith(".db") or path.endswith(".json")):
            raise Exception(f"Expected db or json file, got {path}")


def move_values_level_up(value_name: str):
    """
    :param value_name: name of value that should be moved one level up as value of current column/columns
    :return: function which create DataFrame with values of current column(s) changed to value of chosen sub column
    """

    def level_up_result(df: DataFrameType):
        return df.applymap(lambda x: x.get(value_name), na_action="ignore").reset_index(
            drop=True
        )

    return level_up_result


def get_sub_column(book: DataFrameType, sub_column_path: str) -> DataFrameType:
    """

    :param book: DataFrame with all data from book(s)
    :param sub_column_path: path to get to sub column
    :return: chosen sub column as DataFrame
    """
    sub_col = deepcopy(book)
    for col in sub_column_path.split("/"):
        sub_col = pd.DataFrame(data=unpack_column(sub_col, col)).reset_index(drop=True)

    return sub_col


def load_sub_column_as_value(column_name: str, value_name: str = "value"):
    """

    :param column_name: name that should be given to result dataframe column
    :param value_name: name of sub column which value will be returned
    :return: function to create Dataframe with chosen column name and values from a chosen sub column of current column
    """

    def sub_column_as_value(df: DataFrameType):
        result_df = pd.DataFrame(data=df[value_name])
        result_df.columns = [column_name]
        return result_df.reset_index(drop=True)

    return sub_column_as_value


def create_df_with_basic_values(df: DataFrameType) -> DataFrameType:
    """

    :param df: DataFrame with all information about monsters
    :return: DataFrame with two obligatory values from df
    """
    lvl = load_sub_column_as_value("level")(get_sub_column(df, "system/details/level"))
    book = load_sub_column_as_value("book")(get_sub_column(df, "system/details/source"))

    return pd.concat([lvl, book], axis=1)
