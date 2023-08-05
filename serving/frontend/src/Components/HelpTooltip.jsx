import {Tooltip} from "react-tooltip";

const HelpTooltip = ({helpText}) => {
    return (
        <div>
            <a
              data-tooltip-id="help-tooltip"
              data-tooltip-content={helpText}
              data-tooltip-place="right"
            >
                <p className="help">?</p>
            </a>
            <Tooltip id="help-tooltip" />
        </div>
    );
}

export default HelpTooltip;
