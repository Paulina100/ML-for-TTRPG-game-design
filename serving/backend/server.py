import joblib
import uvicorn
from api_models import CounterfactualsInput, Properties
from calculate_level import calculate_level
from fastapi import FastAPI
from generate_counterfactuals import generate_counterfactuals
from mangum import Mangum
from pandas import read_csv
from starlette.middleware.cors import CORSMiddleware


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


DATASET_PATH = "./counterfactuals_datasets/bestiaries_basic.csv"

df = read_csv(DATASET_PATH)


@app.post("/make_prediction")
async def make_prediction(properties: Properties):
    properties_dict = properties.dict()
    level = calculate_level(monster_stats=properties_dict, model=model)
    result = {"level": str(level) if level <= 20 else ">20"}
    return result


@app.post("/get_counterfactuals")
async def get_counterfactuals(properties: CounterfactualsInput):
    properties_dict = properties.dict(by_alias=True)
    level = properties_dict.pop("level")
    counterfactual_examples = generate_counterfactuals(
        properties_dict, model, level, df
    )
    return counterfactual_examples


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
