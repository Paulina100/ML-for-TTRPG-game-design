from typing import Union, List, TypeVar

import pandas as pd
import numpy as np
import pandas.core.frame
import pandas.core.series

DataFrameType = TypeVar("pandas.core.frame.DataFrame")


def import_merged_bestiaries(books: List[str]) -> DataFrameType:
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
    return pd.concat(b, join="outer", axis=0).fillna(np.nan).reset_index(drop=True)


def unpack_column(
    df: DataFrameType, column_name: str, print_info: bool = False
) -> Union[DataFrameType, None]:
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
