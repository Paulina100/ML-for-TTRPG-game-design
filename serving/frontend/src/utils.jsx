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

export function getGroupedSystemProperties() {
    return new Map([
        ["abilities", ["str", "dex", "con", "int", "wis", "cha"]],  // mod
        ["attributes", ["ac", "hp"]]  // value
    ]);
}

export function getPropertiesValuesKeys() {
    return new Map([
        ["abilities", "mod"],
        ["attributes", "value"]
    ]);
}
