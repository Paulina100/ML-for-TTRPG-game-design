from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import RandomizedSearchCV

from training.creating_dataset import create_dataframe
import numpy as np


def calculate_level(monster_json: str) -> str:

    # Ten trening powinien być zapisany do pliku i będziemy go używać do predyckji
    # Mam moje dane standardowe
    X = create_dataframe()
    y = X.drop("level")

    # Trenuje las losowy (tu będzie funkcja od Joli)
    rf = RandomForestRegressor(
        random_state=0, n_jobs=-1, n_estimators=100, max_features=0.5, max_depth=7
    )

    rf.fit(X, y)

    # Save the model to a file
    # joblib.dump(rf_model, 'random_forest_model.pkl')

    # # Load the saved model from the file
    # loaded_model = joblib.load('random_forest_model.pkl')

    # Z potwora musimy wyciągnąć takie same cechy jakie mamy w X
    monster_X = create_dataframe(books="monster")

    predict = rf.predict(monster_X)
    predict = np.where(
        (predict % 1) > 0.33, np.ceil(predict), np.floor(predict)
    ).astype("int")

    if predict == 21:
        return ">20"
    return predict
