import joblib
from sklearn.ensemble import RandomForestRegressor
from training.creating_dataset import create_dataframe


def save_default_model_to_file(filename: str = "../output/current_model"):
    X = create_dataframe()
    X.pop("book")
    y = X.pop("level")

    # Trenuje las losowy (tu będzie funkcja od Joli)
    model = RandomForestRegressor(
        random_state=0, n_jobs=-1, n_estimators=100, max_features=0.5, max_depth=7
    )
    model.fit(X, y)

    save_model_to_file(model, filename)


def save_model_to_file(model, filename: str = "../output/current_model"):
    joblib.dump(model, filename + ".pkl")


def load_model_from_file(filename: str):
    return joblib.load(filename)


save_default_model_to_file()
