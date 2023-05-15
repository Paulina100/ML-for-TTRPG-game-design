import FileForm from "./FileForm";
import PropertiesForm from "./PropertiesForm";

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

export default function renderForms() {
    return (
        <div>
            { renderCaption() }
        <div id="forms-grid">
            { PropertiesForm() }
            { FileForm() }
        </div>
            </div>
    );
}
