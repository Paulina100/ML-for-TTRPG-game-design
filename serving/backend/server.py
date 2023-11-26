from multiprocessing import Manager, Process

import joblib
import uvicorn
from api_models import CounterfactualsInput, Properties
from calculate_level import calculate_level
from constants import ORDERED_CHARACTERISTICS
from fastapi import FastAPI
from generate_counterfactuals import TOTAL_CF, generate_counterfactuals
from mangum import Mangum
from starlette.middleware.cors import CORSMiddleware

from training.creating_dataset import load_and_preprocess_data


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
handler = Mangum(app)

model = joblib.load(filename="./saved_models/current_model.pkl")


DATASETS_DIR = "pathfinder_2e_data"
DATASET_FILES = [
    "pathfinder-bestiary.db",
    "pathfinder-bestiary-2.db",
    "pathfinder-bestiary-3.db",
]
DATASET_PATHS = [f"{DATASETS_DIR}/{file}" for file in DATASET_FILES]

df = load_and_preprocess_data(
    DATASET_PATHS,
    characteristics=ORDERED_CHARACTERISTICS,
)


@app.post("/make_prediction")
async def make_prediction(properties: Properties):
    properties_dict = properties.dict()
    level = calculate_level(monster_stats=properties_dict, model=model)
    result = {"level": str(level) if level <= 20 else ">20"}
    return result


def generate_counterfactuals_in_process(stats, level, counterfactual_values):
    counterfactual_examples = generate_counterfactuals(stats, model, level, df)
    for i, v in enumerate(counterfactual_examples["values"]):
        counterfactual_values[i] = v


@app.post("/get_counterfactuals")
async def get_counterfactuals(properties: CounterfactualsInput):
    properties_dict = properties.dict(by_alias=True)
    level = properties_dict.pop("level")
    with Manager() as manager:
        counterfactual_values = manager.list(range(TOTAL_CF))
        process = Process(
            target=generate_counterfactuals_in_process,
            args=(properties_dict, level, counterfactual_values),
        )
        process.start()
        process.join(30)  # timeout is set to 30s
        if process.is_alive():  # process will be terminated because of timeout
            process.terminate()
            process.join()
            result = {}
        else:  # counterfactual examples have been generated
            result = {"values": list(counterfactual_values)}
        return result


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
