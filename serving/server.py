import json

from fastapi import FastAPI, UploadFile, File
from starlette.middleware.cors import CORSMiddleware


app = FastAPI()

origins = ["http://localhost:3000", "localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

properties = {}


@app.get("/", tags=["root"])
async def read_root() -> dict:
    return {}


@app.get("/properties")
async def get_properties() -> dict:
    return properties


@app.post("/properties/upload-file")
async def upload_file(file: UploadFile = File(...)):
    file_content = await file.read()
    file_dict = json.loads(file_content)
    system_dict = file_dict["system"]
    properties_attributes = ["ac", "hp"]
    properties_abilities = ["str", "dex", "con", "int", "wis", "cha"]
    for p in properties_attributes:
        properties[p] = system_dict["attributes"][p]["value"]
    for p in properties_abilities:
        properties[p] = system_dict["abilities"][p]["mod"]


@app.post("/properties/upload-form")
async def upload_properties(props: dict[str, str]):
    for k, v in props.items():
        properties[k] = int(v)
