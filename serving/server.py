import copy

import joblib
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
properties = {}


@app.get("/", tags=["root"])
async def read_root() -> dict:
    return {}


@app.get("/properties")
async def get_properties() -> dict:
    return properties


@app.post("/properties/upload")
async def upload_properties(props: dict[str, str]):
    properties["name"] = props.pop("name")
    for k, v in props.items():
        properties[k] = int(v)


@app.get("/level")
async def get_level():
    if properties:
        properties_without_name = copy.copy(properties)
        properties_without_name.pop("name")
        level = calculate_level(monster_stats=properties_without_name, model=model)
        return {"level": str(level) if level <= 20 else ">20"}
    return {}
