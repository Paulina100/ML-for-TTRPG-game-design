import {useEffect, useState} from "react";

const Level = () => {
    const [level, setLevel] = useState(undefined);

    const fetchLevel = () => {
        fetch("http://localhost:8000/level")
            .then(r => r.json())
            .then(r => setLevel(r.level));
    }

    useEffect(() => {setInterval(fetchLevel, 1000)});  // todo: probably should be improved

    return (
        (level === undefined) ?
            <p>Results will be calculated after you submit monster's properties.</p> :
            <p id="level-info">Calculated level value is <span>{level}</span>.</p>
    );
}

export default Level;
