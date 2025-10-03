import React from "react";

export default function ProductoCard({ producto }) {
  return (
    <div style={{ border: "1px solid #ccc", padding: "10px", margin: "10px", borderRadius: "5px" }}>
      <h3>{producto.nombre}</h3>
      <p>{producto.descripcion}</p>
      <p>Stock: {producto.cantidad}</p>
      <p>Precio: ${producto.precio_venta}</p>
    </div>
  );
}
