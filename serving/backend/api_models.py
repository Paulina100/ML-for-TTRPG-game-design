from pydantic import BaseModel, Field


class Properties(BaseModel):
    name: str
    strength: int = Field(alias="str")
    dexterity: int = Field(alias="dex")
    constitution: int = Field(alias="con")
    intelligence: int = Field(alias="int")
    wisdom: int = Field(alias="wis")
    charisma: int = Field(alias="cha")
    armor_class: int = Field(alias="ac")
    hit_points: int = Field(alias="hp")


class CounterfactualsInput(BaseModel):
    name: str
    str: int
    dex: int
    con: int
    int: int
    wis: "int"
    cha: "int"
    ac: "int"
    hp: "int"
    level: "int"
