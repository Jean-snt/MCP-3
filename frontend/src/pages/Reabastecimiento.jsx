import React, { useEffect, useState } from "react";
import { getProductos, getVentas } from "../services/api";

export default function Reabastecimiento() {
  const [productos, setProductos] = useState([]);
  const [ventas, setVentas] = useState([]);
  const [sugerencias, setSugerencias] = useState([]);

  useEffect(() => {
    async function fetchData() {
      const prods = await getProductos();
      const vtas = await getVentas();
      setProductos(prods);
      setVentas(vtas);

      const sugerencias = prods.map(p => {
        const totalVendida = vtas.filter(v => v.producto === p.id)
                                  .reduce((sum, v) => sum + v.cantidad_vendida, 0);
        if (p.cantidad < totalVendida) {
          return `Reabastecer ${p.nombre}: stock actual ${p.cantidad}, demanda estimada ${totalVendida}`;
        }
        return null;
      }).filter(Boolean);

      setSugerencias(sugerencias);
    }

    fetchData();
  }, []);

  return (
    <div>
      <h1>Sugerencias de Reabastecimiento</h1>
      <ul>
        {sugerencias.length > 0 ? (
          sugerencias.map((s, i) => <li key={i}>{s}</li>)
        ) : (
          <li>No hay productos críticos por reabastecer</li>
        )}
      </ul>
    </div>
  );
}
