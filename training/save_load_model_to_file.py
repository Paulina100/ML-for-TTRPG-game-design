import joblib

from training.create_model import get_fitted_model
from training.creating_dataset import create_dataframe


def save_model_to_file(model=None, filename: str = "../saved_models/current_model.pkl"):
    """
    Saves a machine learning model to a file
    :param model: machine learning model to be saved. If None, default model will be created and trained
    :param filename: path and filename to save the model to
    """

    if model is None:
        X = create_dataframe()
        X.pop("book")
        y = X.pop("level")

        model = get_fitted_model(classifier_name="random_forest", X_train=X, y_train=y)

    joblib.dump(model, filename)


def load_model_from_file(filename: str = "../saved_models/current_model.pkl"):
    """
    Loads a machine learning model from a file
    :param filename: path and filename of the model file to load
    :return: loaded machine learning model
    """
    return joblib.load(filename)
