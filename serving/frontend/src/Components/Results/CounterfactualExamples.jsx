import {useState} from "react";
import HelpTooltip from "../HelpTooltip";

const CounterfactualExamples = ({monsterProperties, setMonsterProperties, level}) => {
    const [counterfactualExamples, setCounterfactualExamples] = useState([]);
    const [selectedLevel, setSelectedLevel] = useState("");
    const [displayedInfo, setDisplayedInfo] = useState({});

    const properties = ["Strength (Str)", "Dexterity (Dex)", "Constitution  (Con)", "Intelligence (Int)",
        "Wisdom (Wis)", "Charisma (Cha)", "Armor Class (AC)", "Hit Points (HP)"];

    const validatePressedKey = (event) => {
        const allowedKeys = ["Backspace", "Enter", "Tab", "ArrowLeft", "ArrowRight"];
        if (!/[0-9]/.test(event.key) && !allowedKeys.includes(event.key) && event.key !== "-") {
            event.preventDefault();
        }
        if (event.key === "-" && selectedLevel !== "") {
            event.preventDefault();
        }
    }

    const validateInput = () => {
        const value = parseInt(selectedLevel);
        const inputCell = document.getElementById("selectedLevel");
        if (isNaN(value) || value < -1) {
            inputCell.className = "invalid-input";
        } else {
            inputCell.className = "";
        }
    }

    const handleSubmit = (event) => {
        event.preventDefault();

        setCounterfactualExamples([]);

        const formData = new FormData(event.target);
        const formJson = Object.fromEntries(formData.entries());

        const value = parseInt(selectedLevel);
        if (isNaN(value) || value < -1 || value > 20) {
            window.alert("Entered input is invalid. Form will not be submitted.");
            return;
        }

        const requestBody = {};
        requestBody["level"] = formJson["selectedLevel"];

        Object.keys(monsterProperties).forEach(key => requestBody[key] = monsterProperties[key]);

        setDisplayedInfo({"text": "Calculating, please wait..."});

        let serverUrl;
        if (window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1") {
            serverUrl = process.env.REACT_APP_HOST;
        } else {
            serverUrl = process.env.REACT_APP_AWS_HOST;
        }

        fetch(serverUrl + process.env.REACT_APP_COUNTERFACTUALS_ENDPOINT, {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(requestBody)
        }).then((response) => {
            response.json().then(json => {
                if (! json.hasOwnProperty("values")) {
                    setDisplayedInfo({"text": "Time limit has been exceeded. New properties have not been generated. ",
                        "help": "This may happen if requested level is much bigger or much smaller than the original value."})
                } else {
                    setCounterfactualExamples(json["values"]);
                    setDisplayedInfo({});
                }
            });
        }).catch(error => {
            alert(error);
        });
    }

    const applyCounterfactualExample = (counterfactualExample) => {
        let newMonsterProperties = {};
        counterfactualExample.forEach((value, index) =>
            newMonsterProperties[Object.keys(monsterProperties).at(index+1)] = value);
        setMonsterProperties(newMonsterProperties);
    }

    const renderCounterfactualExampleRow = (counterfactualExample, exampleIndex) => {
        let monsterPropertiesValues = [];
        for (let key in monsterProperties) {
            if (key !== "name") {
                monsterPropertiesValues.push(monsterProperties[key]);
            }
        }
        return (
            <tr key={exampleIndex} className={"counterfactuals-table-row"}>
                {counterfactualExample.map((value, valueIndex) => {
                    return (
                        <td className={"counterfactuals-table-cell"}>
                            {(monsterPropertiesValues[valueIndex] !== value) ?
                                <span className={"counterfactual-changed-value"}>{value}</span> :
                                <span className={"counterfactual-unchanged-value"}>{value}</span>
                            }
                        </td>
                    );
                })}
                <td className={"counterfactuals-table-cell counterfactuals-button-cell"}>
                    <button className={"counterfactuals-button"} onClick={() => {applyCounterfactualExample(counterfactualExample)}}>Apply</button>
                </td>
                <td className={"counterfactuals-table-cell counterfactuals-button-cell"}>
                    <button className={"counterfactuals-button"}>Save</button>
                </td>
            </tr>
        );
    }

    return (
        <div id={"counterfactual-examples"}>
            <p>You can now generate new sets of properties to create a monster with selected level.
                The properties will be based on the ones from the forms above. New level's value has to be bigger than -2 and smaller than 21.</p>
            <form onSubmit={handleSubmit} id="counterfactuals-form">
                <label htmlFor="selectedLevel" id="counterfactuals-form-label">Modify calculated level to value: </label>
                <input id="selectedLevel" name="selectedLevel" type="text" required
                       onKeyDown={(event) => {
                           validatePressedKey(event);
                       }}
                        onChange={(event) => {
                            setSelectedLevel(event.target.value)
                        }}
                        onBlur={() => {validateInput();}}/>
                <button type="submit" id="counterfactuals-submit-button">Generate new properties</button>
            </form>
            {(displayedInfo !== {})
                ? <div id={"counterfactuals-wait-info"}><span>{displayedInfo["text"]}</span>
                    {(displayedInfo.hasOwnProperty("help"))
                        ? <HelpTooltip helpText={displayedInfo["help"]}></HelpTooltip>
                        : <></>}</div>
                : <></>}
            {(counterfactualExamples.length === 0)
                ? <></>
                : <table id={"counterfactuals-table"}>
                    <thead>
                        <tr className={"counterfactuals-table-row"}>
                            {properties.map(property => {return <th key={property} className={"counterfactuals-table-cell"}>{property}</th>})}
                            <th className={"counterfactuals-button-column"}></th>
                            <th className={"counterfactuals-button-column"}></th>
                        </tr>
                    </thead>
                    <tbody>
                        {counterfactualExamples.map((counterfactualExample, index) =>
                            renderCounterfactualExampleRow(counterfactualExample, index)
                        )}
                    </tbody>
                </table>
            }
        </div>
    );
}

export default CounterfactualExamples;
