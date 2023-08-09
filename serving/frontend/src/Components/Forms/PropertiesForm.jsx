import {displaySubmitInfo, renderHeader} from "../../utils";
import {minimumPropertyValues} from "./rules";
import HelpTooltip from "../HelpTooltip";

const PropertiesForm = (monsterProperties, setMonsterProperties, setResultsFunction) => {
    const properties = ["Strength (Str)", "Dexterity (Dex)", "Constitution  (Con)", "Intelligence (Int)",
        "Wisdom (Wis)", "Charisma (Cha)", "Armor Class (AC)", "Hit Points (HP)"]

    const extractBracketedWord = (property) => {
        return property.substring(property.indexOf("(") + 1, property.indexOf(")")).toLowerCase();
    }

    const validatePressedKey = (event, propertyName) => {
        const allowedKeys = ["Backspace", "Enter", "Tab", "ArrowLeft", "ArrowRight", "ArrowTop", "ArrowDown"];
        if (!/[0-9]/.test(event.key) && !allowedKeys.includes(event.key) && event.key !== "-") {
            event.preventDefault();
        }
        if (event.key === "-" && monsterProperties[propertyName] !== undefined && monsterProperties[propertyName] !== "") {
            event.preventDefault();
        }
    }

    const validateInput = (property) => {
        const value = parseInt(monsterProperties[property]);
        const inputCell = document.getElementById(property);
        if (isNaN(value) || value < minimumPropertyValues.get(property)) {
            inputCell.className = "invalid-input";
        } else {
            inputCell.className = "";
        }
    }

    const renderPropertiesFormRow = (property) => {
        const propertyShort = extractBracketedWord(property);
        return (
            <div className="properties-form-row" key={propertyShort}>
                <label htmlFor={propertyShort} id="properties-form-label">{property}</label>
                <input id={propertyShort} name={propertyShort} type="text" required
                       onKeyDown={(event) => {
                           validatePressedKey(event, propertyShort);
                       }}
                       onChange={(event) => {
                           setMonsterProperties({[propertyShort]: event.target.value});
                       }}
                       onBlur={() => validateInput(propertyShort)}
                       value={(monsterProperties === null) ? "" : monsterProperties[propertyShort]}/>
                <HelpTooltip
                    helpText={"Enter a number greater than or equal to " + minimumPropertyValues.get(propertyShort)}
                />
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

        if (document.getElementsByClassName("invalid-input").length > 0) {
            window.alert("Entered input is invalid. Form will not be submitted.");
            return;
        }

        fetch("http://localhost:8000/properties/upload", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(formJson)
        }).then((response) => {
            response.json().then(json => setResultsFunction(json));
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
