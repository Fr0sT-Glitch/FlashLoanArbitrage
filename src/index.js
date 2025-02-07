import React from "react";
import ReactDOM from "react-dom";
import App from "./App";

// Import global styles
import "./index.css";

// Render the main application component
ReactDOM.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
  document.getElementById("root")
);