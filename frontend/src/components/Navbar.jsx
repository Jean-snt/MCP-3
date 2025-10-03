import React from "react";
import { Link } from "react-router-dom";

export default function Navbar() {
  return (
    <nav style={{ padding: "10px", background: "#282c34", color: "white" }}>
      <Link to="/" style={{ margin: "10px", color: "white" }}>Dashboard</Link>
      <Link to="/productos" style={{ margin: "10px", color: "white" }}>Productos</Link>
      <Link to="/reabastecimiento" style={{ margin: "10px", color: "white" }}>Reabastecimiento</Link>
    </nav>
  );
}
