🚀 Ejercicio #3: Inventario Inteligente Colaborativo con Predicción y Análisis de Tendencias
Este proyecto expande el sistema de inventario backend de Python y Django del Ejercicio #2, elevándolo a un nivel intermedio-avanzado. El objetivo es desarrollar una plataforma más robusta y colaborativa, añadiendo funcionalidades de predicción de demanda, análisis de tendencias y una interfaz de usuario interactiva para la visualización de datos.
📋 El Desafío
Desarrollar un sistema de inventario inteligente que no solo gestione el catálogo de productos, sino que también utilice la Inteligencia Artificial para predecir la demanda y sugerir acciones de reabastecimiento, todo ello accesible a través de una API RESTful y un panel de control interactivo.
✨ Características Principales
Gestión de Inventario: CRUD completo de productos y proveedores.
Historial de Ventas: Registro detallado de cada venta para análisis y predicción.
API RESTful: Los puntos finales para interactuar p
Predicción de Demanda (IA): Modelos de Machine Learning para prever la demanda futura de productos.
Análisis de Tendencias: Identificación de productos con alta/baja rotación y patrones de venta.
Sugerencias de Reabastecimiento: La IA propone cuándo y cuánto reabastecer para optimizar el stock.
Panel de Control: Interfaz web interactiva para visualizar métricas clave del inventario.
Interfaz de Línea de Comandos (CLI): Script para interactuar directamente con el sistema de inventario y la IA.
🎯 Entregables y Resultado Esperado
El proyecto consta de los siguientes componentes principales:
Proyecto Django Completo: smart_inventory_project/
Modelos de datos para productos, proveedores y ventas.
API RESTful para todas las operaciones de inventario.
Lógica de IA integrada para predicción y análisis.
Script de Interacción CLI: consultar_inventario.py
Permite consultar el estado del inventario, realizar predicciones y obtener sugerencias de la IA desde la terminal.
Aplicación Dashboard Interactivo: 'dashbodashboard_app.py
Una aplicación web separada construida con Dash/Plotly para visualizar métricas en tiempo real.
🛠️ Tecnologías Utilizadas
Backend: Python 3.x, Django
Base de Datos: SQLite (por defecto, configurable para PostgreSQL/MySQL)
API: Marco REST de Django
Inteligencia Artificial/Machine Learning: Pandas, NumPy, Scikit-learn (para modelos de regresión lineal básicos, extensible a Statsmodels, Prophet para series de tiempo más avanzadas)
Visualización/Dashboard: Guión de la trama
Interacción API: Solicitudes (para el CLI y el Dashboard)
📂 Estructura del Proyecto
code
Código
smart_inventory_project/
├── smart_inventory_project/      # Configuración principal de Django
│   ├── settings.py
│   ├── urls.py
│   └── ...
├── inventory/                    # Aplicación Django del inventario
│   ├── migrations/
│   ├── admin.py
│   ├── models.py                 # Modelos de Product, Sale, Supplier
│   ├── serializers.py            # Serializadores para la API REST
│   ├── views.py                  # Vistas de la API RESTful
│   ├── urls.py                   # URLs específicas de la API del inventario
│   └── ai_logic.py               # Lógica de la IA (predicción, sugerencias)
├── populate_db.py                # Script para cargar datos de ejemplo
├── consultar_inventario.py       # Script CLI para interactuar con el sistema
├── dashboard_app.py              # Aplicación web interactiva (Plotly Dash)
├── manage.py
└── requirements.txt              # Dependencias del proyecto
