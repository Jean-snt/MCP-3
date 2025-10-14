#!/usr/bin/env python
"""
🚀 Smart Inventory System - Inicio Rápido
Sistema de Inventario Inteligente con IA

Este script te ayuda a iniciar rápidamente el sistema completo.
"""

import os
import sys
import subprocess
import time
import webbrowser
from pathlib import Path

def print_banner():

    print("=" * 60)
    print("🏗️  SMART INVENTORY SYSTEM")
    print("   Sistema de Inventario Inteligente con IA")
    print("=" * 60)
    print()

def check_requirements():
    """Verificar que los requisitos estén instalados"""
    print("🔍 Verificando requisitos...")
    
    try:
        import django
        import pandas
        import numpy
        import sklearn
        import plotly
        import dash
        print("✅ Todas las dependencias están instaladas")
        return True
    except ImportError as e:
        print(f"❌ Faltan dependencias: {e}")
        print("💡 Ejecuta: pip install -r requirements.txt")
        return False

def check_database():
    """Verificar estado de la base de datos"""
    print("\n🗄️  Verificando base de datos...")
    
    if not os.path.exists("db.sqlite3"):
        print(" Base de datos no encontrada")
        return False
    
    # Verificar que Django puede conectarse
    try:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "inventario_project.settings")
        import django
        django.setup()
        
        from productos.models import Producto, Proveedor
        productos_count = Producto.objects.count()
        proveedores_count = Proveedor.objects.count()
        
        print(f"✅ Base de datos OK - {productos_count} productos, {proveedores_count} proveedores")
        return True
    except Exception as e:
        print(f"❌ Error en base de datos: {e}")
        return False

def show_menu():
    """Mostrar menú principal"""
    print("\n📋 MENÚ PRINCIPAL")
    print("1. 🌐 Iniciar Servidor Web Principal (Django)")
    print("2. 📊 Iniciar Dashboard Interactivo (Plotly Dash)")
    print("3. 💻 Usar CLI Inteligente")
    print("4. 📦 Cargar Datos de Ejemplo")
    print("5. 🔧 Configurar Sistema Inicial")
    print("6. 📖 Ver Documentación")
    print("7. 🚪 Salir")
    print()

def start_django_server():
    """Iniciar servidor Django"""
    print("\n🌐 Iniciando servidor Django...")
    print("📍 URL: http://localhost:8000")
    print("📍 Admin: http://localhost:8000/admin/")
    print("📍 API: http://localhost:8000/api/")
    print("\n💡 Presiona Ctrl+C para detener el servidor")
    
    try:
        subprocess.run([sys.executable, "manage.py", "runserver"], check=True)
    except KeyboardInterrupt:
        print("\n⏹️  Servidor detenido")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al iniciar servidor: {e}")

def start_dashboard():
    """Iniciar dashboard interactivo"""
    print("\n📊 Iniciando Dashboard Interactivo...")
    print("📍 URL: http://localhost:8050")
    print("\n💡 Presiona Ctrl+C para detener el dashboard")
    
    try:
        subprocess.run([sys.executable, "dashboard_app.py"], check=True)
    except KeyboardInterrupt:
        print("\n⏹️  Dashboard detenido")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al iniciar dashboard: {e}")

def use_cli():
    """Usar CLI inteligente"""
    print("\n💻 CLI Inteligente")
    print("1. Modo básico")
    print("2. Modo interactivo")
    
    choice = input("\nSelecciona opción (1-2): ").strip()
    
    if choice == "1":
        print("\n🔍 Ejecutando consulta básica...")
        subprocess.run([sys.executable, "consultar_inventario.py"])
    elif choice == "2":
        print("\n🔍 Ejecutando modo interactivo...")
        subprocess.run([sys.executable, "consultar_inventario.py", "--interactive"])
    else:
        print("❌ Opción inválida")

def load_sample_data():
    """Cargar datos de ejemplo"""
    print("\n📦 Cargando datos de ejemplo...")
    print("⚠️  Esto eliminará todos los datos existentes")
    
    confirm = input("¿Continuar? (s/N): ").strip().lower()
    if confirm in ['s', 'si', 'sí', 'y', 'yes']:
        try:
            subprocess.run([sys.executable, "populate_db.py"], check=True)
            print("✅ Datos de ejemplo cargados exitosamente")
        except subprocess.CalledProcessError as e:
            print(f"❌ Error al cargar datos: {e}")
    else:
        print("❌ Operación cancelada")

def setup_initial():
    """Configurar sistema inicial"""
    print("\n🔧 Configurando sistema inicial...")
    
    try:
        subprocess.run([sys.executable, "setup_inicial.py"], check=True)
        print("✅ Sistema configurado exitosamente")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error en configuración: {e}")

def show_documentation():
    """Mostrar documentación"""
    print("\n📖 DOCUMENTACIÓN DEL SISTEMA")
    print("=" * 40)
    
    docs = [
        ("README.md", "Documentación principal del proyecto"),
        ("ESTRUCTURA_PROYECTO.md", "Estructura completa del sistema"),
        ("requirements.txt", "Lista de dependencias")
    ]
    
    for doc, description in docs:
        if os.path.exists(doc):
            print(f"📄 {doc} - {description}")
        else:
            print(f"❌ {doc} - No encontrado")
    
    print("\n🌐 URLs importantes:")
    print("   • Servidor principal: http://localhost:8000")
    print("   • Dashboard interactivo: http://localhost:8050")
    print("   • Panel de administración: http://localhost:8000/admin/")
    print("   • API REST: http://localhost:8000/api/")

def main():
    """Función principal"""
    print_banner()
    
    # Verificar requisitos
    if not check_requirements():
        return
    
    # Verificar base de datos
    db_ok = check_database()
    
    while True:
        show_menu()
        
        try:
            choice = input("Selecciona una opción (1-7): ").strip()
            
            if choice == "1":
                start_django_server()
            elif choice == "2":
                start_dashboard()
            elif choice == "3":
                use_cli()
            elif choice == "4":
                load_sample_data()
            elif choice == "5":
                setup_initial()
            elif choice == "6":
                show_documentation()
            elif choice == "7":
                print("\n👋 ¡Hasta luego!")
                break
            else:
                print("❌ Opción inválida. Selecciona 1-7.")
                
        except KeyboardInterrupt:
            print("\n\n👋 ¡Hasta luego!")
            break
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
        
        input("\n⏸️  Presiona Enter para continuar...")

if __name__ == "__main__":
    main()

