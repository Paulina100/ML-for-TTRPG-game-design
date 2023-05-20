from numpy.testing import assert_array_equal

from training.create_model import get_fitted_model
from training.creating_dataset import create_dataframe
from training.save_load_model_to_file import load_model_from_file, save_model_to_file


def test_save_load_model_to_file_default():
    X = create_dataframe()
    X.pop("book")
    y = X.pop("level")
    rf = get_fitted_model(classifier_name="random_forest", X_train=X, y_train=y)

    save_model_to_file(filename="../test/tmp_models/model.pkl")
    loaded_model = load_model_from_file(filename="../test/tmp_models/model.pkl")

    assert loaded_model.best_params_ == rf.best_params_


def test_save_load_model_to_file():
    X = create_dataframe()
    X.pop("book")
    y = X.pop("level")
    regression = get_fitted_model(
        classifier_name="linear_regression", X_train=X, y_train=y
    )

    save_model_to_file(model=regression, filename="../test/tmp_models/model.pkl")
    loaded_model = load_model_from_file(filename="../test/tmp_models/model.pkl")

    assert_array_equal(loaded_model.coef_, regression.coef_)
    assert_array_equal(loaded_model.intercept_, regression.intercept_)
