import FileForm from "./FileForm";
import PropertiesForm from "./PropertiesForm";
import {useState} from "react";

function renderCaption() {
    return(
        <div className="page-info">
            <div className="content-header">First step</div>
            <p>You can choose between two ways of entering your monster's properties:
                you can either manually fill in values of available properties
                or upload a JSON file with monster's characteristics. </p>
        </div>
    );
}

const Forms = () => {
    const [monsterProperties, setMonsterProperties] = useState(null);

    return (
        <div>
            { renderCaption() }
            <div id="forms-grid">
                { PropertiesForm(monsterProperties) }
                { FileForm(setMonsterProperties) }
            </div>
        </div>
    );
}

export default Forms;
