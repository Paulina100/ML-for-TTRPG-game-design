from typing import Union

import pandas as pd
import numpy as np
import pandas.core.frame
import pandas.core.series


def import_merged_bestiaries(books: list[str]) -> pandas.core.frame.DataFrame:
    """
    Returns merged books

    Parameters
    ----------
    books (list[str]): list of paths to books

    Returns
    -------
    out : (pandas.core.frame.DataFrame)
    """
    b = [pd.read_json(book, lines=True) for book in books]
    return pd.concat(b, join="outer", axis=0).fillna(np.nan)


def unpack_column(
    df: pandas.core.frame.DataFrame, column_name: str, print_info: bool = False
) -> Union[pandas.core.frame.DataFrame, None]:
    # sth wrong with Series
    """
    Unpacks dict and changes it to DataFrame

    :param print_info:
        print or not: first row and Len of that row
        default: False
    :param df: DataFrame
        with column with dict
    :param column_name: name of the colum with dict
    :return:
        DataFrame with values from chosen column
    """
    new_df = df[column_name].apply(pd.Series)
    if print_info:
        print("First row:")
        print(new_df.iloc[0])
        print(f"Len = {len(new_df.iloc[0])}")
    return new_df


def remove_redundant_level(
    df: pandas.core.frame.DataFrame, columns: list[str], value: str
) -> pandas.core.frame.DataFrame:
    # TODO
    # find why it doesn't work
    """
    Modifies dataframe and returns it.
    For every row of df and column from columns changes value of cell to value of dictionary that is in that cell to
     remove redundant level in df.

    :param df: dataframe
    :param columns: list of columns to modify
    :param value: value we are looking for in dict in cell
    :return: df with changed cells
    """
    for col in columns:
        for i, row in df.iterrows():
            row[col] = row[col].get(value)
    return df
