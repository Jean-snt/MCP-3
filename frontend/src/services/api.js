import axios from "axios";

const API_URL = "http://127.0.0.1:8000/api";

export const getProductos = async () => {
  const response = await axios.get(`${API_URL}/productos/`);
  return response.data;
};

export const getVentas = async () => {
  const response = await axios.get(`${API_URL}/ventas/`);
  return response.data;
};
