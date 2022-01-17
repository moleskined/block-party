import React, { Component } from "react";
import { render } from "react-dom";

class App extends React.Component {
  render() {
    return (
      <React.StrictMode>
        <p>Hello world</p>
      </React.StrictMode>
    );
  }
}

export default App;

const container = document.getElementById("app");
render(<App />, container);