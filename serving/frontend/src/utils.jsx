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
    return  ["Strength (Str)", "Dexterity (Dex)", "Constitution  (Con)", "Intelligence (Int)",
        "Wisdom (Wis)", "Charisma (Cha)", "Armor Class (AC)", "Hit Points (HP)"];
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
