import {useState} from "react";
import HelpTooltip from "../HelpTooltip";
import {generateMonsterJSON, getDisplayablePropertiesNames} from "../../utils";
import {IconButton, Tooltip} from "@mui/material";
import EditIcon from '@mui/icons-material/Edit';
import SaveIcon from "@mui/icons-material/Save";

const CounterfactualExamples = ({monsterProperties, setMonsterProperties}) => {
    const [counterfactualExamples, setCounterfactualExamples] = useState([]);
    const [selectedLevel, setSelectedLevel] = useState("");
    const [displayedInfo, setDisplayedInfo] = useState({});
    const [fileDownloadUrl, setFileDownloadUrl] = useState("");
    const [fileDownloadRef, setFileDownloadRef] = useState(null);
    const [isGroupVisible, setIsGroupVisible] = useState([
        {"Speed": true, "Spells": true, "Attacks": true, "Resistance": true, "Weakness": true},
        {"Speed": true, "Spells": true, "Attacks": true, "Resistance": true, "Weakness": true},
        {"Speed": true, "Spells": true, "Attacks": true, "Resistance": true, "Weakness": true},
        {"Speed": true, "Spells": true, "Attacks": true, "Resistance": true, "Weakness": true},
        {"Speed": true, "Spells": true, "Attacks": true, "Resistance": true, "Weakness": true}
    ]);
    const [isCounterfactualExampleVisible, setIsCounterfactualExampleVisible] =
        useState([true, true, true, true, true]);

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
        requestBody["properties"] = {};

        Object.keys(monsterProperties).forEach(key => {
            if (key !== "name") {
                requestBody.properties[key] = monsterProperties[key]
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

    const saveCounterfactualExample = (counterfactualExample, event) => {
        event.preventDefault();
        const blob = new Blob([JSON.stringify(generateMonsterJSON(monsterProperties.name, counterfactualExample))]);
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

    const renderCounterfactualExampleIcons = (counterfactualExample) => {
        return (
            <div>
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
            </div>
        );
    }

    const renderPropertiesRow = (property, cfProperty, currentProperty) => {
        return (
            <div key={property} className={"counterfactual-group-row"}>
                {property}:
                {(currentProperty.toString() !== cfProperty.toString()) ?  // values in PropertiesForm are of type String
                    <span className={"counterfactual-changed-value"}>{cfProperty}</span> :
                    <span className={"counterfactual-unchanged-value"}>{cfProperty}</span>
                }
            </div>
        );
    }

    const renderComplexPropertiesRow = (complexProperty, counterfactualExample, counterfactualExampleIndex,
                                        monsterPropertiesValues, startIndex) => {
        const groupName = complexProperty[0];
        return (
            <div className={"properties-group"}>
                <span className={"counterfactual-group-row"}
                   onClick={() => {
                       const updatedGroupVisible = [...isGroupVisible];
                       updatedGroupVisible[counterfactualExampleIndex][groupName] = !isGroupVisible[counterfactualExampleIndex][groupName];
                       setIsGroupVisible(updatedGroupVisible);
                   }}>
                    {isGroupVisible[counterfactualExampleIndex][groupName] ? "˅" : "˃"} {groupName}
                </span>
                <div className={"properties-group-rows counterfactual-properties-group-rows"}
                     style={{visibility: isGroupVisible[counterfactualExampleIndex][groupName] ? "visible" : "hidden",
                         height: isGroupVisible[counterfactualExampleIndex][groupName] ? "max-content" : "0"}}>
                    {complexProperty[1].map((value, i) =>
                        renderPropertiesRow(value, counterfactualExample[startIndex + i],
                            monsterPropertiesValues[startIndex + i], startIndex + i))}
                </div>
            </div>
        );
    }

    const renderFullCounterfactualExample = (counterfactualExample, counterfactualExampleIndex) => {
        const monsterPropertiesWithoutName = Object.fromEntries(Object.entries(monsterProperties).filter(([key]) => key !== "name"));
        const monsterPropertiesValues = Object.values(monsterPropertiesWithoutName);
        let j = -1;
        return (
            <div className={"properties-grid"}>
                <div className={"properties-column"}>
                    {properties[0].map((value) => {
                        j++;
                        return renderPropertiesRow(value, counterfactualExample[j], monsterPropertiesValues[j]);
                    })}
                </div>
                <div className={"properties-column"}>
                    {properties[1].map((value) => {
                        if (typeof value === "string") {
                            j++;
                            return renderPropertiesRow(value, counterfactualExample[j], monsterPropertiesValues[j])
                        } else {
                            j += value[1].length;
                            return renderComplexPropertiesRow(value, counterfactualExample, counterfactualExampleIndex,
                                monsterPropertiesValues, j - value[1].length + 1)
                        }
                    })}
                </div>
                <div className={"properties-column"}>
                    {properties[2].map((value) => {
                        if (typeof value === "string") {
                            j++;
                            return renderPropertiesRow(value, counterfactualExample[j], monsterPropertiesValues[j])
                        } else {
                            j += value[1].length;
                            return renderComplexPropertiesRow(value, counterfactualExample, counterfactualExampleIndex,
                                monsterPropertiesValues, j - value[1].length + 1)
                        }
                    })}
                </div>
            </div>
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
                    {counterfactualExamples.map((counterfactualExample, index) =>
                        <div className={"counterfactual-group"}>
                            <div className={"counterfactual-group-header"}>
                                <h3 className={"counterfactual-group-header-text"}
                                    onClick={() => {
                                        const updatedIsCfVisible = [...isCounterfactualExampleVisible];
                                        updatedIsCfVisible[index] = !isCounterfactualExampleVisible[index];
                                        setIsCounterfactualExampleVisible(updatedIsCfVisible);
                                    }}>
                                    {isCounterfactualExampleVisible[index] ? "˅ " : "˃ "}
                                    Modified properties #{index+1}
                                </h3>
                                {renderCounterfactualExampleIcons(counterfactualExample)}
                            </div>
                            {isCounterfactualExampleVisible[index] ?
                                renderFullCounterfactualExample(counterfactualExample, index) :
                                <></>
                            }
                        </div>
                    )}
                </div>
            }
        </div>
    );
}

export default CounterfactualExamples;
