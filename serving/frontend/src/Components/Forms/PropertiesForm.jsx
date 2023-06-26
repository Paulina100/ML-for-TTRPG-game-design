import {displaySubmitInfo, renderHeader} from "../../utils";

const PropertiesForm = (monsterProperties, setMonsterProperties) => {
    const properties = ["Charisma (Cha)", "Constitution  (Con)", "Dexterity (Dex)", "Intelligence (Int)",
        "Strength (Str)", "Wisdom (Wis)", "Armor Class (AC)", "Hit Points (HP)"]

    const extractBracketedWord = (property) => {
        return property.substring(property.indexOf("(") + 1, property.indexOf(")")).toLowerCase();
    }

    const validateInput = (event) => {
        const allowedKeys = ["Backspace", "Enter", "Tab", "ArrowLeft", "ArrowRight", "ArrowTop", "ArrowDown"];
        if (!/[0-9]/.test(event.key) && !allowedKeys.includes(event.key)) {
            event.preventDefault();
        }
    }

    const renderPropertiesFormRow = (property) => {
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

    const renderNameFormRow = () => {
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

    const handleSubmit = (event) => {
        event.preventDefault();
        const formData = new FormData(event.target);
        const formJson = Object.fromEntries(formData.entries());
        setMonsterProperties(formJson);

        fetch("http://localhost:8000/properties/upload", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(formJson)
        }).then(() => {
            displaySubmitInfo("properties-submit-button", "properties-form");
        }).catch(error => {
            alert(error);
        });
    }

    return (
        <div id="properties-form-container">
            {renderHeader("Insert monster's properties")}
            <form onSubmit={handleSubmit} id="properties-form">
                {renderNameFormRow()}
                {properties.map(value => renderPropertiesFormRow(value))}
                <button type="submit" id="properties-submit-button">Submit</button>
            </form>
        </div>
    );
}

export default PropertiesForm;
