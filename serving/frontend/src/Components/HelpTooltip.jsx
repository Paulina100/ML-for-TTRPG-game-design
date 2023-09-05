import {IconButton, Tooltip} from "@mui/material";
import HelpOutlineIcon from '@mui/icons-material/HelpOutline';

const HelpTooltip = ({helpText}) => {
    return (
        <Tooltip
            title={helpText}
            placement="right"
            arrow PopperProps={{
                modifiers: [
                    {
                        name: "offset",
                        options: {
                            offset: [0, -15],
                        },
                    },
                ],
        }}>
            <IconButton>
                <HelpOutlineIcon />
            </IconButton>
        </Tooltip>
    );
}

export default HelpTooltip;
