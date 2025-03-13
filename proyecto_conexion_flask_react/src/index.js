import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import Chat from "./chat"; // Importa el componente correctamente
import MyComponent from "./pruebaComponent"


const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(<MyComponent />); // Usa el componente con la primera letra en mayúscula

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals

