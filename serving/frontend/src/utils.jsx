export function renderHeader(headerText) {
    return (
        <h1 className={"content-header"}>
            {headerText}
        </h1>
    );
}

export function renderSubheader(subheaderText) {
    return (
        <h2 className={"subheader"}>
            {subheaderText}
        </h2>
    );
}

export function displaySubmitInfo(submitButtonId, formId) {
    const submitButton = document.getElementById(submitButtonId);
    submitButton.setAttribute("style", "display: none");

    let form = document.getElementById(formId);
    const submittedMessage = document.createElement("p");
    submittedMessage.setAttribute("class", "message");
    submittedMessage.appendChild(document.createTextNode("Submit successful"));
    form.appendChild(submittedMessage);

    setTimeout(() => {
        form.removeChild(submittedMessage);
        submitButton.setAttribute("style", "display: block");
    }, 1250);
}

export function getDisplayablePropertiesNames() {
    return [["Strength (Str)", "Dexterity (Dex)", "Constitution  (Con)", "Intelligence (Int)",
        "Wisdom (Wis)", "Charisma (Cha)", "Armor Class (AC)", "Hit Points (HP)",
        "Perception", "Fortitude", "Reflex", "Will"],
        ["Focus", "Number of Immunities", ["Speed", ["Land", "Fly", "Climb", "Swim"]],
            ["Spells", ["Level 1", "Level 2", "Level 3", "Level 4", "Level 5", "Level 6", "Level 7",
                "Level 8", "Level 9"]],
            ["Attacks", ["Melee Max Bonus", "Average Melee Damage", "Ranged Max Bonus", "Average Ranged Damage"]]],
        [["Resistance", ["Acid", "All Damage", "Bludgeoning", "Cold", "Electricity", "Fire", "Mental", "Physical",
            "Piercing", "Poison", "Slashing"]],
            ["Weakness", ["Area Damage", "Cold", "Cold Iron", "Evil", "Fire", "Good", "Slashing", "Splash Damage"]]]];
}

export function getActualPropertiesNames() {
    return [["str", "dex", "con", "int", "wis", "cha", "ac", "hp", "perception", "fortitude", "reflex", "will"],
        ["focus", "num_immunities", ["land_speed", "fly", "climb", "swim"],
            ["spells_nr_lvl_1", "spells_nr_lvl_2", "spells_nr_lvl_3", "spells_nr_lvl_4", "spells_nr_lvl_5",
                "spells_nr_lvl_6", "spells_nr_lvl_7", "spells_nr_lvl_8", "spells_nr_lvl_9"],
            ["melee_max_bonus", "avg_melee_dmg", "ranged_max_bonus", "avg_ranged_dmg"]],
        [["acid_resistance", "all_damage_resistance", "bludgeoning_resistance", "cold_resistance",
            "electricity_resistance", "fire_resistance", "mental_resistance", "physical_resistance",
            "piercing_resistance", "poison_resistance", "slashing_resistance"],
            ["area_damage_weakness", "cold_weakness", "cold_iron_weakness", "evil_weakness", "fire_weakness",
                "good_weakness", "slashing_weakness", "splash_damage_weakness"]]];
}

function getSelectedTypeValue(typeValueList, selectedType) {
    if (typeValueList !== undefined) {
        const filteredList = typeValueList.filter((item) => {return item.type === selectedType})
        if (filteredList.length > 0) {
            return filteredList[0].value;
        }
    }
    return 0;
}

function getSpellsNumberWithLevel(items_list, level) {
    let cnt = 0;
    if (items_list !== undefined) {
        for (let item of items_list) {
            if (item.type === "spell" &&
                item.system.category.value === "spell" &&
                item.system.traits.value.indexOf("cantrip") === -1 &&
                item.system.level.value === level) {
                cnt++;
            }
        }
    }
    return cnt;
}

function getMaxBonus(itemsList, weaponType) {
    if (itemsList === undefined) {
        return 0;
    }
    const melee = [];
    for (let item of itemsList) {
        if (item.type === "melee" && item.system.weaponType.value === weaponType) {
            melee.push(item.system);
        }
    }
    if (melee.length === 0) {
        return 0;
    }
    let maxBonus = melee[0].bonus.value;
    for (let i=1; i<melee.length; i++) {
        let meleeBonus = melee[i].bonus.value;
        if (meleeBonus > maxBonus) {
            maxBonus = meleeBonus;
        }
    }
    return maxBonus;
}

function getAvgDamage(itemsList, weaponType) {
    if (itemsList === undefined) {
        return 0;
    }
    const melee = [];
    for (let item of itemsList) {
        if (item.type === "melee" && item.system.weaponType.value === weaponType) {
            melee.push(item.system);
        }
    }
    if (melee.length === 0) {
        return 0;
    }
    let maxBonus = melee[0].bonus.value;
    let maxBonusIndex = 0;
    for (let i=1; i<melee.length; i++) {
        let meleeBonus = melee[i].bonus.value;
        if (meleeBonus > maxBonus) {
            maxBonus = meleeBonus;
            maxBonusIndex = i;
        }
    }
    const maxBonusDamage = melee[maxBonusIndex].damageRolls;
    let avgDamage = 0;
    for (let damageDict of Object.values(maxBonusDamage)) {
        let damage = damageDict.damage;
        if (damage === null || damage === "varies by") {
            avgDamage = 0;
            break;
        }
        if (damage.indexOf("d") === -1) {
            avgDamage += parseInt(damage);
            continue;
        }
        let splitDamage = damage.split("d");
        let diceType = splitDamage[1];
        let diceResult = 0;
        if (diceType.indexOf("+") !== -1) {
            let splitDiceType = diceType.split("+");
            diceType = splitDiceType[0];
            for (let i=1; i<splitDiceType.length; i++) {
                diceResult += parseInt(splitDiceType[i]);
            }
        }
        if (diceType.indexOf("-") !== -1) {
            let splitDiceType = diceType.split("-");
            diceType = splitDiceType[0];
            diceResult = -parseInt(splitDiceType[1]);
        }
        avgDamage += parseInt(splitDamage[0]) * (parseInt(diceType) + 1) / 2 + diceResult;
    }
    return avgDamage;
}

export function getExtractionMethods() {
    return new Map([
        ["str", (monster_dict) => {return monster_dict.system?.abilities?.str?.mod}],
        ["dex", (monster_dict) => {return monster_dict.system?.abilities?.dex?.mod}],
        ["con", (monster_dict) => {return monster_dict.system?.abilities?.con?.mod}],
        ["int", (monster_dict) => {return monster_dict.system?.abilities?.int?.mod}],
        ["wis", (monster_dict) => {return monster_dict.system?.abilities?.wis?.mod}],
        ["cha", (monster_dict) => {return monster_dict.system?.abilities?.cha?.mod}],
        ["ac", (monster_dict) => {return monster_dict.system?.attributes?.ac?.value}],
        ["hp", (monster_dict) => {return monster_dict.system?.attributes?.hp?.value}],
        ["perception", (monster_dict) => {return monster_dict.system?.attributes?.perception?.value}],
        ["fortitude", (monster_dict) => {return monster_dict.system?.saves?.fortitude?.value}],
        ["reflex", (monster_dict) => {return monster_dict.system?.saves?.reflex?.value}],
        ["will", (monster_dict) => {return monster_dict.system?.saves?.will?.value}],
        ["focus", (monster_dict) => {return monster_dict.system?.resources?.focus?.value}],
        ["num_immunities", (monster_dict) => {
            const immunities = monster_dict.system?.attributes?.immunities;
            return immunities === undefined ? 0 : immunities.length;}],
        ["land_speed", (monster_dict) => {return monster_dict.system?.attributes?.speed?.value}],
        ["fly", (monster_dict) => {return getSelectedTypeValue(monster_dict.system?.attributes?.speed?.otherSpeeds, "fly")}],
        ["climb", (monster_dict) => {return getSelectedTypeValue(monster_dict.system?.attributes?.speed?.otherSpeeds, "climb")}],
        ["swim", (monster_dict) => {return getSelectedTypeValue(monster_dict.system?.attributes?.speed?.otherSpeeds, "swim")}],
        ["spells_nr_lvl_1", (monster_dict) => {return getSpellsNumberWithLevel(monster_dict.items, 1)}],
        ["spells_nr_lvl_2", (monster_dict) => {return getSpellsNumberWithLevel(monster_dict.items, 2)}],
        ["spells_nr_lvl_3", (monster_dict) => {return getSpellsNumberWithLevel(monster_dict.items, 3)}],
        ["spells_nr_lvl_4", (monster_dict) => {return getSpellsNumberWithLevel(monster_dict.items, 4)}],
        ["spells_nr_lvl_5", (monster_dict) => {return getSpellsNumberWithLevel(monster_dict.items, 5)}],
        ["spells_nr_lvl_6", (monster_dict) => {return getSpellsNumberWithLevel(monster_dict.items, 6)}],
        ["spells_nr_lvl_7", (monster_dict) => {return getSpellsNumberWithLevel(monster_dict.items, 7)}],
        ["spells_nr_lvl_8", (monster_dict) => {return getSpellsNumberWithLevel(monster_dict.items, 8)}],
        ["spells_nr_lvl_9", (monster_dict) => {return getSpellsNumberWithLevel(monster_dict.items, 9)}],
        ["melee_max_bonus", (monster_dict) => {return getMaxBonus(monster_dict.items, "melee")}],
        ["avg_melee_dmg", (monster_dict) => {return getAvgDamage(monster_dict.items, "melee")}],
        ["ranged_max_bonus", (monster_dict) => {return getMaxBonus(monster_dict.items, "ranged")}],
        ["avg_ranged_dmg", (monster_dict) => {return getAvgDamage(monster_dict.items, "ranged")}],
        ["acid_resistance", (monster_dict) => {
            return getSelectedTypeValue(monster_dict.system?.attributes?.resistances, "acid")}],
        ["all_damage_resistance", (monster_dict) => {
            return getSelectedTypeValue(monster_dict.system?.attributes?.resistances, "all-damage")}],
        ["bludgeoning_resistance", (monster_dict) => {
            return getSelectedTypeValue(monster_dict.system?.attributes?.resistances, "bludgeoning")}],
        ["cold_resistance", (monster_dict) => {
            return getSelectedTypeValue(monster_dict.system?.attributes?.resistances, "cold")}],
        ["electricity_resistance", (monster_dict) => {
            return getSelectedTypeValue(monster_dict.system?.attributes?.resistances, "electricity")}],
        ["fire_resistance", (monster_dict) => {
            return getSelectedTypeValue(monster_dict.system?.attributes?.resistances, "fire")}],
        ["mental_resistance", (monster_dict) => {
            return getSelectedTypeValue(monster_dict.system?.attributes?.resistances, "mental")}],
        ["physical_resistance", (monster_dict) => {
            return getSelectedTypeValue(monster_dict.system?.attributes?.resistances, "physical")}],
        ["piercing_resistance", (monster_dict) => {
            return getSelectedTypeValue(monster_dict.system?.attributes?.resistances, "piercing")}],
        ["poison_resistance", (monster_dict) => {
            return getSelectedTypeValue(monster_dict.system?.attributes?.resistances, "poison")}],
        ["slashing_resistance", (monster_dict) => {
            return getSelectedTypeValue(monster_dict.system?.attributes?.resistances, "slashing")}],
        ["area_damage_weakness", (monster_dict) => {
            return getSelectedTypeValue(monster_dict.system?.attributes?.weaknesses, "area-damage")}],
        ["cold_weakness", (monster_dict) => {
            return getSelectedTypeValue(monster_dict.system?.attributes?.weaknesses, "cold")}],
        ["cold_iron_weakness", (monster_dict) => {
            return getSelectedTypeValue(monster_dict.system?.attributes?.weaknesses, "cold-iron")}],
        ["evil_weakness", (monster_dict) => {
            return getSelectedTypeValue(monster_dict.system?.attributes?.weaknesses, "evil")}],
        ["fire_weakness", (monster_dict) => {
            return getSelectedTypeValue(monster_dict.system?.attributes?.weaknesses, "fire")}],
        ["good_weakness", (monster_dict) => {
            return getSelectedTypeValue(monster_dict.system?.attributes?.weaknesses, "good")}],
        ["slashing_weakness", (monster_dict) => {
            return getSelectedTypeValue(monster_dict.system?.attributes?.weaknesses, "slashing")}],
        ["splash_damage_weakness", (monster_dict) => {
            return getSelectedTypeValue(monster_dict.system?.attributes?.weaknesses, "splash-damage")}]
    ]);
}
