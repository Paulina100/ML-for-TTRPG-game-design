import pandas as pd
from sklearn.model_selection import train_test_split


DEFAULT_TEST_SIZE: float = 0.25
"""Default value of fraction of the dataset to include in test split."""

PATH_TO_MAPPINGS: str = "../training/books_with_dates.csv"
"""Path to CSV file containing mappings between books and their publishing dates."""


def get_date_books_mapping() -> pd.DataFrame:
    """
    Creates dataframe mapping publishing date to list of corresponding books. Each list of books is
    sorted by their names and dataframe is sorted by the "date" column.\n
    :return: Dataframe containing list of books for each date.
    """
    date_books_mapping = pd.read_csv(PATH_TO_MAPPINGS)
    date_books_mapping = (
        date_books_mapping.groupby("date")["book"].apply(list).reset_index(name="books")
    )
    date_books_mapping["books"] = date_books_mapping.books.sort_values().apply(
        lambda books: sorted(books)
    )
    return date_books_mapping.sort_values(by="date", ignore_index=True)


def get_dataframe_with_oldest_books(
    df: pd.DataFrame, test_size: float = DEFAULT_TEST_SIZE
) -> pd.DataFrame:
    """
    Extracts from dataframe rows with the oldest books. Number of extracted rows is bigger or equal to
    a fraction of initial number of rows defined in test_size. Number of returned rows can be bigger than
    expected to avoid splitting one book into different dataframes.\n
    :param df: Processed dataframe.
    :param test_size: Fraction of the dataset to include in test split. It should be a float number between 0.0 and 1.0.
    :return: Dataframe containing extracted rows.
    """
    books_per_year = get_date_books_mapping()
    filtered_df = pd.DataFrame(columns=df.columns)
    dtypes_dict = df.dtypes.to_dict()
    filtered_df = filtered_df.astype(dtypes_dict)
    remaining_rows_num = int((1 - test_size) * df.shape[0])
    for index, row in books_per_year.iterrows():
        for book_name in row["books"]:
            book_df = df.loc[df["book"] == book_name]
            filtered_df = pd.concat([filtered_df, book_df])
            remaining_rows_num -= book_df.shape[0]
            if remaining_rows_num <= 0:
                return filtered_df
    return filtered_df


def get_chronological_split_results(
    df: pd.DataFrame, test_size: float = DEFAULT_TEST_SIZE
) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """
    Splits dataframe into training and testing sets chronologically, extracting "level" column as label vector.
    :param df: Processed dataframe.
    :param test_size: Fraction of the dataset to include in test split. It should be a float number between 0.0 and 1.0.
    :return: Two feature matrices (X_train, X_test) and two label vectors (y_train, y_test).
    """
    if "book" not in df:
        raise ValueError(
            "No books were found in dataframe - chronological split is not possible."
        )

    X_train = get_dataframe_with_oldest_books(df, test_size)
    X_test = df.drop(X_train.index)
    y_train = X_train.pop("level")
    y_test = X_test.pop("level")

    return X_train, X_test, y_train, y_test


def get_random_split_results(
    df: pd.DataFrame, test_size: float = DEFAULT_TEST_SIZE
) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """
    Splits dataframe into training and testing sets randomly, extracting "level" column as label vector.\n
    :param df: Processed dataframe.
    :param test_size: Fraction of the dataset to include in test split. It should be a float number between 0.0 and 1.0.
    :return: Two feature matrices (X_train, X_test) and two label vectors (y_train, y_test).
    """
    X, y = df.drop("level", axis="columns"), df["level"]
    try:
        return train_test_split(
            X, y, test_size=test_size, random_state=0, shuffle=True, stratify=y
        )
    except ValueError:
        # caused by setting stratify=y if there is a class in y that has only 1 member
        return train_test_split(X, y, test_size=test_size, random_state=0, shuffle=True)


def split_dataframe(
    df: pd.DataFrame,
    test_size: float = DEFAULT_TEST_SIZE,
    chronological_split: bool = True,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """
    Splits dataframe to dataframes allowing training and testing of ML models. Requires "level" column to be
    present in initial dataframe - it is used to split dataframe to feature matrix and label vector.\n
    :param df: Processed dataframe.
    :param test_size: Fraction of the dataset to include in test split. It should be a float number between 0.0 and 1.0.
    :param chronological_split: If True, splits dataframe chronologically so that training set contains rows with
    the oldest books from initial dataframe and testing set contains the newest. Otherwise, the dataframe is
    split randomly.
    :return: Two feature matrices (X_train, X_test) and two label vectors (y_train, y_test).
    """
    if not 0.0 < test_size < 1.0:
        raise ValueError("test_size must be between 0.0 and 1.0.")

    if "level" not in df:
        raise ValueError('Dataframe must contain "level" column.')

    if chronological_split:
        return get_chronological_split_results(df, test_size)

    return get_random_split_results(df, test_size)
