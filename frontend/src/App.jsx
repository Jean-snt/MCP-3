import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import Dashboard from "./pages/Dashboard";
import Productos from "./pages/Productos";
import Reabastecimiento from "./pages/Reabastecimiento";

export default function App() {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/productos" element={<Productos />} />
        <Route path="/reabastecimiento" element={<Reabastecimiento />} />
      </Routes>
    </Router>
  );
}

