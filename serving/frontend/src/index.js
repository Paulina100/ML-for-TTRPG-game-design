import React from "react";
import {render} from 'react-dom';
import {ChakraProvider, Flex} from "@chakra-ui/react";

import Header from "./Components/Header";
import PageInfo from "./Components/PageInfo"
import Forms from "./Components/Forms";
import Footer from "./Components/Footer";
import Results from "./Components/Results";

import "./style.css";

function App() {
    console.log("starting...");
    return (
        <ChakraProvider>
            <Header />
            <Flex id="page-background">
                <div id="page-content">
                    <PageInfo />
                    {Forms()}
                    {Results()}
                </div>
            </Flex>
            <Footer />
        </ChakraProvider>
    )
}

const rootElement = document.getElementById("root")
render(<App />, rootElement)