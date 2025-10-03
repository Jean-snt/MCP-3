import React from "react";
import { Bar } from "react-chartjs-2";
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from "chart.js";

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

export default function VentaChart({ productos, ventas }) {
  const data = {
    labels: productos.map(p => p.nombre),
    datasets: [
      {
        label: "Cantidad Vendida",
        data: productos.map(p => {
          const total = ventas
            .filter(v => v.producto === p.id)
            .reduce((sum, v) => sum + v.cantidad_vendida, 0);
          return total;
        }),
        backgroundColor: "rgba(75, 192, 192, 0.6)",
      },
    ],
  };

  return <Bar data={data} />;
}
