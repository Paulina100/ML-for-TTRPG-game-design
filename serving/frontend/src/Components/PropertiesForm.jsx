import {displaySubmitInfo, renderHeader} from "../utils";

const properties = ["Charisma (Cha)", "Concentration (Con)", "Dexterity (Dex)", "Intelligence (Int)",
    "Strength (Str)", "Wisdom (Wis)", "Armor Class (AC)", "Hit Points (HP)"]

function extractBracketedWord(property) {
    return property.substring(property.indexOf("(") + 1, property.indexOf(")")).toLowerCase();
}

function validateInput(event) {
    const allowedKeys = ["Backspace", "Enter", "Tab"];
    if (!/[0-9]/.test(event.key) && !allowedKeys.includes(event.key)) {
        event.preventDefault();
    }
}

function renderPropertiesFormRow(property, monsterProperties, setMonsterProperties) {
    const propertyShort = extractBracketedWord(property);
    return (
        <div className="properties-form-row" key={propertyShort}>
            <label htmlFor={propertyShort} id="properties-form-label">{property}</label>
            <input id={propertyShort} name={propertyShort} type="text" required
                   onKeyDown={(event) => {
                       validateInput(event);
                   }}
                   onChange={(event) => {
                       setMonsterProperties({[propertyShort]: event.target.value});
                   }}
                   value={(monsterProperties === null) ? "" : monsterProperties[propertyShort]}/>
        </div>
    );
}

function renderNameFormRow(monsterProperties, setMonsterProperties) {
    return (
        <div className="properties-form-row">
            <label htmlFor="name" id="properties-form-label">Name</label>
            <input id="name" name="name" type="text" required
                   onChange={(event) => {
                       setMonsterProperties({"name": event.target.value});
                   }}
                   value={(monsterProperties === null) ? "" : monsterProperties["name"]}/>
        </div>
    );
}

const PropertiesForm = (monsterProperties, setMonsterProperties) => {
    function handleSubmit(e) {
        e.preventDefault();

        const formData = new FormData(e.target);
        const formJson = Object.fromEntries(formData.entries());
        setMonsterProperties(formJson);

        fetch("http://localhost:8000/properties/upload", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(formJson)
        }).then(() => {
            displaySubmitInfo("properties-submit-button", "properties-form");
        }).catch(e => {
            alert(e);
        });
    }

    return (
        <div id="properties-form-container">
            {renderHeader("Insert monster's properties")}
            <form onSubmit={handleSubmit} id="properties-form">
                {renderNameFormRow(monsterProperties, setMonsterProperties)}
                {properties.map(value => renderPropertiesFormRow(value, monsterProperties, setMonsterProperties))}
                <button type="submit" id="properties-submit-button">Submit</button>
            </form>
        </div>
    );
}

export default PropertiesForm;
