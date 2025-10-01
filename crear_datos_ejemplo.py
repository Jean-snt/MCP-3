#!/usr/bin/env python
"""
Script para crear datos de ejemplo en la base de datos
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventario_proj.settings')
django.setup()

from inventario.models import Product

def crear_productos_ejemplo():
    """Crear productos de ejemplo para el inventario"""
    
    # Limpiar productos existentes
    Product.objects.all().delete()
    print("Productos existentes eliminados")
    
    # Productos de ejemplo
    productos = [
        {
            'name': 'Teclado Mecánico RGB',
            'description': 'Teclado mecánico gaming con retroiluminación RGB, switches Cherry MX Red',
            'quantity': 15
        },
        {
            'name': 'Mouse Inalámbrico',
            'description': 'Mouse inalámbrico óptico con sensor de alta precisión y batería de larga duración',
            'quantity': 30
        },
        {
            'name': 'Monitor 24 pulgadas',
            'description': 'Monitor LED 24 pulgadas Full HD, 75Hz, con tecnología FreeSync',
            'quantity': 10
        },
        {
            'name': 'Auriculares Gaming',
            'description': 'Auriculares gaming con micrófono retráctil y sonido 7.1 virtual',
            'quantity': 0  # Producto agotado para probar
        },
        {
            'name': 'Webcam HD 1080p',
            'description': 'Cámara web HD con autofoco automático y micrófono integrado',
            'quantity': 8
        },
        {
            'name': 'Tablet Gráfica',
            'description': 'Tablet digitalizadora para diseño gráfico y ilustración digital',
            'quantity': 5
        },
        {
            'name': 'Disco Duro Externo 1TB',
            'description': 'Disco duro externo USB 3.0 de 1TB para respaldo y almacenamiento',
            'quantity': 12
        },
        {
            'name': 'Memoria RAM DDR4 16GB',
            'description': 'Módulo de memoria RAM DDR4 de 16GB, 3200MHz, para PC gaming',
            'quantity': 0  # Otro producto agotado
        }
    ]
    
    # Crear productos
    productos_creados = []
    for producto_data in productos:
        producto = Product.objects.create(**producto_data)
        productos_creados.append(producto)
        print(f"Creado: {producto.name} ({producto.quantity} unidades)")
    
    print(f"\nSe crearon {len(productos_creados)} productos de ejemplo")
    print(f"Productos disponibles: {Product.objects.filter(quantity__gt=0).count()}")
    print(f"Productos agotados: {Product.objects.filter(quantity=0).count()}")
    
    return productos_creados

if __name__ == '__main__':
    try:
        productos = crear_productos_ejemplo()
        print("\nDatos de ejemplo creados exitosamente!")
        print("Ahora puedes ejecutar el servidor Django con: python manage.py runserver")
        print("Y visitar: http://127.0.0.1:8000")
        
    except Exception as e:
        print(f"Error al crear los datos de ejemplo: {e}")
        sys.exit(1)
