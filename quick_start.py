#!/usr/bin/env python3
"""
Script de inicio rápido para el Sistema de Inventario Inteligente
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def print_banner():
    """Mostrar banner de inicio"""
    print("=" * 60)
    print("🤖 INVENTARIO INTELIGENTE - INICIO RÁPIDO")
    print("=" * 60)
    print("Sistema de gestión de inventario con IA")
    print("Predicción de demanda • Análisis de tendencias • Dashboard interactivo")
    print("=" * 60)

def check_requirements():
    """Verificar requisitos del sistema"""
    print("\n🔍 Verificando requisitos...")
    
    # Verificar Python
    if sys.version_info < (3, 8):
        print("❌ Error: Se requiere Python 3.8 o superior")
        return False
    
    print(f"✅ Python {sys.version.split()[0]}")
    
    # Verificar archivos necesarios
    required_files = [
        "requirements.txt",
        "manage.py",
        "inventario_project/settings.py",
        "productos/models.py"
    ]
    
    for file in required_files:
        if not Path(file).exists():
            print(f"❌ Error: Archivo {file} no encontrado")
            return False
        print(f"✅ {file}")
    
    return True

def install_dependencies():
    """Instalar dependencias"""
    print("\n📦 Instalando dependencias...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True, capture_output=True)
        print("✅ Dependencias instaladas correctamente")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error instalando dependencias: {e}")
        return False

def setup_database():
    """Configurar base de datos"""
    print("\n🗄️ Configurando base de datos...")
    try:
        # Crear migraciones
        subprocess.run([sys.executable, "manage.py", "makemigrations"], 
                      check=True, capture_output=True)
        print("✅ Migraciones creadas")
        
        # Aplicar migraciones
        subprocess.run([sys.executable, "manage.py", "migrate"], 
                      check=True, capture_output=True)
        print("✅ Migraciones aplicadas")
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error configurando base de datos: {e}")
        return False

def create_sample_data():
    """Crear datos de ejemplo"""
    print("\n🌱 Creando datos de ejemplo...")
    try:
        subprocess.run([sys.executable, "seed_data.py"], 
                      check=True, capture_output=True)
        print("✅ Datos de ejemplo creados")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error creando datos de ejemplo: {e}")
        return False

def check_env_file():
    """Verificar archivo .env"""
    print("\n🔐 Verificando configuración...")
    
    if not Path(".env").exists():
        print("⚠️  Archivo .env no encontrado. Creando archivo de ejemplo...")
        env_content = """# Configuración del Sistema de Inventario Inteligente
DJANGO_SECRET_KEY=dev-secret-key-change-in-production
GEMINI_API_KEY=tu-api-key-de-google-gemini-aqui

# Configuración de Base de Datos (opcional)
# DATABASE_URL=postgresql://usuario:password@localhost:5432/inventario_db

# Configuración de Producción (opcional)
# DEBUG=False
# ALLOWED_HOSTS=tu-dominio.com
"""
        with open(".env", "w", encoding="utf-8") as f:
            f.write(env_content)
        print("✅ Archivo .env creado. ¡Recuerda configurar tu GEMINI_API_KEY!")
        return False
    else:
        print("✅ Archivo .env encontrado")
        return True

def show_menu():
    """Mostrar menú de opciones"""
    print("\n" + "=" * 60)
    print("🎯 OPCIONES DISPONIBLES")
    print("=" * 60)
    print("1. 🚀 Iniciar servidor Django (Backend + API)")
    print("2. 📊 Iniciar Dashboard interactivo")
    print("3. 💻 Usar CLI inteligente")
    print("4. 🔧 Ejecutar migraciones")
    print("5. 🌱 Crear datos de ejemplo")
    print("6. 📋 Ver estado del sistema")
    print("7. ❌ Salir")
    print("=" * 60)

def start_django_server():
    """Iniciar servidor Django"""
    print("\n🚀 Iniciando servidor Django...")
    print("📍 Backend: http://localhost:8000")
    print("📍 Admin: http://localhost:8000/admin/")
    print("📍 API: http://localhost:8000/api/")
    print("\n💡 Presiona Ctrl+C para detener el servidor")
    try:
        subprocess.run([sys.executable, "manage.py", "runserver"])
    except KeyboardInterrupt:
        print("\n⏹️  Servidor detenido")

def start_dashboard():
    """Iniciar dashboard interactivo"""
    print("\n📊 Iniciando Dashboard interactivo...")
    print("📍 Dashboard: http://localhost:8050")
    print("\n💡 Presiona Ctrl+C para detener el dashboard")
    try:
        subprocess.run([sys.executable, "dashboard_app.py"])
    except KeyboardInterrupt:
        print("\n⏹️  Dashboard detenido")

def start_cli():
    """Iniciar CLI inteligente"""
    print("\n💻 Iniciando CLI inteligente...")
    try:
        subprocess.run([sys.executable, "consultar_inventario.py", "--interactive"])
    except KeyboardInterrupt:
        print("\n⏹️  CLI detenido")

def run_migrations():
    """Ejecutar migraciones"""
    print("\n🔧 Ejecutando migraciones...")
    try:
        subprocess.run([sys.executable, "manage.py", "makemigrations"], check=True)
        subprocess.run([sys.executable, "manage.py", "migrate"], check=True)
        print("✅ Migraciones ejecutadas correctamente")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error ejecutando migraciones: {e}")

def create_sample_data_menu():
    """Crear datos de ejemplo desde menú"""
    print("\n🌱 Creando datos de ejemplo...")
    try:
        subprocess.run([sys.executable, "seed_data.py"], check=True)
        print("✅ Datos de ejemplo creados correctamente")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error creando datos de ejemplo: {e}")

def show_system_status():
    """Mostrar estado del sistema"""
    print("\n📋 ESTADO DEL SISTEMA")
    print("=" * 40)
    
    # Verificar archivos
    files_status = {
        "requirements.txt": Path("requirements.txt").exists(),
        "manage.py": Path("manage.py").exists(),
        ".env": Path(".env").exists(),
        "db.sqlite3": Path("db.sqlite3").exists(),
    }
    
    for file, exists in files_status.items():
        status = "✅" if exists else "❌"
        print(f"{status} {file}")
    
    # Verificar dependencias principales
    try:
        import django
        print(f"✅ Django {django.get_version()}")
    except ImportError:
        print("❌ Django no instalado")
    
    try:
        import pandas
        print(f"✅ Pandas {pandas.__version__}")
    except ImportError:
        print("❌ Pandas no instalado")
    
    try:
        import plotly
        print(f"✅ Plotly {plotly.__version__}")
    except ImportError:
        print("❌ Plotly no instalado")

def main():
    """Función principal"""
    print_banner()
    
    # Verificar requisitos
    if not check_requirements():
        print("\n❌ No se pueden cumplir los requisitos del sistema")
        return
    
    # Verificar archivo .env
    env_configured = check_env_file()
    
    # Instalar dependencias
    if not install_dependencies():
        print("\n❌ Error instalando dependencias")
        return
    
    # Configurar base de datos
    if not setup_database():
        print("\n❌ Error configurando base de datos")
        return
    
    # Crear datos de ejemplo si no existen
    if not Path("db.sqlite3").exists() or Path("db.sqlite3").stat().st_size < 1000:
        if not create_sample_data():
            print("\n⚠️  No se pudieron crear datos de ejemplo")
    
    print("\n✅ ¡Sistema configurado correctamente!")
    
    # Mostrar menú principal
    while True:
        show_menu()
        
        try:
            opcion = input("\nSelecciona una opción (1-7): ").strip()
            
            if opcion == "1":
                start_django_server()
            elif opcion == "2":
                start_dashboard()
            elif opcion == "3":
                start_cli()
            elif opcion == "4":
                run_migrations()
            elif opcion == "5":
                create_sample_data_menu()
            elif opcion == "6":
                show_system_status()
            elif opcion == "7":
                print("\n👋 ¡Hasta luego!")
                break
            else:
                print("\n❌ Opción inválida. Intenta de nuevo.")
            
            if opcion in ["1", "2", "3"]:
                input("\nPresiona Enter para continuar...")
                
        except KeyboardInterrupt:
            print("\n\n👋 ¡Hasta luego!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()
