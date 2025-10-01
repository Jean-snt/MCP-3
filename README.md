🚀 Ejercicio #3: Inventario Inteligente Colaborativo con Predicción y Análisis de Tendencias

Este proyecto expande el sistema de inventario backend de Python y Django del Ejercicio #2, elevándolo a un nivel intermedio–avanzado.
El objetivo es desarrollar una plataforma más robusta y colaborativa, añadiendo funcionalidades de predicción de demanda, análisis de tendencias y una interfaz interactiva para la visualización de datos.

📋 Desafío

Desarrollar un sistema de inventario inteligente que no solo gestione el catálogo de productos, sino que también utilice Inteligencia Artificial para:

Predecir la demanda.

Sugerir acciones de reabastecimiento.

Proveer acceso mediante una API RESTful y un panel de control interactivo.

✨ Características Principales

Gestión de Inventario
CRUD completo de productos y proveedores.

Historial de Ventas
Registro detallado de cada venta para análisis y predicción.

API RESTful
Puntos finales para interactuar con el sistema desde aplicaciones externas.

Predicción de Demanda (IA)
Modelos de Machine Learning para prever la demanda futura de productos.

Análisis de Tendencias
Identificación de productos con alta/baja rotación y patrones de venta.

Sugerencias de Reabastecimiento
La IA propone cuándo y cuánto reabastecer para optimizar el stock.

Panel de Control
Interfaz web interactiva para visualizar métricas clave del inventario.

Interfaz de Línea de Comandos (CLI)
Script para interactuar directamente con el sistema y la IA desde la terminal.

🎯 Entregables y Resultado Esperado

El proyecto consta de los siguientes componentes principales:

Proyecto Django Completo (smart_inventory_project/)

Modelos de datos para productos, proveedores y ventas.

API RESTful para todas las operaciones de inventario.

Lógica de IA integrada para predicción y análisis.

Script de Interacción CLI (consultar_inventario.py)

Permite consultar el estado del inventario, realizar predicciones y obtener sugerencias de la IA desde la terminal.

Aplicación Dashboard Interactivo (dashboard_app.py)

Aplicación web separada construida con Dash/Plotly para visualizar métricas en tiempo real.

🛠️ Tecnologías Utilizadas

Backend: Python 3.x, Django

Base de Datos: SQLite (por defecto, configurable para PostgreSQL/MySQL)

API: Django REST Framework

IA / Machine Learning:

Pandas

NumPy

Scikit-learn (para regresión lineal básica)

Statsmodels / Prophet (opcional, para series de tiempo más avanzadas)

Visualización / Dashboard: Plotly Dash

Interacción con API: requests (para el CLI y Dashboard)

📂 Estructura del Proyecto
-----------------------------------------
<img width="560" height="424" alt="image" src="https://github.com/user-attachments/assets/9261f789-dbbd-4c24-ac88-04689eff955a" />

