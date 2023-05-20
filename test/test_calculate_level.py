from training.calculate_level import calculate_level


def test_calculate_level_standardized():
    monster_adult_white_dragon = (
        '{"cha":1, "con":5, "dex":2, "int":1, "str":7, "wis":2, "ac":29, "hp":215}'
    )
    monster_lantern_archon = (
        '{"cha":1, "con":1, "dex":3, "int":-1, "str":-5, "wis":1, "ac":16, "hp":20}'
    )
    monster_treerazer = (
        '{"cha":8, "con":11, "dex":9, "int":7, "str":12, "wis":8, "ac":54, "hp":550}'
    )

    level = calculate_level(monster_json=monster_adult_white_dragon, standardized=True)
    assert level == "10"

    level = calculate_level(monster_json=monster_lantern_archon, standardized=True)
    assert level == "1"

    level = calculate_level(monster_json=monster_treerazer, standardized=True)
    assert level == ">20"


def test_calculate_level_not_standardized():
    level = calculate_level(
        monster_json="example_monsters/monster_adult_white_dragon.json",
        standardized=False,
    )
    assert level == "10"

    level = calculate_level(
        monster_json="example_monsters/monster_lantern_archon.json", standardized=False
    )
    assert level == "1"

    level = calculate_level(
        monster_json="example_monsters/monster_treerazer.json", standardized=False
    )
    assert level == ">20"
