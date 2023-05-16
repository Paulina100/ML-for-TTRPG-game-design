import {useState} from "react";
import {renderHeader} from "../utils";

const FileForm = () => {
    const [selectedFile, setSelectedFile] = useState(null);
    const [selectedFileName, setSelectedFileName] = useState("");
    const [obtainedProperties, setObtainedProperties] = useState({});

    const uploadFile = (file) => {
        if (file === undefined) {
            return;
        }
        setSelectedFile(file);
        setSelectedFileName(file.name);
    };

    const submitForm = async (e) => {
        e.preventDefault();
        const formData = new FormData();
        formData.append("file", selectedFile);
        await fetch("http://localhost:8000/properties/upload-file", {
            method: "POST",
            body: formData
        })
            .then(getUploadedData)
            .catch((e) => {alert(e);});
    };

    const getUploadedData = async () => {
        const properties = await fetch("http://localhost:8000/properties");
        const properties_dict = await properties.json();
        setObtainedProperties(properties_dict);
    }

    return (
        <div id="file-form-container">
            {renderHeader("Select JSON file containing monster's properties")}
            <p>This file has to have the same structure as files from Pathfinder books.</p>
            <form onSubmit={submitForm}>
                <label htmlFor="file-input">
                    <div id="file-input-button">Select file</div>
                </label>
                <input type="file" id="file-input" onInput={(e) => uploadFile(e.target.files[0])} required/>
                <p id="selected-file">{(selectedFileName === "") ? "No file selected." : selectedFileName}</p>
                <button type="submit">Submit</button>
            </form>
            <div>{"{"}{Object.entries(obtainedProperties).map(([k, v]) => {return k + ": " + v + ", "})}{"}"}</div>
        </div>
    );
}

export default FileForm;
