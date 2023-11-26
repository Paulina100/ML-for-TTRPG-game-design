import {displaySubmitInfo, getDisplayablePropertiesNames, renderSubheader} from "../../utils";
import {minimumPropertyValues} from "./rules";
import HelpTooltip from "../HelpTooltip";

const PropertiesForm = (monsterProperties, setMonsterProperties, setResultsFunction) => {
    const properties = getDisplayablePropertiesNames();

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
                           setMonsterProperties(monsterProperties => ({
                               ...monsterProperties,
                               ...{[propertyShort]: event.target.value}
                           }));
                       }}
                       onBlur={() => {validateInput(propertyShort)}}
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

        for (let property in monsterProperties) {
            if (property === "name") {
                continue;
            }
            let value = parseInt(monsterProperties[property]);
            if (isNaN(value) || value < minimumPropertyValues.get(property)) {
                window.alert("Entered input is invalid. Form will not be submitted.");
                return;
            }
        }

        let serverUrl;
        if (window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1") {
            serverUrl = process.env.REACT_APP_HOST;
        } else {
            serverUrl = process.env.REACT_APP_AWS_HOST;
        }

        fetch(serverUrl + process.env.REACT_APP_UPLOAD_ENDPOINT, {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(Object.entries(formJson).filter(([key]) => key !== "name"))
        }).then((response) => {
            response.json().then(json => setResultsFunction(json));
            displaySubmitInfo("properties-submit-button", "properties-form");
        }).catch(error => {
            alert(error);
        });
    }

    return (
        <div id="properties-form-container">
            {renderSubheader("Insert monster's properties")}
            <form onSubmit={handleSubmit} id="properties-form">
                {renderNameFormRow()}
                {properties.map(value => renderPropertiesFormRow(value))}
                <button type="submit" id="properties-submit-button">Submit</button>
            </form>
        </div>
    );
}

export default PropertiesForm;
