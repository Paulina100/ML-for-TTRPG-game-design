import joblib
from sklearn.ensemble import RandomForestRegressor
from training.creating_dataset import create_dataframe


def save_model_to_file(model=None, filename: str = "../saved_models/current_model.pkl"):
    if model is None:
        X = create_dataframe()
        X.pop("book")
        y = X.pop("level")

        # Trenuje las losowy (tu będzie funkcja od Joli)
        model = RandomForestRegressor(
            random_state=0, n_jobs=-1, n_estimators=100, max_features=0.5, max_depth=7
        )
        model.fit(X, y)

    joblib.dump(model, filename)


def load_model_from_file(filename: str = "../saved_models/current_model.pkl"):
    return joblib.load(filename)


save_model_to_file()
