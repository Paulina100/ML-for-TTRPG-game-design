import React from "react";
import { Heading, Flex } from "@chakra-ui/react";

const Header = () => {
    return (
        <Flex id="header" as="nav">
            <Heading as="h1" size="xl">Pathfinder Monster Creator</Heading>
        </Flex>
    );
};

export default Header;
