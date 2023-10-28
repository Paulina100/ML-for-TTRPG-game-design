import {useState} from "react";
import HelpTooltip from "../HelpTooltip";

const CounterfactualExamples = (monsterProperties, setMonsterProperties, level) => {
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
        if (isNaN(value) || value < -1) {
            window.alert("Entered input is invalid. Form will not be submitted.");
            return;
        }

        const requestBody = {};
        requestBody["level"] = formJson["selectedLevel"];

        Object.keys(monsterProperties.monsterProperties)
          .forEach(key => requestBody[key] = monsterProperties.monsterProperties[key]);

        setDisplayedInfo({"text": "Calculating, please wait..."});

        fetch("http://" + process.env.REACT_APP_HOST + ":" + process.env.REACT_APP_PORT + process.env.REACT_APP_COUNTERFACTUALS_ENDPOINT, {
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

    const renderCounterfactualExampleRow = (counterfactualExample, exampleIndex) => {
        let monsterPropertiesValues = [];
        for (let key in monsterProperties.monsterProperties) {
            if (key !== "name") {
                monsterPropertiesValues.push(monsterProperties.monsterProperties[key]);
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
            </tr>
        );
    }

    return (
        <div id={"counterfactual-examples"}>
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
