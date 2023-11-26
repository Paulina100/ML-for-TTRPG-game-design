from pydantic import BaseModel, Field


class Properties(BaseModel):
    strength: int = Field(alias="str")
    dexterity: int = Field(alias="dex")
    constitution: int = Field(alias="con")
    intelligence: int = Field(alias="int")
    wisdom: int = Field(alias="wis")
    charisma: int = Field(alias="cha")
    armor_class: int = Field(alias="ac")
    hit_points: int = Field(alias="hp")


class CounterfactualsInput(BaseModel):
    strength: int = Field(alias="str")
    dexterity: int = Field(alias="dex")
    constitution: int = Field(alias="con")
    intelligence: int = Field(alias="int")
    wisdom: int = Field(alias="wis")
    charisma: int = Field(alias="cha")
    armor_class: int = Field(alias="ac")
    hit_points: int = Field(alias="hp")
    level: int
