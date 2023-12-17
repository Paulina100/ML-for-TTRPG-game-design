import {useState} from "react";
import {
    displaySubmitInfo,
    getActualPropertiesNames,
    getExtractionMethods,
    renderSubheader
} from "../../utils";
import {minimumPropertyValues} from "./rules";

const FileForm = (setMonsterProperties, setResults) => {
    const [selectedFile, setSelectedFile] = useState(null);
    const [selectedFileName, setSelectedFileName] = useState("");

    const requiredProperties = getActualPropertiesNames()[0];
    const extractionMethods = getExtractionMethods();

    const uploadFile = (file) => {
        if (file === undefined) {
            return;
        }
        setSelectedFile(file);
        setSelectedFileName(file.name);
    };

    const parseFile = (fileReader) => {
        const fileDict = JSON.parse(fileReader.result);
        let resultDict = {};
        try {
            resultDict["name"] = fileDict.name;
            extractionMethods.forEach((extractionMethod, property) => {
                let propertyValue = extractionMethod(fileDict);
                if (propertyValue === undefined) {
                    if (requiredProperties.indexOf(property) !== -1) {
                        throw new Error(`Selected JSON is invalid: value of ${property} was not found.`);
                    } else {
                        propertyValue = 0;
                    }
                }
                if (propertyValue < minimumPropertyValues.get(property)) {
                    throw new Error(`Selected JSON is invalid: value of ${property} has to be ` +
                        `grater than or equal to ${minimumPropertyValues.get(property)} ` +
                        `(currently is ${propertyValue}).`);
                }
                resultDict[property] = propertyValue;
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
            setResults({});

            let serverUrl;
            if (window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1") {
                serverUrl = process.env.REACT_APP_HOST;
            } else {
                serverUrl = process.env.REACT_APP_AWS_HOST;
            }

            fetch(serverUrl + process.env.REACT_APP_UPLOAD_ENDPOINT, {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify(Object.entries(properties).filter(([key]) => key !== "name"))
            }).then((response) => {
                response.json().then(json => setResults(json));
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
            {renderSubheader("Select JSON file containing monster's properties")}
            <p>This file has to have the same structure as files from Pathfinder books.</p>
            <form onSubmit={submitForm} id={"file-form"}>
                <div id={"file-form-input-row"}>
                    <p id="selected-file">{(selectedFileName === "") ? "No file selected." : selectedFileName}</p>
                    <label htmlFor="file-input">
                        <div id="file-input-button">Select file</div>
                    </label>
                    <input type="file" id="file-input" accept=".json"
                           onInput={(e) => uploadFile(e.target.files[0])}
                           required/>
                </div>
                <button type="submit" id="file-submit-button">Submit</button>
            </form>
        </div>
    );
}

export default FileForm;
