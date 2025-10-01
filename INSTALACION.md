# 🚀 Guía de Instalación Rápida

## Requisitos Previos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

## ⚡ Instalación en 5 Pasos

### 1. Clonar el Proyecto
```bash
git clone <url-del-repositorio>
cd MCP_2
```

### 2. Crear Entorno Virtual
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
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

### 5. Ejecutar el Servidor
```bash
python manage.py runserver
```

**¡Listo!** Visita: http://127.0.0.1:8000

## 🎯 Datos de Prueba (Opcional)

Si quieres probar el sistema con datos de ejemplo:

```bash
python crear_datos_ejemplo.py
```

## 🔧 Verificación de Instalación

Para verificar que todo está funcionando correctamente:

```bash
# Verificar Django
python -c "import django; print('Django:', django.get_version())"

# Verificar Vertex AI
python -c "import vertexai; print('Vertex AI: OK')"

# Verificar que el servidor inicia
python manage.py check
```

## ❗ Solución de Problemas Comunes

### Error: "No module named 'vertexai'"
```bash
pip install --upgrade google-cloud-aiplatform
```

### Error: "No module named 'django'"
```bash
pip install Django==5.2.6
```

### Error de Migraciones
```bash
python manage.py makemigrations inventario
python manage.py migrate
```

### Error de Permisos (Windows)
Ejecutar PowerShell como Administrador y repetir los pasos.

---

**¡El sistema está listo para usar!** 🎉
