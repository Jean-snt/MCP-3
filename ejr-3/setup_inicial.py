#!/usr/bin/env python
"""
Script para crear datos iniciales básicos del sistema de inventario
Ejecutar: python setup_inicial.py
"""

import os
import django
from datetime import datetime, timedelta
import random

# Configurar Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "inventario_project.settings")
django.setup()

from productos.models import Proveedor, Producto, Venta, MovimientoInventario

def crear_proveedor_ejemplo():
    """Crear un proveedor de ejemplo"""
    proveedor = Proveedor.objects.create(
        nombre="Proveedor Principal",
        contacto="Contacto Principal",
        telefono="+1-555-0000",
        email="contacto@proveedor.com",
        direccion="Dirección Principal"
    )
    print(f"Proveedor creado: {proveedor.nombre}")
    return proveedor

def crear_producto_ejemplo(proveedor):
    """Crear un producto de ejemplo"""
    producto = Producto.objects.create(
        nombre="Producto de Ejemplo",
        descripcion="Descripción del producto de ejemplo",
        categoria="General",
        cantidad=100,
        cantidad_minima=10,
        precio_compra=50.00,
        precio_venta=75.00,
        proveedor=proveedor,
        codigo_barras="123456789",
        ubicacion="Almacén A"
    )
    print(f"Producto creado: {producto.nombre}")
    return producto

def main():
    """Función principal para crear datos iniciales básicos"""
    print("Configurando sistema inicial...")
    print("=" * 40)
    
    # Limpiar datos existentes
    print("Limpiando datos existentes...")
    Venta.objects.all().delete()
    MovimientoInventario.objects.all().delete()
    Producto.objects.all().delete()
    Proveedor.objects.all().delete()
    
    # Crear datos básicos
    print("\nCreando proveedor de ejemplo...")
    proveedor = crear_proveedor_ejemplo()
    
    print("\nCreando producto de ejemplo...")
    producto = crear_producto_ejemplo(proveedor)
    
    print("\n" + "=" * 40)
    print("Sistema configurado exitosamente!")
    print("Resumen:")
    print(f"   - Proveedores: {Proveedor.objects.count()}")
    print(f"   - Productos: {Producto.objects.count()}")
    print(f"   - Ventas: {Venta.objects.count()}")
    print(f"   - Movimientos: {MovimientoInventario.objects.count()}")
    
    print("\nAhora puedes:")
    print("   - Ejecutar el servidor Django: python manage.py runserver")
    print("   - Usar el CLI: python consultar_inventario.py --interactive")
    print("   - Ejecutar el dashboard: python dashboard_app.py")
    print("   - Agregar tus propios datos desde la interfaz web")

if __name__ == "__main__":
    main()

