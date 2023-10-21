import joblib
from api_models import Properties
from calculate_level import calculate_level
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from serving.backend.constants import ORDERED_CHARACTERISTICS


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = joblib.load(filename="../../saved_models/current_model.pkl")


@app.post("/make_prediction")
async def make_prediction(properties: Properties):
    properties_dict = properties.dict()
    stats = {p: properties_dict[p] for p in ORDERED_CHARACTERISTICS}
    level = calculate_level(monster_stats=stats, model=model)
    result = {"level": str(level) if level <= 20 else ">20"}
    return result
