import os
import django
from datetime import datetime, timedelta
import random

# Configurar Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "inventario_project.settings")
django.setup()

from productos.models import Proveedor, Producto, Venta, MovimientoInventario

def crear_datos_basicos():
    """Crear datos básicos de ejemplo"""
    print("Creando datos de ejemplo...")
    
    # Crear proveedores
    proveedor1 = Proveedor.objects.create(
        nombre="TechSupply Corp",
        contacto="Juan Perez",
        telefono="+1-555-0101",
        email="juan@techsupply.com",
        direccion="123 Tech Street, Silicon Valley, CA"
    )
    
    proveedor2 = Proveedor.objects.create(
        nombre="ElectroMax",
        contacto="Maria Garcia",
        telefono="+1-555-0102",
        email="maria@electromax.com",
        direccion="456 Electronics Ave, Austin, TX"
    )
    
    print("Proveedores creados")
    
    # Crear productos
    productos_data = [
        {'nombre': 'iPhone 15 Pro', 'categoria': 'electronica', 'precio_compra': 800, 'precio_venta': 1200, 'cantidad': 25, 'cantidad_minima': 5},
        {'nombre': 'MacBook Air M2', 'categoria': 'electronica', 'precio_compra': 900, 'precio_venta': 1300, 'cantidad': 15, 'cantidad_minima': 3},
        {'nombre': 'Samsung Galaxy S24', 'categoria': 'electronica', 'precio_compra': 700, 'precio_venta': 1000, 'cantidad': 30, 'cantidad_minima': 5},
        {'nombre': 'AirPods Pro', 'categoria': 'electronica', 'precio_compra': 150, 'precio_venta': 250, 'cantidad': 50, 'cantidad_minima': 10},
        {'nombre': 'Camiseta Nike', 'categoria': 'ropa', 'precio_compra': 15, 'precio_venta': 35, 'cantidad': 100, 'cantidad_minima': 20},
        {'nombre': 'Jeans Levis', 'categoria': 'ropa', 'precio_compra': 30, 'precio_venta': 80, 'cantidad': 75, 'cantidad_minima': 15},
        {'nombre': 'Aspiradora Dyson', 'categoria': 'hogar', 'precio_compra': 300, 'precio_venta': 500, 'cantidad': 10, 'cantidad_minima': 2},
        {'nombre': 'Cafetera Nespresso', 'categoria': 'hogar', 'precio_compra': 80, 'precio_venta': 150, 'cantidad': 15, 'cantidad_minima': 3},
    ]
    
    productos = []
    for data in productos_data:
        producto = Producto.objects.create(
            nombre=data['nombre'],
            categoria=data['categoria'],
            precio_compra=data['precio_compra'],
            precio_venta=data['precio_venta'],
            cantidad=data['cantidad'],
            cantidad_minima=data['cantidad_minima'],
            proveedor=proveedor1 if data['categoria'] == 'electronica' else proveedor2,
            descripcion=f"Producto {data['categoria']} de alta calidad"
        )
        productos.append(producto)
    
    print(f"Productos creados: {len(productos)}")
    
    # Crear algunas ventas
    for i in range(20):
        producto = random.choice(productos)
        cantidad = random.randint(1, 3)
        fecha = datetime.now() - timedelta(days=random.randint(1, 30))
        
        venta = Venta.objects.create(
            producto=producto,
            cantidad_vendida=cantidad,
            precio_unitario=producto.precio_venta,
            fecha_venta=fecha,
            cliente=f"Cliente_{random.randint(1000, 9999)}",
            notas="Venta de ejemplo"
        )
        
        # Actualizar stock
        producto.cantidad -= cantidad
        if producto.cantidad < 0:
            producto.cantidad = 0
        producto.save()
    
    print("Ventas creadas: 20")
    print("Datos de ejemplo creados exitosamente!")

if __name__ == "__main__":
    crear_datos_basicos()
