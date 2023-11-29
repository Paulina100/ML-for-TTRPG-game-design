import {useState} from "react";
import HelpTooltip from "../HelpTooltip";
import {getDisplayablePropertiesNames, getGroupedSystemProperties, getPropertiesValuesKeys} from "../../utils";
import {IconButton, Tooltip} from "@mui/material";
import EditIcon from '@mui/icons-material/Edit';
import SaveIcon from "@mui/icons-material/Save";

const CounterfactualExamples = ({monsterProperties, setMonsterProperties}) => {
    const [counterfactualExamples, setCounterfactualExamples] = useState([]);
    const [selectedLevel, setSelectedLevel] = useState("");
    const [displayedInfo, setDisplayedInfo] = useState({});
    const [fileDownloadUrl, setFileDownloadUrl] = useState("");
    const [fileDownloadRef, setFileDownloadRef] = useState(null);

    const properties = getDisplayablePropertiesNames();

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
        if (isNaN(value) || value < -1 || value > 20) {
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

        Object.keys(monsterProperties).forEach(key => {
            if (key !== "name") {
                requestBody[key] = monsterProperties[key]
            }
        });

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
        newMonsterProperties.name = monsterProperties.name;
        counterfactualExample.forEach((value, index) =>
            newMonsterProperties[Object.keys(monsterProperties).at(index+1)] = value);
        setMonsterProperties(newMonsterProperties);
    }

    const getStandardizedPropertiesJson = (counterfactualExample) => {
        const standardizedProperties = {"system": {}};
        const groupedSystemProperties = getGroupedSystemProperties();
        const propertiesValuesKeys = getPropertiesValuesKeys();
        let index = 0;
        groupedSystemProperties.forEach((subproperties, property) => {
            standardizedProperties.system[property] = {};
            const valuesKey = propertiesValuesKeys.get(property);
            for (let subproperty of subproperties) {
                standardizedProperties.system[property][subproperty] = {};
                standardizedProperties.system[property][subproperty][valuesKey] = counterfactualExample[index];
                index++;
            }
        });
        standardizedProperties["name"] = monsterProperties.name;
        return standardizedProperties;
    }

    const saveCounterfactualExample = (counterfactualExample, event) => {
        event.preventDefault();
        const blob = new Blob([JSON.stringify(getStandardizedPropertiesJson(counterfactualExample))]);
        const fileDownloadUrl = URL.createObjectURL(blob);
        setFileDownloadUrl(fileDownloadUrl);
        const interval = setInterval(() => {  // wait until fileDownloadUrl is set
            if (fileDownloadUrl !== "") {
                fileDownloadRef.click();
                URL.revokeObjectURL(fileDownloadUrl);
                setFileDownloadUrl("");
                clearInterval(interval);
            }
        }, 100);
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
                            {(monsterPropertiesValues[valueIndex] !== value &&
                                monsterPropertiesValues[valueIndex] !== value.toString()) ?  // values in PropertiesForm are of type String
                                <span className={"counterfactual-changed-value"}>{value}</span> :
                                <span className={"counterfactual-unchanged-value"}>{value}</span>
                            }
                        </td>
                    );
                })}
                <td className={"counterfactuals-button-cell"}>
                    <Tooltip
                        title={"click to insert these properties to form above"}
                        placement="top"
                        arrow PopperProps={{
                            modifiers: [
                                {
                                    name: "offset",
                                    options: {
                                        offset: [0, -15],
                                    },
                                },
                            ],
                        }}>
                        <button className={"counterfactuals-button"}
                                onClick={() => {applyCounterfactualExample(counterfactualExample)}}>
                            <IconButton>
                                <EditIcon />
                            </IconButton>
                        </button>
                    </Tooltip>
                </td>
                <td className={"counterfactuals-button-cell"}>
                    <Tooltip
                        title={"click to download these properties to JSON file"}
                        placement="top"
                        arrow PopperProps={{
                            modifiers: [
                                {
                                    name: "offset",
                                    options: {
                                        offset: [0, -15],
                                    },
                                },
                            ],
                        }}>
                        <button className={"counterfactuals-button"}
                                onClick={(event) => {saveCounterfactualExample(counterfactualExample, event)}}>
                            <IconButton>
                                <SaveIcon />
                            </IconButton>
                        </button>
                    </Tooltip>
                    <a download={`generated_level_${selectedLevel}.json`}
                       href={fileDownloadUrl}
                       ref={e => setFileDownloadRef(e)}
                       style={{display: "none"}}
                    >Save file</a>
                </td>
            </tr>
        );
    }

    return (
        <div id={"counterfactual-examples"}>
            <p>You can now generate new sets of properties to create a monster with selected level.
                The properties will be based on the ones from the forms above. New level's value has to be between -1 and 20.</p>
            <form onSubmit={handleSubmit} id="counterfactuals-form">
                <label htmlFor="selectedLevel" id="counterfactuals-form-label">Modify calculated level to value: </label>
                <input id="selectedLevel" name="selectedLevel" type="text" value={selectedLevel} required
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
                : <div>
                    <p>Click on <EditIcon fontSize={"small"} /> to insert selected properties to the form above.
                        You will have to resubmit the form manually. Alternatively, click on <SaveIcon fontSize={"small"}/> to
                        save properties to a JSON file.</p>
                    <table id={"counterfactuals-table"}>
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
                </div>
            }
        </div>
    );
}

export default CounterfactualExamples;
