import {renderHeader} from "../../utils";
import Level from "./Level";
import CounterfactualExamples from "./CounterfactualExamples";

const Results = ({results, monsterProperties, setMonsterProperties}) => {
    return (
        <div id="results">
            {renderHeader("Results")}
            {JSON.stringify(results) === "{}" ?
                <p>Results will be calculated after you submit monster's properties.</p> :
                <div>
                    <Level level={results.level} />
                    <CounterfactualExamples monsterProperties={monsterProperties} setMonsterProperties={setMonsterProperties} level={results.level} />
                </div>
            }
        </div>
    );
}

export default Results;
