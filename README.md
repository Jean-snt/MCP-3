# 🚀 SmartStock Pro - Sistema de Inventario IA de Nueva Generación

## 💎 Descripción

**SmartStock Pro** es una plataforma de gestión de inventario de próxima generación con un diseño moderno oscuro y capacidades de Inteligencia Artificial avanzadas. Desarrollada con Django y tecnologías de IA, ofrece:

- 🧠 **Motor de IA Predictivo** - Análisis de demanda con Machine Learning avanzado
- ⚡ **Interfaz Ultra-Moderna** - Tema oscuro con animaciones fluidas y diseño responsivo
- 📊 **Dashboard en Tiempo Real** - Visualización instantánea de métricas clave
- 🤖 **Asistente Virtual Inteligente** - Consultas en lenguaje natural con Vertex AI
- 🎯 **Sistema de Alertas Proactivo** - Notificaciones automáticas inteligentes
- 📈 **Analíticas Avanzadas** - Patrones de ventas y predicciones de tendencias

## ✨ Características Principales

### 🎨 Diseño e Interfaz de Usuario
- **Tema Oscuro Moderno** - Paleta de colores Cyan/Orange/Purple con efectos de luminiscencia
- **Sidebar de Navegación** - Menú lateral fijo con animaciones suaves
- **Cards Interactivas** - Efectos hover con transformaciones 3D
- **Responsive Design** - Adaptable a todos los dispositivos
- **Animaciones Fluidas** - Transiciones suaves en todos los componentes
- **Google Fonts Poppins** - Tipografía moderna y legible

### 🧠 Inteligencia Artificial Avanzada
- **Predicción de Demanda ML** - Algoritmos de Scikit-learn para forecasting
- **Análisis de Tendencias** - Detección de patrones en datos históricos
- **Asistente Virtual** - Chatbot con Vertex AI (Gemini) para consultas naturales
- **Sugerencias Automáticas** - Recomendaciones de reabastecimiento inteligentes
- **Alertas Predictivas** - Sistema proactivo de notificaciones

### 📊 Centro de Control y Analíticas
- **Panel en Tiempo Real** - Métricas instantáneas de inventario
- **Visualización de Datos** - Gráficos interactivos y tablas modernas
- **KPIs Dinámicos** - Indicadores clave de rendimiento actualizados
- **Reportes Personalizables** - Análisis detallados por períodos
- **Top Productos** - Rankings de ventas y rotación

### 🛠️ Gestión Completa de Inventario
- **CRUD Avanzado** - Gestión completa de productos, proveedores y categorías
- **Control de Stock** - Niveles mínimos/máximos con alertas automáticas
- **Historial de Ventas** - Registro detallado de todas las transacciones
- **Órdenes de Compra** - Sistema completo de gestión de pedidos
- **Gestión de Promociones** - Control de descuentos y ofertas

## 🛠️ Stack Tecnológico

### 🎨 Frontend
- **HTML5, CSS3 Avanzado** - Diseño moderno con CSS Grid y Flexbox
- **JavaScript ES6+** - Interactividad y animaciones
- **Bootstrap 5** - Sistema de grillas responsivo
- **Font Awesome 6** - Biblioteca de iconos
- **Google Fonts (Poppins)** - Tipografía premium
- **CSS Custom Properties** - Variables para theming dinámico

### ⚙️ Backend
- **Python 3.10+** - Lenguaje de programación principal
- **Django 5.2** - Framework web full-stack
- **SQLite** - Base de datos (PostgreSQL/MySQL para producción)
- **Django ORM** - Mapeo objeto-relacional avanzado
- **Django Templates** - Motor de plantillas

### 🤖 Inteligencia Artificial
- **Google Vertex AI** - API de Gemini para procesamiento de lenguaje natural
- **Scikit-learn** - Machine Learning (regresión, clasificación)
- **Pandas & NumPy** - Procesamiento y análisis de datos
- **TensorFlow** (opcional) - Deep Learning para predicciones avanzadas

### 📊 Visualización y Datos
- **Plotly** - Gráficos interactivos
- **Chart.js** (opcional) - Visualizaciones ligeras
- **Pandas** - Manipulación de datos
- **JSON** - Formato de intercambio de datos

## 📁 Arquitectura del Proyecto

```
MCP-3/
├── 📂 productos/                        # 🎯 App principal Django
│   ├── 📄 models.py                    # Modelos: Product, Sale, Supplier, Category, Alert
│   ├── 📄 views.py                     # Vistas principales y lógica de negocio
│   ├── 📄 advanced_views.py            # Vistas de analíticas y predicciones
│   ├── 📄 ml_services.py               # 🤖 Servicios de Machine Learning
│   ├── 📄 admin.py                     # Panel de administración Django
│   ├── 📄 urls.py                      # Rutas de la aplicación
│   └── 📂 management/commands/         # Comandos personalizados
│       └── limpiar_datos.py            # Utilidad de limpieza
│
├── 📂 config/                           # ⚙️ Configuración del proyecto
│   ├── 📄 settings.py                  # Configuración Django
│   ├── 📄 urls.py                      # URLs principales
│   ├── 📄 wsgi.py                      # WSGI para producción
│   └── 📄 asgi.py                      # ASGI para async
│
├── 📂 templates/                        # 🎨 Plantillas HTML
│   ├── 📄 base.html                    # ⭐ Plantilla base (Tema Oscuro Moderno)
│   └── 📂 inventario/
│       ├── 📄 inicio.html              # Centro de Comando
│       ├── 📄 dashboard.html           # Panel de Control
│       ├── 📄 predictions.html         # Predicciones IA
│       ├── 📄 analytics.html           # Analíticas Avanzadas
│       ├── 📄 lista_productos.html     # Catálogo de Productos
│       ├── 📄 consultar_ia.html        # Asistente Virtual
│       └── 📄 alerts.html              # Sistema de Alertas
│
├── 📂 modelos_ia/                       # 🧠 Modelos ML entrenados
├── 📂 static/                           # 🎨 Archivos estáticos (CSS, JS, imágenes)
├── 📄 manage.py                        # Django management
├── 📄 db.sqlite3                       # Base de datos SQLite
├── 📄 requirements.txt                 # Dependencias Python
├── 📄 README.md                        # Documentación
├── 📄 inventario_cli.py                # CLI de gestión
└── 📄 inventario_ia.py                 # CLI con asistente IA
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

### 🌐 Interfaz Web (SmartStock Pro)

Inicia el servidor de desarrollo:

```bash
python manage.py runserver
```

Accede a la aplicación: **http://127.0.0.1:8000**

#### 📍 Módulos Disponibles:

| Módulo | URL | Descripción |
|--------|-----|-------------|
| 🏠 **Centro de Comando** | `/` | Dashboard principal con estadísticas en tiempo real |
| 📊 **Panel de Control** | `/dashboard/` | Métricas avanzadas y visualizaciones |
| 📦 **Catálogo** | `/productos/` | Gestión completa de productos |
| 🧠 **Predicciones IA** | `/predictions/` | Forecasting y análisis predictivo |
| 📈 **Analíticas** | `/analytics/` | Tendencias y patrones de ventas |
| 💬 **Asistente IA** | `/consultar-ia/` | Chatbot con procesamiento de lenguaje natural |
| 🔔 **Alertas** | `/alerts/` | Sistema de notificaciones inteligentes |

### 🎨 Características Visuales

- ✨ **Animaciones Suaves**: Transiciones fluidas en hover y click
- 🌈 **Paleta de Colores**: Cyan (#00d4ff), Orange (#ff6b35), Purple (#b794f6)
- 🎯 **Sidebar Fija**: Navegación lateral siempre visible
- 📱 **100% Responsive**: Adaptable a móviles, tablets y desktop
- 🌙 **Tema Oscuro**: Reducción de fatiga visual para uso prolongado

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
