import {useState} from "react";
import {displaySubmitInfo, renderHeader} from "../../utils";
import {minimumPropertyValues} from "./rules";

const FileForm = (setMonsterProperties, setResultsFunction) => {
    const [selectedFile, setSelectedFile] = useState(null);
    const [selectedFileName, setSelectedFileName] = useState("");
    const systemProperties = new Map([
        ["abilities", ["str", "dex", "con", "int", "wis", "cha"]],  // mod
        ["attributes", ["ac", "hp"]]  // value
    ]);
    const propertiesValuesKey = new Map([
        ["abilities", "mod"],
        ["attributes", "value"]
    ]);

    const uploadFile = (file) => {
        if (file === undefined) {
            return;
        }
        setSelectedFile(file);
        setSelectedFileName(file.name);
    };

    const unpackValue = (dict, dictKeys) => {
        let current = dict;
        for (let dictKey of dictKeys) {
            if (! current.hasOwnProperty(dictKey)) {
                const keyPath = dictKeys.join("/");
                throw new Error("Selected JSON is invalid: value from " + keyPath + " was not found.")
            }
            current = current[dictKey];
        }
        return current;
    }

    const parseFile = (fileReader) => {
        const fileDict = JSON.parse(fileReader.result);
        const systemDict = fileDict.system;
        let resultDict = {};
        try {
            resultDict["name"] = fileDict.name;
            systemProperties.forEach((subproperties, property) => {
                const valuesKey = propertiesValuesKey.get(property);
                for (let subproperty of subproperties) {
                    const unpackedValue = unpackValue(systemDict, [property, subproperty, valuesKey]);
                    resultDict[subproperty] = unpackedValue;
                    if (unpackedValue < minimumPropertyValues.get(subproperty)) {
                        throw new Error("Selected JSON is invalid: value of " + property + "/" + subproperty +
                            " has to be grater than or equal to " + minimumPropertyValues.get(subproperty) +
                            " (currently is " + unpackedValue + ").");
                    }
                }
            })
        } catch (e) {
            alert(e);
            return null;
        }
        return resultDict;
    };

    const submitForm = async (e) => {
        e.preventDefault();
        let reader = new FileReader();
        reader.readAsText(selectedFile);
        reader.addEventListener("load", (event) => {
            const properties = parseFile(reader);
            if (properties === null) {
                return;
            }
            fetch("http://" + process.env.REACT_APP_HOST + ":" + process.env.REACT_APP_PORT + process.env.REACT_APP_UPLOAD_ENDPOINT, {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify(properties)
            }).then((response) => {
                response.json().then(json => setResultsFunction(json));
                displaySubmitInfo("file-submit-button", "file-form");
                setMonsterProperties(properties);
                alert("File was uploaded successfully. " +
                    "Monster's properties were inserted to the form on the left " +
                    "where they can be easily edited and resubmitted.")
            }).catch(e => {
                alert(e);
            });
        });
    };

    return (
        <div id="file-form-container">
            {renderHeader("Select JSON file containing monster's properties")}
            <p>This file has to have the same structure as files from Pathfinder books.</p>
            <form onSubmit={submitForm} id="file-form">
                <label htmlFor="file-input">
                    <div id="file-input-button">Select file</div>
                </label>
                <input type="file" id="file-input" accept=".json" onInput={(e) => uploadFile(e.target.files[0])}
                       required/>
                <p id="selected-file">{(selectedFileName === "") ? "No file selected." : selectedFileName}</p>
                <button type="submit" id="file-submit-button">Submit</button>
            </form>
        </div>
    );
}

export default FileForm;
