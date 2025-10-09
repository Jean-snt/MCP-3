import os
import django
from datetime import datetime, timedelta
import random

# Configurar Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "inventario_project.settings")
django.setup()

from productos.models import Proveedor, Producto, Venta, MovimientoInventario

def crear_proveedores():
    """Crear proveedores de ejemplo"""
    proveedores_data = [
        {
            'nombre': 'TechSupply Corp',
            'contacto': 'Juan Pérez',
            'telefono': '+1-555-0101',
            'email': 'juan@techsupply.com',
            'direccion': '123 Tech Street, Silicon Valley, CA'
        },
        {
            'nombre': 'ElectroMax',
            'contacto': 'María García',
            'telefono': '+1-555-0102',
            'email': 'maria@electromax.com',
            'direccion': '456 Electronics Ave, Austin, TX'
        },
        {
            'nombre': 'HomeGoods Plus',
            'contacto': 'Carlos López',
            'telefono': '+1-555-0103',
            'email': 'carlos@homegoods.com',
            'direccion': '789 Home Street, Miami, FL'
        },
        {
            'nombre': 'SportsWorld',
            'contacto': 'Ana Martínez',
            'telefono': '+1-555-0104',
            'email': 'ana@sportsworld.com',
            'direccion': '321 Sports Blvd, Denver, CO'
        },
        {
            'nombre': 'BookHaven',
            'contacto': 'Roberto Silva',
            'telefono': '+1-555-0105',
            'email': 'roberto@bookhaven.com',
            'direccion': '654 Library Lane, Seattle, WA'
        }
    ]
    
    proveedores = []
    for data in proveedores_data:
        proveedor, created = Proveedor.objects.get_or_create(
            nombre=data['nombre'],
            defaults=data
        )
        proveedores.append(proveedor)
        print(f"✅ Proveedor creado: {proveedor.nombre}")
    
    return proveedores

def crear_productos(proveedores):
    """Crear productos de ejemplo"""
    productos_data = [
        # Electrónicos
        {'nombre': 'iPhone 15 Pro', 'categoria': 'electronica', 'precio_compra': 800, 'precio_venta': 1200, 'cantidad': 25, 'cantidad_minima': 5, 'codigo_barras': '1234567890123'},
        {'nombre': 'MacBook Air M2', 'categoria': 'electronica', 'precio_compra': 900, 'precio_venta': 1300, 'cantidad': 15, 'cantidad_minima': 3, 'codigo_barras': '1234567890124'},
        {'nombre': 'Samsung Galaxy S24', 'categoria': 'electronica', 'precio_compra': 700, 'precio_venta': 1000, 'cantidad': 30, 'cantidad_minima': 5, 'codigo_barras': '1234567890125'},
        {'nombre': 'AirPods Pro', 'categoria': 'electronica', 'precio_compra': 150, 'precio_venta': 250, 'cantidad': 50, 'cantidad_minima': 10, 'codigo_barras': '1234567890126'},
        {'nombre': 'iPad Air', 'categoria': 'electronica', 'precio_compra': 400, 'precio_venta': 600, 'cantidad': 20, 'cantidad_minima': 4, 'codigo_barras': '1234567890127'},
        
        # Ropa
        {'nombre': 'Camiseta Nike Dri-FIT', 'categoria': 'ropa', 'precio_compra': 15, 'precio_venta': 35, 'cantidad': 100, 'cantidad_minima': 20, 'codigo_barras': '1234567890128'},
        {'nombre': 'Jeans Levis 501', 'categoria': 'ropa', 'precio_compra': 30, 'precio_venta': 80, 'cantidad': 75, 'cantidad_minima': 15, 'codigo_barras': '1234567890129'},
        {'nombre': 'Zapatillas Adidas Ultraboost', 'categoria': 'ropa', 'precio_compra': 80, 'precio_venta': 180, 'cantidad': 40, 'cantidad_minima': 8, 'codigo_barras': '1234567890130'},
        {'nombre': 'Chaqueta North Face', 'categoria': 'ropa', 'precio_compra': 60, 'precio_venta': 150, 'cantidad': 25, 'cantidad_minima': 5, 'codigo_barras': '1234567890131'},
        
        # Hogar
        {'nombre': 'Aspiradora Dyson V15', 'categoria': 'hogar', 'precio_compra': 300, 'precio_venta': 500, 'cantidad': 10, 'cantidad_minima': 2, 'codigo_barras': '1234567890132'},
        {'nombre': 'Cafetera Nespresso', 'categoria': 'hogar', 'precio_compra': 80, 'precio_venta': 150, 'cantidad': 15, 'cantidad_minima': 3, 'codigo_barras': '1234567890133'},
        {'nombre': 'Robot Aspirador iRobot', 'categoria': 'hogar', 'precio_compra': 200, 'precio_venta': 350, 'cantidad': 8, 'cantidad_minima': 2, 'codigo_barras': '1234567890134'},
        {'nombre': 'Sartén Antiadherente', 'categoria': 'hogar', 'precio_compra': 25, 'precio_venta': 50, 'cantidad': 30, 'cantidad_minima': 6, 'codigo_barras': '1234567890135'},
        
        # Deportes
        {'nombre': 'Pelota de Fútbol Adidas', 'categoria': 'deportes', 'precio_compra': 20, 'precio_venta': 45, 'cantidad': 50, 'cantidad_minima': 10, 'codigo_barras': '1234567890136'},
        {'nombre': 'Raqueta de Tenis Wilson', 'categoria': 'deportes', 'precio_compra': 80, 'precio_venta': 150, 'cantidad': 20, 'cantidad_minima': 4, 'codigo_barras': '1234567890137'},
        {'nombre': 'Bicicleta Mountain Bike', 'categoria': 'deportes', 'precio_compra': 300, 'precio_venta': 600, 'cantidad': 5, 'cantidad_minima': 1, 'codigo_barras': '1234567890138'},
        {'nombre': 'Pesas Ajustables', 'categoria': 'deportes', 'precio_compra': 100, 'precio_venta': 200, 'cantidad': 12, 'cantidad_minima': 3, 'codigo_barras': '1234567890139'},
        
        # Libros
        {'nombre': 'Python para Principiantes', 'categoria': 'libros', 'precio_compra': 15, 'precio_venta': 30, 'cantidad': 25, 'cantidad_minima': 5, 'codigo_barras': '1234567890140'},
        {'nombre': 'El Arte de la Guerra', 'categoria': 'libros', 'precio_compra': 8, 'precio_venta': 18, 'cantidad': 40, 'cantidad_minima': 8, 'codigo_barras': '1234567890141'},
        {'nombre': 'Cocina Mediterránea', 'categoria': 'libros', 'precio_compra': 20, 'precio_venta': 40, 'cantidad': 15, 'cantidad_minima': 3, 'codigo_barras': '1234567890142'},
        
        # Alimentación
        {'nombre': 'Café Premium Colombia', 'categoria': 'alimentacion', 'precio_compra': 12, 'precio_venta': 25, 'cantidad': 60, 'cantidad_minima': 12, 'codigo_barras': '1234567890143'},
        {'nombre': 'Aceite de Oliva Extra Virgen', 'categoria': 'alimentacion', 'precio_compra': 8, 'precio_venta': 18, 'cantidad': 35, 'cantidad_minima': 7, 'codigo_barras': '1234567890144'},
        {'nombre': 'Chocolate Artesanal', 'categoria': 'alimentacion', 'precio_compra': 5, 'precio_venta': 12, 'cantidad': 80, 'cantidad_minima': 16, 'codigo_barras': '1234567890145'},
    ]
    
    productos = []
    for i, data in enumerate(productos_data):
        # Asignar proveedor basado en categoría
        if data['categoria'] == 'electronica':
            proveedor = proveedores[0]  # TechSupply Corp
        elif data['categoria'] == 'ropa':
            proveedor = proveedores[1]  # ElectroMax
        elif data['categoria'] == 'hogar':
            proveedor = proveedores[2]  # HomeGoods Plus
        elif data['categoria'] == 'deportes':
            proveedor = proveedores[3]  # SportsWorld
        elif data['categoria'] == 'libros':
            proveedor = proveedores[4]  # BookHaven
        else:
            proveedor = proveedores[0]  # Default
        
        producto, created = Producto.objects.get_or_create(
            nombre=data['nombre'],
            defaults={
                **data,
                'proveedor': proveedor,
                'descripcion': f"Producto {data['categoria']} de alta calidad",
                'ubicacion': f"Estante {chr(65 + i % 10)}-{i % 10 + 1}"
            }
        )
        productos.append(producto)
        print(f"✅ Producto creado: {producto.nombre}")
    
    return productos

def crear_ventas_historicas(productos):
    """Crear ventas históricas para análisis"""
    print("\n📊 Creando ventas históricas...")
    
    # Crear ventas para los últimos 90 días
    fecha_inicio = datetime.now() - timedelta(days=90)
    
    for i in range(90):
        fecha_venta = fecha_inicio + timedelta(days=i)
        
        # Crear entre 1-5 ventas por día
        num_ventas_dia = random.randint(1, 5)
        
        for j in range(num_ventas_dia):
            producto = random.choice(productos)
            cantidad_vendida = random.randint(1, min(5, producto.cantidad))
            precio_unitario = float(producto.precio_venta)
            
            # Ajustar precio ocasionalmente (descuentos/promociones)
            if random.random() < 0.1:  # 10% de probabilidad de descuento
                precio_unitario *= random.uniform(0.8, 0.95)
            
            venta = Venta.objects.create(
                producto=producto,
                cantidad_vendida=cantidad_vendida,
                precio_unitario=precio_unitario,
                fecha_venta=fecha_venta,
                cliente=f"Cliente_{random.randint(1000, 9999)}",
                notas=f"Venta histórica - Día {i+1}"
            )
            
            # Actualizar stock del producto
            producto.cantidad -= cantidad_vendida
            if producto.cantidad < 0:
                producto.cantidad = 0
            producto.save()
            
            # Registrar movimiento de inventario
            MovimientoInventario.objects.create(
                producto=producto,
                tipo_movimiento='salida',
                cantidad=-cantidad_vendida,
                motivo=f"Venta histórica - {venta.cliente}",
                fecha_movimiento=fecha_venta,
                usuario="Sistema"
            )
    
    print(f"✅ Creadas ventas históricas para 90 días")

def crear_movimientos_inventario(productos):
    """Crear movimientos de inventario adicionales"""
    print("\n📦 Creando movimientos de inventario...")
    
    for producto in productos:
        # Crear algunos reabastecimientos
        if random.random() < 0.3:  # 30% de probabilidad
            cantidad_entrada = random.randint(10, 50)
            fecha_movimiento = datetime.now() - timedelta(days=random.randint(1, 30))
            
            MovimientoInventario.objects.create(
                producto=producto,
                tipo_movimiento='entrada',
                cantidad=cantidad_entrada,
                motivo="Reabastecimiento automático",
                fecha_movimiento=fecha_movimiento,
                usuario="Sistema"
            )
            
            # Actualizar stock
            producto.cantidad += cantidad_entrada
            producto.save()
    
    print("✅ Movimientos de inventario creados")

def main():
    """Función principal para crear todos los datos de ejemplo"""
    print("🚀 Iniciando creación de datos de ejemplo...")
    print("=" * 50)
    
    # Limpiar datos existentes (opcional)
    print("🧹 Limpiando datos existentes...")
    Venta.objects.all().delete()
    MovimientoInventario.objects.all().delete()
    Producto.objects.all().delete()
    Proveedor.objects.all().delete()
    
    # Crear datos
    print("\n👥 Creando proveedores...")
    proveedores = crear_proveedores()
    
    print("\n📦 Creando productos...")
    productos = crear_productos(proveedores)
    
    print("\n💰 Creando ventas históricas...")
    crear_ventas_historicas(productos)
    
    print("\n📋 Creando movimientos de inventario...")
    crear_movimientos_inventario(productos)
    
    print("\n" + "=" * 50)
    print("✅ ¡Datos de ejemplo creados exitosamente!")
    print(f"📊 Resumen:")
    print(f"   • Proveedores: {Proveedor.objects.count()}")
    print(f"   • Productos: {Producto.objects.count()}")
    print(f"   • Ventas: {Venta.objects.count()}")
    print(f"   • Movimientos: {MovimientoInventario.objects.count()}")
    print("\n🎯 Ahora puedes:")
    print("   • Ejecutar el servidor Django: python manage.py runserver")
    print("   • Usar el CLI: python consultar_inventario.py --interactive")
    print("   • Ejecutar el dashboard: python dashboard_app.py")

if __name__ == "__main__":
    main()
