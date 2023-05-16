import {renderHeader} from "../utils";

const properties = ["Armor Class (AC)", "Hit Points (HP)", "Strength (Str)", "Dexterity (Dex)",
    "Concentration (Con)", "Intelligence (Int)", "Wisdom (Wis)", "Charisma (Cha)"]


function extractBracketedWord(property) {
    return property.substring(property.indexOf("(") + 1, property.indexOf(")")).toLowerCase();
}

function renderPropertiesFormRow(property) {
    const propertyShort = extractBracketedWord(property);
    return (
        <div id="properties-form-row">
            <label htmlFor={propertyShort} id="properties-form-label">{property}</label>
            <input id={propertyShort} name={propertyShort} type="number" pattern="[0-9]+" required/>
        </div>
    );
}

function handleSubmit(e) {
    e.preventDefault();

    const formData = new FormData(e.target);
    const formJson = Object.fromEntries(formData.entries());

    fetch("http://localhost:8000/properties/upload-form", {
        method: "POST",
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(formJson)
    }).catch(e => {
        alert(e);
    });
}

const PropertiesForm = () => {
    return (
        <div id="properties-form-container">
            {renderHeader("Insert monster's properties")}
            <form method="POST" onSubmit={handleSubmit}>
                {properties.map(value => renderPropertiesFormRow(value))}
                <button type="submit">Submit</button>
            </form>
        </div>
    );
}

export default PropertiesForm;
