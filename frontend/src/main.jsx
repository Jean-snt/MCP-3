import React from "react";
import ReactDOM from "react-dom/client";  // Asegúrate de que sea así
import App from "./App";                   // Solo una vez
import "./index.css";                      

// Renderiza la app
ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
