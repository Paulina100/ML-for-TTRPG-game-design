from fastapi import FastAPI
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


@app.post("/properties/upload")
async def upload_properties(props: dict[str, str]):
    properties["name"] = props.pop("name")
    for k, v in props.items():
        properties[k] = int(v)
