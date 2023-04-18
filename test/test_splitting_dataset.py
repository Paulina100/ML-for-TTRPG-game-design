import pytest

from training.creating_dataset import create_dataframe
from training.splitting_dataset import (
    _get_book_names_from_dataframe,
    _get_grouped_book_names,
    _get_dataframe_with_oldest_books,
    _get_chronological_split_results,
    _get_random_split_results,
    split_dataframe,
)


# _get_book_names_from_dataframe
def test_get_book_names_from_dataframe():
    dataframe = create_dataframe()
    books = sorted(_get_book_names_from_dataframe(dataframe))
    expected_books = sorted(
        [
            "Pathfinder Bestiary",
            "Pathfinder Bestiary 2",
            "Pathfinder Bestiary 3",
            "Pathfinder Core Rulebook",
        ]
    )
    assert all(x == y for x, y in zip(books, expected_books))

    dataframe.drop(columns="book", axis=1, inplace=True)
    books = _get_book_names_from_dataframe(dataframe)
    assert len(books) == 0


# _get_grouped_book_names
def test_get_grouped_book_names():
    dataframe = create_dataframe()
    grouped_books = _get_grouped_book_names(dataframe)
    expected_grouped_books = {
        2019: ["Pathfinder Bestiary", "Pathfinder Core Rulebook"],
        2020: ["Pathfinder Bestiary 2"],
        2021: ["Pathfinder Bestiary 3"],
    }
    assert grouped_books == expected_grouped_books

    dataframe.at[0, "book"] = "Not Existing Book"
    grouped_books = _get_grouped_book_names(dataframe)
    expected_grouped_books[0] = ["Not Existing Book"]
    assert grouped_books == expected_grouped_books

    dataframe.drop(columns="book", axis=1, inplace=True)
    grouped_books = _get_grouped_book_names(dataframe)
    assert len(grouped_books) == 0


# _get_dataframe_with_oldest_books
def test_get_dataframe_with_oldest_books():
    test_size = 0.5
    dataframe = create_dataframe()
    oldest_books_dataframe = _get_dataframe_with_oldest_books(dataframe, test_size)
    assert oldest_books_dataframe.shape[0] == int((1 - test_size) * dataframe.shape[0])

    books = sorted(oldest_books_dataframe.book.unique())
    expected_books = sorted(
        ["Pathfinder Bestiary", "Pathfinder Core Rulebook", "Pathfinder Bestiary 2"]
    )
    assert all(x == y for x, y in zip(books, expected_books))


# _get_chronological_split_results
def test_get_chronological_split_results():
    test_size = 0.5
    dataframe = create_dataframe()
    X_train, X_test, y_train, y_test = _get_chronological_split_results(
        dataframe, test_size
    )
    assert "level" not in X_train
    assert "level" not in X_test
    assert X_train.shape[0] + X_test.shape[0] == dataframe.shape[0]
    assert y_train.shape[0] + y_test.shape[0] == dataframe.shape[0]

    dataframe.drop(columns="book", axis=1, inplace=True)
    X_train, X_test, y_train, y_test = _get_chronological_split_results(
        dataframe, test_size
    )
    assert "level" not in X_train
    assert "level" not in X_test
    assert X_train.shape[0] + X_test.shape[0] == dataframe.shape[0]
    assert y_train.shape[0] + y_test.shape[0] == dataframe.shape[0]


# _get_random_split_results
def test_get_random_split_results():
    test_size = 0.5
    dataframe = create_dataframe()
    X_train, X_test, y_train, y_test = _get_random_split_results(dataframe, test_size)
    assert "level" not in X_train
    assert "level" not in X_test
    assert X_train.shape[0] + X_test.shape[0] == dataframe.shape[0]
    assert y_train.shape[0] + y_test.shape[0] == dataframe.shape[0]


# split_dataframe
def test_split_dataframe():
    test_size = 1.5
    dataframe = create_dataframe()
    with pytest.raises(ValueError):
        X_train, X_test, y_train, y_test = split_dataframe(dataframe, test_size)

    test_size = 0.5
    dataframe.drop(columns="level", axis=1, inplace=True)
    with pytest.raises(ValueError):
        X_train, X_test, y_train, y_test = split_dataframe(dataframe, test_size)
