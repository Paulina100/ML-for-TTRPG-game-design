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
    perception: int
    fortitude: int
    reflex: int
    will: int
    focus: int
    num_immunities: int
    land_speed: int
    fly: int
    climb: int
    swim: int
    spells_nr_lvl_1: int
    spells_nr_lvl_2: int
    spells_nr_lvl_3: int
    spells_nr_lvl_4: int
    spells_nr_lvl_5: int
    spells_nr_lvl_6: int
    spells_nr_lvl_7: int
    spells_nr_lvl_8: int
    spells_nr_lvl_9: int
    melee_max_bonus: int
    avg_melee_dmg: int
    ranged_max_bonus: int
    avg_ranged_dmg: int
    acid_resistance: int
    all_damage_resistance: int
    bludgeoning_resistance: int
    cold_resistance: int
    electricity_resistance: int
    fire_resistance: int
    mental_resistance: int
    physical_resistance: int
    piercing_resistance: int
    poison_resistance: int
    slashing_resistance: int
    area_damage_weakness: int
    cold_weakness: int
    cold_iron_weakness: int
    evil_weakness: int
    fire_weakness: int
    good_weakness: int
    slashing_weakness: int
    splash_damage_weakness: int


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
