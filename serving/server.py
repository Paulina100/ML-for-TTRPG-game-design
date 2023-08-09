from typing import Optional

import joblib
from api_models import Properties
from backend.calculate_level import calculate_level
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = joblib.load(filename="../saved_models/current_model.pkl")
properties: Optional[Properties] = None


@app.get("/", tags=["root"])
async def read_root() -> dict:
    return {}


@app.get("/properties")
async def get_properties() -> dict:
    return properties.dict() if properties else {}


@app.post("/properties/upload")
async def upload_properties(props: Properties):
    global properties
    properties = props


@app.get("/level")
async def get_level():
    if properties:
        ordered_properties = ["cha", "con", "dex", "int", "str", "wis", "ac", "hp"]
        properties_dict = properties.dict()
        stats = {p: properties_dict[p] for p in ordered_properties}
        level = calculate_level(monster_stats=stats, model=model)
        result = {"level": str(level) if level <= 20 else ">20"}
        return result
    return {}