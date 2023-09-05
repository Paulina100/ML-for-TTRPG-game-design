from pydantic import BaseModel


class Properties(BaseModel):
    name: str
    str: int
    dex: int
    con: int
    wis: int
    cha: int
    ac: int
    hp: int
    int: int
