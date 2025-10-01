🚀 Ejercicio #3: Inventario Inteligente Colaborativo con Predicción y Análisis de Tendencias (Django, IA, y Dashboards)
📋 El Desafío
El objetivo es transformar el sistema de inventario actual en una plataforma más robusta y colaborativa, añadiendo funcionalidades de predicción de demanda, análisis de tendencias y una interfaz de usuario interactiva para la visualización de datos.
Requisitos de la Base de Datos
Mantendremos la estructura de productos actual (nombre, descripción, cantidad), pero la enriqueceremos con:
Historial de Ventas: Una tabla relacionada que registre las ventas de cada producto (fecha, cantidad vendida). Esto es crucial para la predicción.
Proveedor: Un campo para indicar el proveedor de cada producto.
Precio Unitario: Un campo para el precio de venta de cada producto.
Mínimo de Datos: Se requieren al menos 10 productos con un historial de ventas simulado para los últimos 3 meses (pueden ser ventas aleatorias pero con cierta lógica de tendencias si es posible).
🎯 Entregable y Resultado Esperado
El entregable final es el proyecto Django completo, una API RESTful, el script principal (actualizado) y un nuevo script o módulo para la visualización de datos.consultar_inventario.py
Funcionalidad Clave
API RESTful para el Inventario:
Exponer endpoints para listar, crear, actualizar y eliminar productos.
Endpoint para consultar el stock disponible.
Endpoint para registrar ventas (lo que actualizará el stock y el historial de ventas).
Predicción de Demanda con IA:
La IA deberá ser capaz de predecir la demanda futura de cada producto (por ejemplo, para la próxima semana o mes) basándose en el historial de ventas.
Se puede utilizar un modelo de Machine Learning simple (ej. ARIMA, Prophet, o incluso un modelo lineal si los datos son muy básicos) implementado con librerías como o .scikit-learnModelos de estado
Análisis de Tendencias y Reabastecimiento Óptimo:
La IA debe ser capaz de identificar productos con alta rotación o tendencias crecientes/decrecientes en las ventas.
Basado en la predicción de demanda y el stock actual, la IA debería sugerir cuándo y cuánto reabastecer cada producto para evitar quiebres de stock o exceso de inventario.
Panel de Control Interactivo (Dashboard):
Crear una pequeña aplicación web o un script utilizando una librería de visualización de datos (ej. o incluso ) para mostrar:Guión de la tramaGráficos de Django
Stock actual de todos los productos.
Predicción de demanda para los próximos períodos.
Productos con bajo stock o sugerencias de reabastecimiento.
Tendencias de ventas por producto.
consultar_inventario.py (Actualizado):
Este script ahora interactuará con la API RESTful de Django.
Además de consultar productos disponibles, el script debería permitir:
Consultar la predicción de demanda para un producto específico.
Preguntar a la IA sobre sugerencias de reabastecimiento.
Listar productos con baja rotación.
Herramientas Sugeridas (Además de Django y SQLite)
Marco REST de Django (DRF): Para construir la API RESTful de manera eficiente.
Pandas y NumPy: Para manipulación y análisis de datos en Python, especialmente para la preparación de datos para los modelos de ML.
Scikit-learn / Statsmodels / Prophet: Para implementar los modelos de predicción de demanda.
Plotly Dash (o similar): Para crear el dashboard interactivo de visualización de datos. Esto añadiría un componente de front-end ligero sin la complejidad de un framework JS completo, integrándose bien con Python.
