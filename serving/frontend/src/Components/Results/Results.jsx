import {renderHeader} from "../../utils";
import Level from "./Level";

const Results = () => {
    return (
        <div id="results">
            {renderHeader("Results")}
            {Level()}
        </div>
    );
}

export default Results;
