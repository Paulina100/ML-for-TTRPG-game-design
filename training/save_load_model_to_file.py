import joblib
from sklearn.ensemble import RandomForestRegressor
from training.creating_dataset import create_dataframe


def save_latest_version_of_model_to_file(filename: str = "./output/current_model"):
    # Mam moje dane standardowe
    X = create_dataframe()
    y = X.drop("level")

    # Trenuje las losowy (tu będzie funkcja od Joli)
    model = RandomForestRegressor(
        random_state=0, n_jobs=-1, n_estimators=100, max_features=0.5, max_depth=7
    )

    model.fit(X, y)

    save_model_to_file(model, filename)


def save_model_to_file(model, filename: str = "./output/current_model"):
    # Save the model to a file
    joblib.dump(model, filename + ".pkl")


def load_model_from_file(filename: str):
    # Load the saved model from the file
    return joblib.load(filename)


save_latest_version_of_model_to_file()
