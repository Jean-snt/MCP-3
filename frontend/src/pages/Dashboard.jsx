import React, { useEffect, useState } from "react";
import { getProductos, getVentas } from "../services/api";
import VentaChart from "../components/VentaChart";

export default function Dashboard() {
  const [productos, setProductos] = useState([]);
  const [ventas, setVentas] = useState([]);

  useEffect(() => {
    getProductos().then(setProductos);
    getVentas().then(setVentas);
  }, []);

  return (
    <div>
      <h1>Dashboard de Inventario</h1>
      <VentaChart productos={productos} ventas={ventas} />
    </div>
  );
}
