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
        if (damage === null || damage === "" || damage === "varies by") {
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
    return avgDamage.toString();
}

export function getExtractionMethods() {
    return new Map([
        ["str", (monsterDict) => {return monsterDict.system?.abilities?.str?.mod}],
        ["dex", (monsterDict) => {return monsterDict.system?.abilities?.dex?.mod}],
        ["con", (monsterDict) => {return monsterDict.system?.abilities?.con?.mod}],
        ["int", (monsterDict) => {return monsterDict.system?.abilities?.int?.mod}],
        ["wis", (monsterDict) => {return monsterDict.system?.abilities?.wis?.mod}],
        ["cha", (monsterDict) => {return monsterDict.system?.abilities?.cha?.mod}],
        ["ac", (monsterDict) => {return monsterDict.system?.attributes?.ac?.value}],
        ["hp", (monsterDict) => {return monsterDict.system?.attributes?.hp?.value}],
        ["perception", (monsterDict) => {return monsterDict.system?.attributes?.perception?.value}],
        ["fortitude", (monsterDict) => {return monsterDict.system?.saves?.fortitude?.value}],
        ["reflex", (monsterDict) => {return monsterDict.system?.saves?.reflex?.value}],
        ["will", (monsterDict) => {return monsterDict.system?.saves?.will?.value}],
        ["focus", (monsterDict) => {return monsterDict.system?.resources?.focus?.value}],
        ["num_immunities", (monsterDict) => {
            const immunities = monsterDict.system?.attributes?.immunities;
            return immunities === undefined ? 0 : immunities.length;}],
        ["land_speed", (monsterDict) => {return monsterDict.system?.attributes?.speed?.value}],
        ["fly", (monsterDict) => {return getSelectedTypeValue(monsterDict.system?.attributes?.speed?.otherSpeeds, "fly")}],
        ["climb", (monsterDict) => {return getSelectedTypeValue(monsterDict.system?.attributes?.speed?.otherSpeeds, "climb")}],
        ["swim", (monsterDict) => {return getSelectedTypeValue(monsterDict.system?.attributes?.speed?.otherSpeeds, "swim")}],
        ["spells_nr_lvl_1", (monsterDict) => {return getSpellsNumberWithLevel(monsterDict.items, 1)}],
        ["spells_nr_lvl_2", (monsterDict) => {return getSpellsNumberWithLevel(monsterDict.items, 2)}],
        ["spells_nr_lvl_3", (monsterDict) => {return getSpellsNumberWithLevel(monsterDict.items, 3)}],
        ["spells_nr_lvl_4", (monsterDict) => {return getSpellsNumberWithLevel(monsterDict.items, 4)}],
        ["spells_nr_lvl_5", (monsterDict) => {return getSpellsNumberWithLevel(monsterDict.items, 5)}],
        ["spells_nr_lvl_6", (monsterDict) => {return getSpellsNumberWithLevel(monsterDict.items, 6)}],
        ["spells_nr_lvl_7", (monsterDict) => {return getSpellsNumberWithLevel(monsterDict.items, 7)}],
        ["spells_nr_lvl_8", (monsterDict) => {return getSpellsNumberWithLevel(monsterDict.items, 8)}],
        ["spells_nr_lvl_9", (monsterDict) => {return getSpellsNumberWithLevel(monsterDict.items, 9)}],
        ["melee_max_bonus", (monsterDict) => {return getMaxBonus(monsterDict.items, "melee")}],
        ["avg_melee_dmg", (monsterDict) => {return getAvgDamage(monsterDict.items, "melee")}],
        ["ranged_max_bonus", (monsterDict) => {return getMaxBonus(monsterDict.items, "ranged")}],
        ["avg_ranged_dmg", (monsterDict) => {return getAvgDamage(monsterDict.items, "ranged")}],
        ["acid_resistance", (monsterDict) => {
            return getSelectedTypeValue(monsterDict.system?.attributes?.resistances, "acid")}],
        ["all_damage_resistance", (monsterDict) => {
            return getSelectedTypeValue(monsterDict.system?.attributes?.resistances, "all-damage")}],
        ["bludgeoning_resistance", (monsterDict) => {
            return getSelectedTypeValue(monsterDict.system?.attributes?.resistances, "bludgeoning")}],
        ["cold_resistance", (monsterDict) => {
            return getSelectedTypeValue(monsterDict.system?.attributes?.resistances, "cold")}],
        ["electricity_resistance", (monsterDict) => {
            return getSelectedTypeValue(monsterDict.system?.attributes?.resistances, "electricity")}],
        ["fire_resistance", (monsterDict) => {
            return getSelectedTypeValue(monsterDict.system?.attributes?.resistances, "fire")}],
        ["mental_resistance", (monsterDict) => {
            return getSelectedTypeValue(monsterDict.system?.attributes?.resistances, "mental")}],
        ["physical_resistance", (monsterDict) => {
            return getSelectedTypeValue(monsterDict.system?.attributes?.resistances, "physical")}],
        ["piercing_resistance", (monsterDict) => {
            return getSelectedTypeValue(monsterDict.system?.attributes?.resistances, "piercing")}],
        ["poison_resistance", (monsterDict) => {
            return getSelectedTypeValue(monsterDict.system?.attributes?.resistances, "poison")}],
        ["slashing_resistance", (monsterDict) => {
            return getSelectedTypeValue(monsterDict.system?.attributes?.resistances, "slashing")}],
        ["area_damage_weakness", (monsterDict) => {
            return getSelectedTypeValue(monsterDict.system?.attributes?.weaknesses, "area-damage")}],
        ["cold_weakness", (monsterDict) => {
            return getSelectedTypeValue(monsterDict.system?.attributes?.weaknesses, "cold")}],
        ["cold_iron_weakness", (monsterDict) => {
            return getSelectedTypeValue(monsterDict.system?.attributes?.weaknesses, "cold-iron")}],
        ["evil_weakness", (monsterDict) => {
            return getSelectedTypeValue(monsterDict.system?.attributes?.weaknesses, "evil")}],
        ["fire_weakness", (monsterDict) => {
            return getSelectedTypeValue(monsterDict.system?.attributes?.weaknesses, "fire")}],
        ["good_weakness", (monsterDict) => {
            return getSelectedTypeValue(monsterDict.system?.attributes?.weaknesses, "good")}],
        ["slashing_weakness", (monsterDict) => {
            return getSelectedTypeValue(monsterDict.system?.attributes?.weaknesses, "slashing")}],
        ["splash_damage_weakness", (monsterDict) => {
            return getSelectedTypeValue(monsterDict.system?.attributes?.weaknesses, "splash-damage")}]
    ]);
}

export function generateMonsterJSON(monsterName, monsterValues) {
    function generateImmunities(numImmunities) {
        if (numImmunities === 0) {
            return {};
        }
        let immunities = [];
        for (let i=0; i<numImmunities; i++) {
            immunities.push({"type": ""})
        }
        return {"immunities": immunities};
    }

    function generateSpeeds() {
        const value = parseInt(monsterValues[14]);
        const fly = parseInt(monsterValues[15]);
        const climb = parseInt(monsterValues[16]);
        const swim = parseInt(monsterValues[17]);

        if (value === 0  && fly === 0 && climb === 0 && swim === 0) {
            return {};
        }

        const speedDict = {"speed": {"value": value, "otherSpeeds": []}}
        if (fly !== 0) {
            speedDict.speed.otherSpeeds.push({"type": "fly", "value": fly})
        }
        if (climb !== 0) {
            speedDict.speed.otherSpeeds.push({"type": "climb", "value": climb})
        }
        if (swim !== 0) {
            speedDict.speed.otherSpeeds.push({"type": "swim", "value": swim})
        }
        return speedDict;
    }

    function generateResistances() {
        const resistanceTypes = ["acid", "all-damage", "bludgeoning", "cold", "electricity", "fire", "mental",
            "physical", "piercing", "poison", "slashing"];
        const resistances = [];
        for (let i=0; i<resistanceTypes.length; i++) {
            let resistanceValue = parseInt(monsterValues[31 + i]);
            if (resistanceValue !== 0) {
                resistances.push({"type": resistanceTypes[i], "value": resistanceValue});
            }
        }
        if (resistances.length > 0) {
            return {"resistances": resistances};
        }
        return {};
    }

    function generateWeaknesses() {
        const weaknessTypes = ["area-damage", "cold", "cold-iron", "evil", "fire", "good",
            "slashing", "splash-damage"];
        const weaknesses = [];
        for (let i=0; i<weaknessTypes.length; i++) {
            let weaknessValue = parseInt(monsterValues[42 + i]);
            if (weaknessValue !== 0) {
                weaknesses.push({"type": weaknessTypes[i], "value": weaknessValue});
            }
        }
        if (weaknesses.length > 0) {
            return {"weaknesses": weaknesses};
        }
        return {};
    }

    function generateSpells(spellsLevel, spellsNumber) {
        let spells = [];
        for (let i=0; i<spellsNumber; i++) {
            spells.push({
                "type": "spell",
                "system": {
                    "category": {"value": "spell"},
                    "traits": {"value": []},
                    "level": {"value": spellsLevel}
                }})
        }
        return spells;
    }

    function calculateAttackDamage(avgAttackValue) {
        if (avgAttackValue === 0 || isNaN(avgAttackValue)) {
            return "";
        }
        if (avgAttackValue % 1 === 0.5) {
            return avgAttackValue > 4.5 ?
                `1d8+${avgAttackValue - 4.5}` :
                avgAttackValue === 4.5 ?
                    "1d8":
                    `1d8-${4.5 - avgAttackValue}`;
        }
        return avgAttackValue > 9 ?
            `2d8+${avgAttackValue - 9}` :
            avgAttackValue === 9 ?
                "2d8" :
                `2d8-${9 - avgAttackValue}`;

    }

    function generateAttacks(weaponType) {
        let bonusValue, damage;
        if (weaponType === "melee") {
            bonusValue = parseInt(monsterValues[27]);
            damage = parseFloat(monsterValues[28]);
        } else {  // "ranged"
            bonusValue = parseInt(monsterValues[29]);
            damage = parseFloat(monsterValues[30]);
        }

        if (bonusValue === 0) {
            return [];
        }
        return [{
            "type": "melee", "system": {
                "weaponType": {"value": weaponType},
                "bonus": {"value": parseInt(bonusValue)},
                "damageRolls": {"id": {"damage": calculateAttackDamage(parseFloat(damage)), "damageType": ""}}
            }
        }];
    }

    return {
        "name": monsterName,
        "system": {
            "abilities": {
                "str": {"mod": parseInt(monsterValues[0])},  // required
                "dex": {"mod": parseInt(monsterValues[1])},  // required
                "con": {"mod": parseInt(monsterValues[2])},  // required
                "int": {"mod": parseInt(monsterValues[3])},  // required
                "wis": {"mod": parseInt(monsterValues[4])},  // required
                "cha": {"mod": parseInt(monsterValues[5])}  // required
            },
            "attributes": {
                "ac": {"value": parseInt(monsterValues[6])},  // required
                "hp": {"value": parseInt(monsterValues[7])},  // required
                "perception": {"value": parseInt(monsterValues[8])},  // required
                ...generateImmunities(parseInt(monsterValues[13])),
                ...generateSpeeds(),
                ...generateResistances(),
                ...generateWeaknesses()
            },
            "saves": {
                "fortitude": {"value": parseInt(monsterValues[9])},  // required
                "reflex": {"value": parseInt(monsterValues[10])},  // required
                "will": {"value": parseInt(monsterValues[11])}  // required
            },
            "resources": {
                "focus": {"value": parseInt(monsterValues[12])}
            }
        },
        "items": [
            ...generateSpells(1, parseInt(monsterValues[18])),
            ...generateSpells(2, parseInt(monsterValues[19])),
            ...generateSpells(3, parseInt(monsterValues[20])),
            ...generateSpells(4, parseInt(monsterValues[21])),
            ...generateSpells(5, parseInt(monsterValues[22])),
            ...generateSpells(6, parseInt(monsterValues[23])),
            ...generateSpells(7, parseInt(monsterValues[24])),
            ...generateSpells(8, parseInt(monsterValues[25])),
            ...generateSpells(9, parseInt(monsterValues[26])),
            ...generateAttacks("melee"),
            ...generateAttacks("ranged")
        ]
    };
}
