import {renderHeader} from "../../utils";
import Level from "./Level";

const Results = ({results}) => {
    return (
        <div id="results">
            {renderHeader("Results")}
            {JSON.stringify(results) === "{}" ?
                <p>Results will be calculated after you submit monster's properties.</p> :
                <Level level={results.level} />
            }
        </div>
    );
}

export default Results;
