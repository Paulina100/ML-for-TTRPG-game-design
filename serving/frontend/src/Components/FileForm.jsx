import {useState} from "react";
import {renderHeader} from "../utils";

const FileForm = () => {
    const [selectedFile, setSelectedFile] = useState(null);
    const [selectedFileName, setSelectedFileName] = useState("");
    const systemProperties = new Map([
            ["attributes", ["ac", "hp"]],  // value
            ["abilities", ["str", "dex", "con", "int", "wis", "cha"]]  //mod
        ]);
    const propertiesValuesKey = new Map([
        ["attributes", "value"],
        ["abilities", "mod"]
    ]);

    const uploadFile = (file) => {
        if (file === undefined) {
            return;
        }
        setSelectedFile(file);
        setSelectedFileName(file.name);
    };

    const parseFile = (fileReader) => {
        const fileDict = JSON.parse(fileReader.result);
        const systemDict = fileDict.system;
        let resultDict = {};
        try {
            systemProperties.forEach((subproperties, property) => {
                const valuesKey = propertiesValuesKey.get(property);
                for (let subproperty of subproperties) {
                    resultDict[subproperty] = systemDict[property][subproperty][valuesKey];
                    if (typeof resultDict[subproperty] != "number") {
                        throw new Error("Selected JSON is invalid.")
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
            fetch("http://localhost:8000/properties/upload", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify(properties)
            }).catch(e => {
                alert(e);
            });
        });
    };

    return (
        <div id="file-form-container">
            {renderHeader("Select JSON file containing monster's properties")}
            <p>This file has to have the same structure as files from Pathfinder books.</p>
            <form onSubmit={submitForm}>
                <label htmlFor="file-input">
                    <div id="file-input-button">Select file</div>
                </label>
                <input type="file" id="file-input" accept=".json" onInput={(e) => uploadFile(e.target.files[0])} required/>
                <p id="selected-file">{(selectedFileName === "") ? "No file selected." : selectedFileName}</p>
                <button type="submit">Submit</button>
            </form>
        </div>
    );
}

export default FileForm;
