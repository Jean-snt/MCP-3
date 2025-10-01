# 🤖 Sistema de Inventario con IA

Un sistema inteligente de gestión de inventario que utiliza **Vertex AI (Google Gemini)** para interpretar comandos en lenguaje natural y realizar operaciones de inventario de forma conversacional.

## ✨ Características

- **🧠 IA Conversacional**: Habla con la IA como si fuera un asistente personal
- **📦 Gestión Completa de Inventario**: Agregar, eliminar, actualizar y consultar productos
- **🎯 Comandos Naturales**: Usa lenguaje natural para todas las operaciones
- **📱 Interfaz Web Moderna**: Diseño responsive con Bootstrap
- **⚡ Formularios Dinámicos**: La IA te ayuda a completar información faltante

## 🚀 Instalación y Configuración

### 1. Clonar el Proyecto
```bash
git clone <url-del-repositorio>
cd MCP_2
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

### 4. Configurar Base de Datos
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Crear Datos de Ejemplo (Opcional)
```bash
python crear_datos_ejemplo.py
```

### 6. Ejecutar el Servidor
```bash
python manage.py runserver
```

Visita: http://127.0.0.1:8000

## 🎯 Cómo Usar el Sistema

### Comandos Básicos de Inventario:
- **"muestra todo mi inventario"** - Ver todos los productos
- **"qué productos están disponibles"** - Ver productos con stock
- **"añade 10 laptops"** - Agregar productos
- **"elimina el teclado"** - Eliminar productos
- **"actualiza el mouse a 15 unidades"** - Actualizar cantidades
- **"muestra información del monitor"** - Ver detalles de un producto

### Preguntas Generales:
- **"¿cómo funciona esto?"** - Explicación del sistema
- **"¿qué es la inteligencia artificial?"** - Preguntas generales
- **"¿cómo estás?"** - Conversación casual

### Salir del Sistema:
- **"quiero salir"** o **"adiós"**

## 🛠️ Estructura del Proyecto

```
MCP_2/
├── inventario/              # App principal
│   ├── models.py           # Modelo de Producto
│   ├── views.py            # Lógica de la IA y vistas
│   ├── urls.py             # URLs de la app
│   └── admin.py            # Configuración del admin
├── inventario_proj/        # Configuración del proyecto
│   ├── settings.py         # Configuración Django
│   └── urls.py             # URLs principales
├── templates/              # Plantillas HTML
│   ├── base.html           # Plantilla base
│   └── inventario/         # Plantillas de la app
├── static/                 # Archivos estáticos (CSS, JS)
├── requirements.txt        # Dependencias Python
├── manage.py              # Script de gestión Django
└── crear_datos_ejemplo.py # Script para datos de prueba
```

## 🧠 Tecnologías Utilizadas

- **Backend**: Django 5.2.6
- **IA**: Google Vertex AI (Gemini)
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Base de Datos**: SQLite
- **Iconos**: Font Awesome

## 📋 Modelo de Datos

### Producto
- `name`: Nombre del producto
- `description`: Descripción detallada
- `quantity`: Cantidad en stock
- `created_at`: Fecha de creación
- `updated_at`: Fecha de última actualización

## 🔧 Configuración de Vertex AI

El sistema utiliza Vertex AI de Google. Para configurarlo:

1. **Proyecto Google Cloud**: `stone-poetry-473315-a9`
2. **Ubicación**: `us-central1`
3. **Autenticación**: Se maneja automáticamente con las credenciales del sistema

## 🎨 Características de la Interfaz

- **Diseño Responsive**: Funciona en desktop, tablet y móvil
- **Tema Moderno**: Colores azul y púrpura con gradientes
- **Interacción Fluida**: Respuestas en tiempo real
- **Formularios Inteligentes**: La IA genera formularios dinámicos cuando necesita más información

## 🚀 Funcionalidades Avanzadas

### IA Conversacional
- Responde preguntas generales de forma inteligente
- Mantiene contexto sobre el inventario
- Proporciona ayuda y explicaciones

### Gestión Inteligente
- Detecta automáticamente qué acción quieres realizar
- Completa información faltante con formularios dinámicos
- Valida datos antes de realizar operaciones

### Interfaz Adaptativa
- Formularios que aparecen solo cuando son necesarios
- Mensajes de confirmación y error claros
- Navegación intuitiva

## 📝 Ejemplos de Uso

### Agregar Producto
```
Usuario: "quiero agregar un nuevo producto"
IA: Te ayudo a agregar un producto. ¿Cuál es el nombre del producto?
Usuario: "Laptop Gaming"
IA: Perfecto. ¿Cuántas unidades quieres agregar?
Usuario: "5"
IA: ✅ Producto "Laptop Gaming" agregado exitosamente con 5 unidades.
```

### Consultar Inventario
```
Usuario: "muestra todo mi inventario"
IA: 📦 **Tu Inventario Completo:**
    • Laptop Gaming - 5 unidades
    • Teclado Mecánico - 12 unidades
    • Mouse Inalámbrico - 8 unidades
    Total: 3 productos
```

### Pregunta General
```
Usuario: "¿qué es la inteligencia artificial?"
IA: 🤖 La inteligencia artificial (IA) es una tecnología que permite a las máquinas...
    [Respuesta completa sobre IA]
    
    Por cierto, si necesitas ayuda con tu inventario, solo pregúntame! 😊
```

## 🆘 Solución de Problemas

### Error de Migraciones
```bash
python manage.py makemigrations inventario
python manage.py migrate
```

### Error de Dependencias
```bash
pip install --upgrade -r requirements.txt
```

### Error de Vertex AI
- Verificar conexión a internet
- Comprobar configuración del proyecto Google Cloud

## 📞 Soporte

Si tienes problemas o preguntas:
1. Revisa la sección de solución de problemas
2. Verifica que todas las dependencias estén instaladas
3. Comprueba la configuración de Vertex AI

---

**¡Disfruta usando tu sistema de inventario inteligente!** 🎉