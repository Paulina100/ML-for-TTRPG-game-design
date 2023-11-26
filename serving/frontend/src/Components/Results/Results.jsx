import {renderHeader} from "../../utils";
import Level from "./Level";
import CounterfactualExamples from "./CounterfactualExamples";

const Results = ({results, setResults, monsterProperties, setMonsterProperties}) => {
    return (
        <div id="results">
            {renderHeader("Results")}
            {JSON.stringify(results) === "{}" ?
                <p>Results will be calculated after you submit monster's properties.</p> :
                <div>
                    <Level level={results.level} />
                    <CounterfactualExamples monsterProperties={monsterProperties}
                                            setMonsterProperties={setMonsterProperties}
                                            setResults={setResults} />
                </div>
            }
        </div>
    );
}

export default Results;
