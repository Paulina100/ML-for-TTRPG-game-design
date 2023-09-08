import lightgbm as lightgbm
import pandas as pd
import pytest
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import RidgeCV

from training.create_model import create_model, get_fitted_model


@pytest.fixture
def train_set() -> tuple[pd.DataFrame, pd.Series]:
    n = 10
    data = {
        "cha": [10 for _ in range(n)],
        "con": [10 for _ in range(n)],
        "dex": [10 for _ in range(n)],
    }

    X_train = pd.DataFrame(data=data)
    y_train = pd.Series(data=[10 for _ in range(n)])

    return X_train, y_train


def test_create_linear_regression(train_set):
    X_train, y_train = train_set

    model = get_fitted_model("linear_regression", X_train, y_train)

    assert type(model) == RidgeCV


def test_create_random_forest(train_set):
    X_train, y_train = train_set
    model = get_fitted_model("random_forest", X_train, y_train)

    assert type(model.best_estimator_) == RandomForestRegressor


def test_create_lightgbm(train_set):
    X_train, y_train = train_set
    model = get_fitted_model("lightgbm", X_train, y_train)

    assert isinstance(model, lightgbm.Booster)


def test_wrong_classifier_name():
    with pytest.raises(ValueError):
        model = create_model("wrong_classifier_name")
