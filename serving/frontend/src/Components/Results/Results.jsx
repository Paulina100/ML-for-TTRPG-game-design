import {renderHeader} from "../../utils";
import Level from "./Level";
import CounterfactualExamples from "./CounterfactualExamples";

const Results = ({results, monsterProperties, setMonsterProperties}) => {
    return (
        <div id="results">
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
