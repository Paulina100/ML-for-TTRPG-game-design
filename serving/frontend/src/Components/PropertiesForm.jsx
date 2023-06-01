import {renderHeader} from "../utils";

const properties = ["Armor Class (AC)", "Hit Points (HP)", "Strength (Str)", "Dexterity (Dex)",
    "Concentration (Con)", "Intelligence (Int)", "Wisdom (Wis)", "Charisma (Cha)"]


function extractBracketedWord(property) {
    return property.substring(property.indexOf("(") + 1, property.indexOf(")")).toLowerCase();
}

function validateInput(event) {
    const allowedKeys = ["Backspace", "Enter", "Tab"];
    if (!/[0-9]/.test(event.key) && !allowedKeys.includes(event.key)) {
        event.preventDefault();
    }
}

function renderPropertiesFormRow(property, monsterProperties) {
    const propertyShort = extractBracketedWord(property);
    return (
        <div id="properties-form-row">
            <label htmlFor={propertyShort} id="properties-form-label">{property}</label>
            <input id={propertyShort} name={propertyShort} type="text" required
                onKeyDown={(event) => { validateInput(event); }}
                defaultValue={(monsterProperties === null) ? "" :  monsterProperties[propertyShort]} />
        </div>
    );
}

function renderNameFormRow(monsterProperties) {
    return (
        <div id="properties-form-row">
            <label htmlFor="name" id="properties-form-label">Name</label>
            <input id="name" name="name" type="text" required
                value={(monsterProperties === null) ? "" :  monsterProperties["name"]} />
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
            const submitButton = document.getElementById("submit-button");
            submitButton.setAttribute("style", "display:none");

            let form = document.getElementById("properties-form");
            const submittedMessage = document.createElement("p");
            submittedMessage.setAttribute("class", "message");
            submittedMessage.appendChild(document.createTextNode("Submit successful"));
            form.appendChild(submittedMessage);

            setTimeout(() => {
                form.removeChild(submittedMessage);
                submitButton.setAttribute("style", "display:block");
            }, 1250);
        }).catch(e => {
            alert(e);
        });
    }

    return (
        <div id="properties-form-container">
            {renderHeader("Insert monster's properties")}
            <form method="POST" onSubmit={handleSubmit} id="properties-form">
                {renderNameFormRow(monsterProperties)}
                {properties.map(value => renderPropertiesFormRow(value, monsterProperties))}
                <button type="submit" id="submit-button">Submit</button>
            </form>
        </div>
    );
}

export default PropertiesForm;
