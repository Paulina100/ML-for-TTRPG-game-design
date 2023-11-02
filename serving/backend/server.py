import joblib
import uvicorn
from api_models import Properties
from calculate_level import calculate_level
from fastapi import FastAPI
from mangum import Mangum
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


@app.post("/make_prediction")
async def make_prediction(properties: Properties):
    properties_dict = properties.dict()
    properties_dict.pop("name")
    level = calculate_level(monster_stats=properties_dict, model=model)
    result = {"level": str(level) if level <= 20 else ">20"}
    return result


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
