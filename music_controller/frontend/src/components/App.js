import React, { Component } from "react";
import { render } from "react-dom";
import { HomePage } from "./HomePage";

export function App() {
  return (
    <div className="center">
      <HomePage />
    </div>
  );
}

const divApp = document.getElementById("app");
render(<App />, divApp);
