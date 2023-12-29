import {generateMonsterJSON, renderHeader} from "../../utils";
import Level from "./Level";
import CounterfactualExamples from "./CounterfactualExamples";
import {useState} from "react";

const Results = ({results, monsterProperties, setMonsterProperties}) => {
    const [fileDownloadUrl, setFileDownloadUrl] = useState("");
    const [fileDownloadRef, setFileDownloadRef] = useState(null);

    const savePropertiesToFile = (event) => {
        event.preventDefault();
        const blob = new Blob([JSON.stringify(
            generateMonsterJSON(monsterProperties.name,
                Object.values(Object.fromEntries(Object.entries(monsterProperties).filter(([key]) => key !== "name"))))
        )]);
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

    return (
        <div id="results">
            {
                results.level !== undefined ?
                    <div>
                        <button id={"save-properties-button"}
                                onClick={(event) => {savePropertiesToFile(event)}}>
                            Save properties from form to file
                        </button>
                        <a download={`${monsterProperties.name}.json`}
                           href={fileDownloadUrl}
                           ref={e => setFileDownloadRef(e)}
                           style={{display: "none"}}
                        >Save file</a>
                    </div> :
                    <></>
            }
            {renderHeader("Results")}
            {JSON.stringify(results) === "{}" ?
                <p>Results will be calculated after you submit monster's properties.</p> :
                results.level !== undefined ?
                    <div>
                        <Level level={results.level} />
                        <CounterfactualExamples monsterProperties={monsterProperties}
                                                setMonsterProperties={setMonsterProperties} />
                    </div> :
                    <p>Level was not calculated successfully. Please review your input and try again. If this error
                        persists, you are welcome to <a href={"https://github.com/Paulina100/ML-for-TTRPG-game-design/issues/new"}
                                                        target={"_blank"} rel={"noreferrer"}>open an issue on app's github</a>
                        {" "}to let us know.</p>
            }
        </div>
    );
}

export default Results;
