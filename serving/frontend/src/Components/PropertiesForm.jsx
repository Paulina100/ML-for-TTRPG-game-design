import {
    FormControl,
    FormLabel, NumberDecrementStepper,
    NumberIncrementStepper,
    NumberInput,
    NumberInputField,
    NumberInputStepper
} from "@chakra-ui/react";
import {renderHeader} from "../utils";

const properties = ["Armor Class (AC)", "Hit Points (HP)", "Strength (Str)", "Dexterity (Dex)",
    "Concentration (Con)", "Intelligence (Int)", "Wisdom (Wis)", "Charisma (Cha)"]


function extractBracketedWord(property) {
    return property.substring(property.indexOf("(") + 1, property.indexOf(")")).toLowerCase();
}

function renderPropertiesFormRow(property) {
    return (
        <FormControl key={extractBracketedWord(property)}>
            <div id="properties-form-row">
                <FormLabel as={extractBracketedWord(property)} htmlFor={extractBracketedWord(property)}
                           id="properties-form-label">{property}</FormLabel>
                <NumberInput isRequired>
                    <NumberInputField/>
                    <NumberInputStepper>
                        <NumberIncrementStepper/>
                        <NumberDecrementStepper/>
                    </NumberInputStepper>
                </NumberInput>
            </div>
        </FormControl>
    );
}

const PropertiesForm = () => {
    return (
        <div id="properties-form-container">
            {renderHeader("Insert monster's properties")}
            {properties.map(value => renderPropertiesFormRow(value))}
            <button type="submit">Submit</button>
        </div>
    );
}

export default PropertiesForm;
