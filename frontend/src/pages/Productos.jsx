import React, { useEffect, useState } from "react";
import { getProductos } from "../services/api";
import ProductoCard from "../components/ProductoCard";

export default function Productos() {
  const [productos, setProductos] = useState([]);

  useEffect(() => {
    getProductos().then(setProductos);
  }, []);

  return (
    <div>
      <h1>Productos Disponibles</h1>
      <div style={{ display: "flex", flexWrap: "wrap" }}>
        {productos.map(p => (
          <ProductoCard key={p.id} producto={p} />
        ))}
      </div>
    </div>
  );
}



// Dentro de Productos.jsx
const [productos, setProductos] = useState([]);
const [nuevoProducto, setNuevoProducto] = useState({nombre:"", descripcion:"", cantidad:0, precio_venta:0});

// Crear producto
const crearProducto = () => {
  const id = productos.length + 1;
  setProductos([...productos, { ...nuevoProducto, id }]);
  setNuevoProducto({nombre:"", descripcion:"", cantidad:0, precio_venta:0});
}

// Editar producto
const editarProducto = (id, datos) => {
  setProductos(productos.map(p => p.id === id ? {...p, ...datos} : p));
}

// Eliminar producto
const eliminarProducto = (id) => {
  setProductos(productos.filter(p => p.id !== id));
}
