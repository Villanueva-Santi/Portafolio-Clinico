/* src/services/api.js */

import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000/api/",
  headers: {
    "Content-Type": "application/json",
    Accept: "application/json",
  },
});

// Interceptor para agregar token automáticamente
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");

  if (token) {
    config.headers.Authorization = `Token ${token}`;
  } else {
    delete config.headers.Authorization;
  }
  return config;
});

// Manejo de errores global
api.interceptors.response.use(
  (res) => res,
  (error) => {
    if (error.response?.status === 401) {
      console.warn("⚠ Token inválido. Cerrando sesión...");
      localStorage.clear();
      window.location.href = "/login";
    }

    if (!error.response) {
      console.error("❌ No hay conexión con el backend");
      alert("No se pudo conectar con el servidor.");
    }

    return Promise.reject(error);
  }
);

export default api;

// API: Crear autoevaluación
export const crearAutoevaluacion = (data) => {
  return api.post("autoevaluaciones/", data);
};
