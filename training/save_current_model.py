import joblib

from training.create_model import get_fitted_model
from training.creating_dataset import create_dataframe


if __name__ == "__main__":
    X = create_dataframe()
    X.pop("book")
    y = X.pop("level")
    rf = get_fitted_model(classifier_name="random_forest", X_train=X, y_train=y)

    joblib.dump(value=rf, filename="../saved_models/current_model.pkl")
