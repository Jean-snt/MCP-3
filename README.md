# 🤖 Sistema de Inventario Inteligente con IA

## 📋 Descripción

Este proyecto implementa un **Sistema de Inventario Inteligente Colaborativo con Predicción y Análisis de Tendencias** que utiliza Inteligencia Artificial (Vertex AI/Gemini) para:

- 🔮 **Predecir la demanda** de productos usando Machine Learning
- 💡 **Sugerir acciones de reabastecimiento** automáticamente
- 📊 **Analizar tendencias** de ventas y comportamiento del mercado
- 🚨 **Generar alertas** inteligentes de inventario
- 💬 **Responder consultas** en lenguaje natural sobre el inventario
- 📈 **Visualizar datos** en tiempo real con dashboards interactivos

## ✨ Características Principales

### 🎯 Gestión de Inventario Avanzada
- **CRUD completo** de productos, proveedores y categorías
- **Historial de ventas** detallado para análisis
- **Órdenes de compra** con seguimiento de estado
- **Alertas automáticas** de inventario

### 🤖 Inteligencia Artificial Integrada
- **Predicción de demanda** usando Machine Learning (Scikit-learn)
- **Análisis de tendencias** con algoritmos de regresión
- **Consultas en lenguaje natural** con Vertex AI (Gemini)
- **Sugerencias inteligentes** de reabastecimiento

### 📊 Visualización y Dashboard
- **Dashboard web** con métricas en tiempo real
- **Gráficos interactivos** con Plotly y Dash
- **Análisis visual** de tendencias y patrones
- **Reportes automáticos** de estado del inventario

### 🖥️ Múltiples Interfaces
- **Interfaz web** Django con diseño moderno
- **CLI inteligente** para consultas desde terminal
- **Dashboard interactivo** con visualizaciones
- **APIs simples** para integración externa

## 🛠️ Tecnologías Utilizadas

### Backend
- **Python 3.10+** - Lenguaje principal
- **Django 5.2** - Framework web
- **SQLite** - Base de datos (configurable para PostgreSQL/MySQL)

### Inteligencia Artificial
- **Google Vertex AI** - Modelo Gemini para consultas naturales
- **Scikit-learn** - Machine Learning para predicciones
- **Pandas & NumPy** - Análisis de datos

### Visualización
- **Plotly** - Gráficos interactivos
- **Dash** - Dashboard web
- **Bootstrap** - Diseño responsive

### Frontend
- **HTML5, CSS3, JavaScript** - Interfaz web
- **Bootstrap 5** - Framework CSS
- **Font Awesome** - Iconos

## 📁 Estructura del Proyecto

```
MCP_2/
├── inventario/                    # App principal de Django
│   ├── models.py                 # Modelos de datos avanzados
│   ├── views.py                  # Vistas web básicas
│   ├── advanced_views.py         # Vistas avanzadas
│   ├── ml_services.py            # Servicios de Machine Learning
│   ├── admin.py                  # Configuración del admin
│   └── urls.py                   # URLs del sistema
├── inventario_proj/              # Configuración del proyecto
│   ├── settings.py               # Configuración Django
│   └── urls.py                   # URLs principales
├── templates/                    # Plantillas HTML
│   ├── base.html                 # Plantilla base
│   ├── inventario/
│   │   ├── dashboard.html        # Dashboard principal
│   │   ├── predictions.html      # Predicciones IA
│   │   └── ...
├── smart_cli.py                  # CLI inteligente
├── dashboard_interactivo.py      # Dashboard con Dash
├── crear_datos_completos.py      # Script de datos de ejemplo
├── consultar_inventario.py       # Script original de IA
└── requirements.txt              # Dependencias
```

## 🚀 Instalación y Configuración

### 1. Clonar el Repositorio
```bash
git clone https://github.com/CesarMartel/MCP_2.git
cd MCP_2
```

### 2. Crear Entorno Virtual
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
```

### 3. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar Vertex AI
1. Crear proyecto en [Google Cloud Console](https://console.cloud.google.com/)
2. Habilitar Vertex AI API
3. Crear credenciales de servicio
4. Descargar archivo JSON de credenciales
5. Configurar variable de entorno:
```bash
set GOOGLE_APPLICATION_CREDENTIALS=path/to/credentials.json
```

### 5. Configurar Base de Datos
```bash
python manage.py migrate
```

### 6. Crear Datos de Ejemplo
```bash
python crear_datos_completos.py
```

## 🎮 Uso del Sistema

### 🌐 Interfaz Web
```bash
python manage.py runserver
```
Acceder a: http://127.0.0.1:8000

#### Páginas Disponibles:
- **Inicio**: http://127.0.0.1:8000/
- **Dashboard**: http://127.0.0.1:8000/dashboard/
- **Predicciones**: http://127.0.0.1:8000/predictions/
- **Análisis**: http://127.0.0.1:8000/analytics/
- **Alertas**: http://127.0.0.1:8000/alerts/
- **Consultar IA**: http://127.0.0.1:8000/consultar-ia/

### 🖥️ CLI Inteligente
```bash
python smart_cli.py
```

#### Comandos Disponibles:
- `1` - Ver métricas principales
- `2` - Productos con stock bajo
- `3` - Sugerencias de reabastecimiento
- `4` - Predicciones de demanda
- `5` - Ver alertas activas
- `6` - Entrenar modelos de ML
- `7` - Generar alertas
- `8` - Consultar a la IA

#### Ejemplos de Consultas a la IA:
- "¿Qué productos necesitan reabastecimiento?"
- "Muéstrame las tendencias de ventas"
- "¿Cuál es el estado general del inventario?"
- "¿Qué productos tienen mejor rendimiento?"

### 📊 Dashboard Interactivo
```bash
python dashboard_interactivo.py
```
Acceder a: http://127.0.0.1:8050

## 🔧 Funcionalidades Avanzadas

### 🤖 Machine Learning
El sistema incluye servicios de ML para:

- **Predicción de Demanda**: Modelos de regresión lineal para predecir ventas futuras
- **Análisis de Tendencias**: Identificación de patrones en datos históricos
- **Sugerencias de Reabastecimiento**: Algoritmos para optimizar niveles de stock

### 📈 Análisis de Datos
- **Métricas en tiempo real** del inventario
- **Análisis de ventas** por período y categoría
- **Identificación de productos** con alta/baja rotación
- **Alertas automáticas** basadas en umbrales configurables

### 💬 IA Conversacional
- **Consultas en lenguaje natural** sobre el inventario
- **Interpretación inteligente** de solicitudes
- **Respuestas contextuales** basadas en datos actuales
- **Sugerencias proactivas** de acciones

## 📊 Modelos de Datos

### Product
```python
- name: Nombre del producto
- sku: Código único
- category: Categoría del producto
- supplier: Proveedor
- quantity: Cantidad en stock
- min_stock_level: Nivel mínimo
- max_stock_level: Nivel máximo
- cost_price: Precio de costo
- selling_price: Precio de venta
- predicted_demand_7d: Demanda predicha 7 días
- predicted_demand_30d: Demanda predicha 30 días
- reorder_suggestion: Sugerencia de reorden
```

### Sale
```python
- product: Producto vendido
- quantity_sold: Cantidad vendida
- unit_price: Precio unitario
- total_amount: Monto total
- sale_date: Fecha de venta
- customer_name: Nombre del cliente
```

### InventoryAlert
```python
- product: Producto relacionado
- alert_type: Tipo de alerta
- message: Mensaje descriptivo
- is_resolved: Estado de resolución
- created_at: Fecha de creación
```

## 🎯 Casos de Uso

### 1. Gestión de Inventario
- Agregar/editar/eliminar productos
- Configurar niveles de stock
- Gestionar proveedores y categorías
- Registrar ventas y órdenes de compra

### 2. Análisis Predictivo
- Predecir demanda futura
- Identificar productos con riesgo de stockout
- Optimizar niveles de reabastecimiento
- Analizar tendencias de mercado

### 3. Monitoreo Inteligente
- Alertas automáticas de stock bajo
- Notificaciones de productos sin stock
- Reportes de productos con alta rotación
- Seguimiento de métricas clave

### 4. Consultas Inteligentes
- "¿Cuántas unidades de iPhone tenemos?"
- "¿Qué productos necesitan reabastecimiento urgente?"
- "Muéstrame las ventas del último mes"
- "¿Cuál es el margen de ganancia promedio?"

## 🔒 Seguridad y Configuración

### Variables de Entorno
```bash
# Google Cloud
GOOGLE_APPLICATION_CREDENTIALS=path/to/credentials.json

# Django
SECRET_KEY=your-secret-key
DEBUG=False  # En producción
```

### Base de Datos
- **Desarrollo**: SQLite (incluida)
- **Producción**: PostgreSQL o MySQL recomendado

## 📈 Rendimiento

### Optimizaciones Implementadas
- **Caché de modelos** ML para predicciones rápidas
- **Consultas optimizadas** con select_related y prefetch_related
- **Paginación** en listas grandes
- **Índices de base de datos** en campos críticos

### Escalabilidad
- **Arquitectura modular** para fácil extensión
- **APIs RESTful** para integración externa
- **Separación de servicios** ML y web
- **Configuración flexible** para diferentes entornos

## 🤝 Contribución

### Cómo Contribuir
1. Fork del repositorio
2. Crear rama de feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit de cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

### Estándares de Código
- **PEP 8** para Python
- **Docstrings** en todas las funciones
- **Tests unitarios** para nuevas funcionalidades
- **Documentación** actualizada

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 👥 Autores

- **César Martel** - Desarrollo principal
- **Josué Ochoa** - Contribuciones y testing

## 🙏 Agradecimientos

- **Google Cloud** por Vertex AI
- **Django** por el framework web
- **Plotly** por las visualizaciones
- **Scikit-learn** por las herramientas de ML

## 📞 Soporte

Para soporte técnico o preguntas:
- **Email**: cesar.martel@ejemplo.com
- **Issues**: [GitHub Issues](https://github.com/CesarMartel/MCP_2/issues)
- **Documentación**: [Wiki del proyecto](https://github.com/CesarMartel/MCP_2/wiki)

---

## 🚀 Próximas Funcionalidades

- [ ] **Integración con APIs externas** (e-commerce, ERP)
- [ ] **Análisis de sentimiento** en reseñas de productos
- [ ] **Optimización de rutas** de entrega
- [ ] **Predicción de precios** dinámicos
- [ ] **Análisis de competencia** automático
- [ ] **Reportes PDF** automatizados
- [ ] **Notificaciones push** móviles
- [ ] **Integración con IoT** para tracking automático

¡El sistema está listo para usar y seguir evolucionando! 🎉
