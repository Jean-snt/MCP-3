## 馃殌 Ejercicio #3: Inventario Inteligente Colaborativo con Predicci贸n y An谩lisis de Tendencias (Django, IA, y Dashboards)

### 馃搵 El Desaf铆o

El objetivo es transformar el sistema de inventario actual en una plataforma m谩s robusta y colaborativa, a帽adiendo funcionalidades de predicci贸n de demanda, an谩lisis de tendencias y una interfaz de usuario interactiva para la visualizaci贸n de datos.

### Requisitos de la Base de Datos

Mantendremos la estructura de productos actual (nombre, descripci贸n, cantidad), pero la enriqueceremos con:

*   **Historial de Ventas:** Una tabla relacionada que registre las ventas de cada producto (fecha, cantidad vendida). Esto es crucial para la predicci贸n.
*   **Proveedor:** Un campo para indicar el proveedor de cada producto.
*   **Precio Unitario:** Un campo para el precio de venta de cada producto.

**M铆nimo de Datos:** Se requieren al menos 10 productos con un historial de ventas simulado para los 煤ltimos 3 meses (pueden ser ventas aleatorias pero con cierta l贸gica de tendencias si es posible).

### 馃幆 Entregable y Resultado Esperado

El entregable final es el proyecto Django completo, una API RESTful, el script principal `consultar_inventario.py` (actualizado) y un nuevo script o m贸dulo para la visualizaci贸n de datos.

### Funcionalidad Clave

1.  **API RESTful para el Inventario:**
    *   Exponer endpoints para listar, crear, actualizar y eliminar productos.
    *   Endpoint para consultar el stock disponible.
    *   Endpoint para registrar ventas (lo que actualizar谩 el stock y el historial de ventas).

2.  **Predicci贸n de Demanda con IA:**
    *   La IA deber谩 ser capaz de predecir la demanda futura de cada producto (por ejemplo, para la pr贸xima semana o mes) bas谩ndose en el historial de ventas.
    *   Se puede utilizar un modelo de Machine Learning simple (ej. ARIMA, Prophet, o incluso un modelo lineal si los datos son muy b谩sicos) implementado con librer铆as como `scikit-learn` o `statsmodels`.

3.  **An谩lisis de Tendencias y Reabastecimiento 脫ptimo:**
    *   La IA debe ser capaz de identificar productos con alta rotaci贸n o tendencias crecientes/decrecientes en las ventas.
    *   Basado en la predicci贸n de demanda y el stock actual, la IA deber铆a sugerir cu谩ndo y cu谩nto reabastecer cada producto para evitar quiebres de stock o exceso de inventario.

4.  **Panel de Control Interactivo (Dashboard):**
    *   Crear una peque帽a aplicaci贸n web o un script utilizando una librer铆a de visualizaci贸n de datos (ej. `Plotly Dash` o incluso `Django Charts`) para mostrar:
        *   Stock actual de todos los productos.
        *   Predicci贸n de demanda para los pr贸ximos per铆odos.
        *   Productos con bajo stock o sugerencias de reabastecimiento.
        *   Tendencias de ventas por producto.

5.  **`consultar_inventario.py` (Actualizado):**
    *   Este script ahora interactuar谩 con la API RESTful de Django.
    *   Adem谩s de consultar productos disponibles, el script deber铆a permitir:
        *   Consultar la predicci贸n de demanda para un producto espec铆fico.
        *   Preguntar a la IA sobre sugerencias de reabastecimiento.
        *   Listar productos con baja rotaci贸n.

### Herramientas Sugeridas (Adem谩s de Django y SQLite)

*   **Django REST Framework (DRF):** Para construir la API RESTful de manera eficiente.
*   **Pandas y NumPy:** Para manipulaci贸n y an谩lisis de datos en Python, especialmente para la preparaci贸n de datos para los modelos de ML.
*   **Scikit-learn / Statsmodels / Prophet:** Para implementar los modelos de predicci贸n de demanda.
*   **Plotly Dash (o similar):** Para crear el dashboard interactivo de visualizaci贸n de datos. Esto a帽adir铆a un componente de front-end ligero sin la complejidad de un framework JS completo, integr谩ndose bien con Python.
