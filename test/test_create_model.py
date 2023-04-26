from training.creating_dataset import create_dataframe
from training.create_model import create_model
from training.splitting_dataset import get_random_split_results
from sklearn.linear_model import RidgeCV
from sklearn.ensemble import RandomForestRegressor


def test_linear_regression():
    dataset = create_dataframe()
    X_train, X_test, y_train, y_test = get_random_split_results(dataset)
    X_train = X_train.drop(columns=["book"])
    model = create_model("train_linear_regression", X_train, y_train)

    assert type(model) == RidgeCV


def test_random_forest():
    dataset = create_dataframe()
    X_train, X_test, y_train, y_test = get_random_split_results(dataset)
    X_train = X_train.drop(columns=["book"])
    model = create_model("train_random_forest", X_train, y_train)

    assert type(model.best_estimator_) == RandomForestRegressor


def test_wrong_classifier_name():
    dataset = create_dataframe()
    X_train, X_test, y_train, y_test = get_random_split_results(dataset)
    X_train = X_train.drop(columns=["book"])
    model = create_model("train_wrong_classifier_name", X_train, y_train)

    assert model is None
