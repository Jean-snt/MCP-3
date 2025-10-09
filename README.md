# 🤖 Inventario Inteligente Colaborativo con Predicción y Análisis de Tendencias

Un sistema avanzado de gestión de inventario que utiliza Inteligencia Artificial para predecir demanda, analizar tendencias y sugerir acciones de reabastecimiento optimizadas.

## ✨ Características Principales

- **Gestión Completa de Inventario**: CRUD completo para productos, proveedores y ventas
- **API RESTful**: Endpoints para integración con aplicaciones externas
- **Predicción de Demanda con IA**: Modelos de Machine Learning para prever demanda futura
- **Análisis de Tendencias**: Identificación de patrones de venta y rotación de productos
- **Sugerencias Inteligentes**: IA que propone cuándo y cuánto reabastecer
- **Dashboard Interactivo**: Visualización en tiempo real de métricas clave
- **CLI Avanzado**: Interfaz de línea de comandos con análisis de IA

## 🛠️ Tecnologías Utilizadas

- **Backend**: Python 3.x, Django 5.0.6
- **Base de Datos**: SQLite (configurable para PostgreSQL/MySQL)
- **API**: Django REST Framework
- **IA/ML**: Pandas, NumPy, Scikit-learn
- **Visualización**: Plotly Dash, Matplotlib, Seaborn
- **IA Generativa**: Google Gemini AI

## 📋 Requisitos del Sistema

- Python 3.8+
- pip (gestor de paquetes de Python)
- Git (opcional, para clonar el repositorio)

## 🚀 Instalación y Configuración

### 1. Clonar el Repositorio
```bash
git clone <repository-url>
cd joelpc03/MCP-3
```

### 2. Crear Entorno Virtual
```bash
python -m venv venv
# En Windows:
venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate
```

### 3. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar Variables de Entorno
Crear un archivo `.env` en la raíz del proyecto:
```env
DJANGO_SECRET_KEY=tu-clave-secreta-aqui
GEMINI_API_KEY=tu-api-key-de-google-gemini
```

### 5. Configurar Base de Datos
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Crear Datos de Ejemplo
```bash
python seed_data.py
```

### 7. Crear Superusuario (Opcional)
```bash
python manage.py createsuperuser
```

## 🎯 Uso del Sistema

### Servidor Django (Backend + API)
```bash
python manage.py runserver
```
- **Admin Panel**: http://localhost:8000/admin/
- **API**: http://localhost:8000/api/

### Dashboard Interactivo
```bash
python dashboard_app.py
```
- **Dashboard**: http://localhost:8050

### CLI Inteligente
```bash
# Modo básico
python consultar_inventario.py

# Modo interactivo
python consultar_inventario.py --interactive
```

## 📊 API Endpoints

### Productos
- `GET /api/productos/` - Listar productos
- `POST /api/productos/` - Crear producto
- `GET /api/productos/{id}/` - Obtener producto
- `PUT /api/productos/{id}/` - Actualizar producto
- `DELETE /api/productos/{id}/` - Eliminar producto
- `GET /api/productos/bajo_stock/` - Productos bajo stock
- `POST /api/productos/{id}/registrar_venta/` - Registrar venta
- `POST /api/productos/{id}/ajustar_stock/` - Ajustar stock

### Análisis
- `GET /api/analisis/dashboard/` - Datos del dashboard
- `GET /api/analisis/prediccion_demanda/` - Predicción de demanda
- `GET /api/analisis/tendencias/` - Análisis de tendencias
- `GET /api/analisis/sugerencias_reabastecimiento/` - Sugerencias IA

## 🤖 Funcionalidades de IA

### Predicción de Demanda
- Utiliza regresión lineal para predecir ventas futuras
- Analiza patrones históricos de 90 días
- Calcula nivel de confianza basado en variabilidad de datos

### Análisis de Tendencias
- Identifica productos con alta/baja rotación
- Analiza patrones por categoría y día de la semana
- Detecta estacionalidad en las ventas

### Sugerencias de Reabastecimiento
- Calcula demanda diaria promedio
- Estima días restantes de stock
- Sugiere cantidades óptimas de reabastecimiento
- Clasifica urgencia (CRÍTICA, ALTA, MEDIA)

## 📈 Dashboard Interactivo

El dashboard incluye:
- **Métricas Principales**: Total productos, bajo stock, ventas, ingresos
- **Gráficos de Ventas**: Tendencias diarias y productos populares
- **Análisis de Tendencias**: Patrones por día de la semana
- **Tabla de Sugerencias**: Reabastecimiento inteligente con colores de urgencia
- **Actualización Automática**: Datos en tiempo real cada 30 segundos

## 💻 CLI Avanzado

### Modo Interactivo
```bash
python consultar_inventario.py --interactive
```

Opciones disponibles:
1. **Consultar inventario básico** - Lista productos disponibles
2. **Análisis de tendencias** - Productos con mayor/menor rotación
3. **Predicción de demanda** - Análisis específico por producto
4. **Sugerencias de reabastecimiento** - Recomendaciones IA
5. **Dashboard ejecutivo** - Resumen estadístico completo

### Ejemplos de Uso

#### Consulta Básica
```bash
python consultar_inventario.py
```

#### Análisis de Producto Específico
```bash
python consultar_inventario.py --interactive
# Seleccionar opción 3 y proporcionar ID del producto
```

## 🔧 Configuración Avanzada

### Base de Datos PostgreSQL
```python
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'inventario_db',
        'USER': 'tu_usuario',
        'PASSWORD': 'tu_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Configuración de Producción
```python
# settings.py
DEBUG = False
ALLOWED_HOSTS = ['tu-dominio.com']
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = ['https://tu-dominio.com']
```

## 📊 Modelos de Datos

### Producto
- Información básica (nombre, descripción, categoría)
- Gestión de stock (cantidad, cantidad mínima)
- Precios (compra, venta, margen de ganancia)
- Relación con proveedor
- Código de barras y ubicación

### Venta
- Registro de transacciones
- Cantidad vendida y precio unitario
- Información del cliente
- Fecha y notas

### MovimientoInventario
- Historial de entradas y salidas
- Tipos de movimiento (entrada, salida, ajuste)
- Motivo y usuario responsable

## 🧪 Testing y Desarrollo

### Ejecutar Tests
```bash
python manage.py test
```

### Crear Datos de Prueba
```bash
python seed_data.py
```

### Acceder al Admin
```bash
python manage.py runserver
# Ir a http://localhost:8000/admin/
```

## 📚 Documentación de la API

### Autenticación
Actualmente el sistema no requiere autenticación para desarrollo. Para producción, implementar:
- JWT tokens
- API keys
- OAuth2

### Formato de Respuesta
```json
{
    "count": 25,
    "next": "http://localhost:8000/api/productos/?page=2",
    "previous": null,
    "results": [...]
}
```

### Códigos de Estado
- `200` - OK
- `201` - Creado
- `400` - Bad Request
- `404` - No encontrado
- `500` - Error interno

## 🚨 Solución de Problemas

### Error de Conexión a la API
```bash
# Verificar que Django esté ejecutándose
python manage.py runserver

# Verificar puerto
curl http://localhost:8000/api/
```

### Error de Gemini AI
```bash
# Verificar API key en .env
echo $GEMINI_API_KEY

# Verificar conexión
python -c "import google.generativeai as genai; print('OK')"
```

### Error de Dashboard
```bash
# Verificar dependencias
pip install dash plotly

# Verificar puerto 8050
netstat -an | grep 8050
```

## 🤝 Contribución

1. Fork el proyecto
2. Crear rama para feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

## 👥 Autores

- **Desarrollador Principal**: [Tu Nombre]
- **IA/ML**: Google Gemini AI
- **Framework**: Django REST Framework
- **Visualización**: Plotly Dash

## 🙏 Agradecimientos

- Django Community
- Google Gemini AI
- Plotly Team
- Scikit-learn Contributors

---

## 📞 Soporte

Para soporte técnico o preguntas:
- 📧 Email: soporte@inventario-inteligente.com
- 📱 Teléfono: +1-555-INVENTARIO
- 🌐 Web: https://inventario-inteligente.com

**¡Gracias por usar Inventario Inteligente! 🚀**