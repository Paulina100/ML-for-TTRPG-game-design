import React, {useState} from "react";
import {render} from 'react-dom';

import Header from "./Components/Header";
import PageInfo from "./Components/PageInfo"
import Forms from "./Components/Forms/Forms";
import Footer from "./Components/Footer";
import Results from "./Components/Results/Results";

import "./style.css";

function App() {
    console.log("starting...");

    const [results, setResults] = useState({});

    return (
        <div id="app">
            <Header />
            <div id="page-background">
                <div id="page-content">
                    <PageInfo />
                    <Forms setResultsFunction={setResults} />
                    <Results results={results} />
                </div>
            </div>
            <Footer />
        </div>
    )
}

const rootElement = document.getElementById("root")
render(<App />, rootElement)