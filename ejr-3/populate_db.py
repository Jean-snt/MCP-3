#!/usr/bin/env python
"""
Script para poblar la base de datos con datos de ejemplo
Ejecutar: python populate_db.py
"""

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
            'direccion': '654 Book Lane, Seattle, WA'
        }
    ]
    
    proveedores = []
    for data in proveedores_data:
        proveedor, created = Proveedor.objects.get_or_create(
            nombre=data['nombre'],
            defaults=data
        )
        proveedores.append(proveedor)
        if created:
            print(f"Proveedor creado: {proveedor.nombre}")
    
    return proveedores

def crear_productos(proveedores):
    """Crear productos de ejemplo"""
    productos_data = [
        # Tecnología
        {
            'nombre': 'iPhone 15 Pro',
            'descripcion': 'Smartphone Apple con cámara profesional',
            'categoria': 'Tecnología',
            'cantidad': 25,
            'cantidad_minima': 5,
            'precio_compra': 800.00,
            'precio_venta': 999.00,
            'proveedor': proveedores[0],
            'codigo_barras': '1234567890123',
            'ubicacion': 'Almacén A - Estante 1'
        },
        {
            'nombre': 'MacBook Air M2',
            'descripcion': 'Laptop Apple con chip M2',
            'categoria': 'Tecnología',
            'cantidad': 15,
            'cantidad_minima': 3,
            'precio_compra': 1000.00,
            'precio_venta': 1299.00,
            'proveedor': proveedores[0],
            'codigo_barras': '1234567890124',
            'ubicacion': 'Almacén A - Estante 2'
        },
        {
            'nombre': 'Samsung Galaxy S24',
            'descripcion': 'Smartphone Samsung con IA integrada',
            'categoria': 'Tecnología',
            'cantidad': 30,
            'cantidad_minima': 8,
            'precio_compra': 600.00,
            'precio_venta': 799.00,
            'proveedor': proveedores[1],
            'codigo_barras': '1234567890125',
            'ubicacion': 'Almacén A - Estante 1'
        },
        {
            'nombre': 'AirPods Pro',
            'descripcion': 'Audífonos inalámbricos Apple con cancelación de ruido',
            'categoria': 'Tecnología',
            'cantidad': 50,
            'cantidad_minima': 10,
            'precio_compra': 200.00,
            'precio_venta': 249.00,
            'proveedor': proveedores[0],
            'codigo_barras': '1234567890126',
            'ubicacion': 'Almacén A - Estante 3'
        },
        {
            'nombre': 'iPad Air',
            'descripcion': 'Tablet Apple con pantalla Liquid Retina',
            'categoria': 'Tecnología',
            'cantidad': 20,
            'cantidad_minima': 4,
            'precio_compra': 500.00,
            'precio_venta': 599.00,
            'proveedor': proveedores[0],
            'codigo_barras': '1234567890127',
            'ubicacion': 'Almacén A - Estante 2'
        },
        
        # Ropa
        {
            'nombre': 'Camiseta Nike Dri-FIT',
            'descripcion': 'Camiseta deportiva con tecnología Dri-FIT',
            'categoria': 'Ropa',
            'cantidad': 100,
            'cantidad_minima': 20,
            'precio_compra': 25.00,
            'precio_venta': 35.00,
            'proveedor': proveedores[3],
            'codigo_barras': '1234567890128',
            'ubicacion': 'Almacén B - Estante 1'
        },
        {
            'nombre': 'Jeans Levis 501',
            'descripcion': 'Jeans clásicos Levis 501',
            'categoria': 'Ropa',
            'cantidad': 75,
            'cantidad_minima': 15,
            'precio_compra': 40.00,
            'precio_venta': 60.00,
            'proveedor': proveedores[3],
            'codigo_barras': '1234567890129',
            'ubicacion': 'Almacén B - Estante 2'
        },
        {
            'nombre': 'Zapatillas Adidas Ultraboost',
            'descripcion': 'Zapatillas deportivas con tecnología Boost',
            'categoria': 'Calzado',
            'cantidad': 40,
            'cantidad_minima': 8,
            'precio_compra': 120.00,
            'precio_venta': 180.00,
            'proveedor': proveedores[3],
            'codigo_barras': '1234567890130',
            'ubicacion': 'Almacén B - Estante 3'
        },
        {
            'nombre': 'Chaqueta North Face',
            'descripcion': 'Chaqueta impermeable para actividades al aire libre',
            'categoria': 'Ropa',
            'cantidad': 35,
            'cantidad_minima': 7,
            'precio_compra': 80.00,
            'precio_venta': 120.00,
            'proveedor': proveedores[3],
            'codigo_barras': '1234567890131',
            'ubicacion': 'Almacén B - Estante 4'
        },
        
        # Hogar
        {
            'nombre': 'Aspiradora Dyson V15',
            'descripcion': 'Aspiradora inalámbrica con tecnología láser',
            'categoria': 'Hogar',
            'cantidad': 12,
            'cantidad_minima': 3,
            'precio_compra': 400.00,
            'precio_venta': 549.00,
            'proveedor': proveedores[2],
            'codigo_barras': '1234567890132',
            'ubicacion': 'Almacén C - Estante 1'
        },
        {
            'nombre': 'Cafetera Nespresso',
            'descripcion': 'Cafetera de cápsulas Nespresso',
            'categoria': 'Hogar',
            'cantidad': 18,
            'cantidad_minima': 4,
            'precio_compra': 150.00,
            'precio_venta': 199.00,
            'proveedor': proveedores[2],
            'codigo_barras': '1234567890133',
            'ubicacion': 'Almacén C - Estante 2'
        },
        {
            'nombre': 'Robot Aspirador iRobot',
            'descripcion': 'Robot aspirador inteligente con mapeo',
            'categoria': 'Hogar',
            'cantidad': 8,
            'cantidad_minima': 2,
            'precio_compra': 300.00,
            'precio_venta': 399.00,
            'proveedor': proveedores[2],
            'codigo_barras': '1234567890134',
            'ubicacion': 'Almacén C - Estante 1'
        },
        {
            'nombre': 'Sartén Antiadherente',
            'descripcion': 'Sartén de acero inoxidable con recubrimiento antiadherente',
            'categoria': 'Cocina',
            'cantidad': 25,
            'cantidad_minima': 5,
            'precio_compra': 30.00,
            'precio_venta': 45.00,
            'proveedor': proveedores[2],
            'codigo_barras': '1234567890135',
            'ubicacion': 'Almacén C - Estante 3'
        },
        
        # Deportes
        {
            'nombre': 'Pelota de Fútbol Adidas',
            'descripcion': 'Pelota oficial de fútbol Adidas',
            'categoria': 'Deportes',
            'cantidad': 60,
            'cantidad_minima': 12,
            'precio_compra': 20.00,
            'precio_venta': 35.00,
            'proveedor': proveedores[3],
            'codigo_barras': '1234567890136',
            'ubicacion': 'Almacén D - Estante 1'
        },
        {
            'nombre': 'Raqueta de Tenis Wilson',
            'descripcion': 'Raqueta de tenis profesional Wilson',
            'categoria': 'Deportes',
            'cantidad': 15,
            'cantidad_minima': 3,
            'precio_compra': 80.00,
            'precio_venta': 120.00,
            'proveedor': proveedores[3],
            'codigo_barras': '1234567890137',
            'ubicacion': 'Almacén D - Estante 2'
        },
        {
            'nombre': 'Bicicleta Mountain Bike',
            'descripcion': 'Bicicleta de montaña con suspensión',
            'categoria': 'Deportes',
            'cantidad': 5,
            'cantidad_minima': 1,
            'precio_compra': 400.00,
            'precio_venta': 599.00,
            'proveedor': proveedores[3],
            'codigo_barras': '1234567890138',
            'ubicacion': 'Almacén D - Estante 3'
        },
        {
            'nombre': 'Pesas Ajustables',
            'descripcion': 'Set de pesas ajustables para gimnasio en casa',
            'categoria': 'Deportes',
            'cantidad': 20,
            'cantidad_minima': 4,
            'precio_compra': 100.00,
            'precio_venta': 150.00,
            'proveedor': proveedores[3],
            'codigo_barras': '1234567890139',
            'ubicacion': 'Almacén D - Estante 4'
        },
        
        # Libros
        {
            'nombre': 'Python para Principiantes',
            'descripcion': 'Libro de programación Python para principiantes',
            'categoria': 'Libros',
            'cantidad': 45,
            'cantidad_minima': 10,
            'precio_compra': 15.00,
            'precio_venta': 25.00,
            'proveedor': proveedores[4],
            'codigo_barras': '1234567890140',
            'ubicacion': 'Almacén E - Estante 1'
        },
        {
            'nombre': 'El Arte de la Guerra',
            'descripcion': 'Clásico de estrategia militar de Sun Tzu',
            'categoria': 'Libros',
            'cantidad': 30,
            'cantidad_minima': 6,
            'precio_compra': 8.00,
            'precio_venta': 15.00,
            'proveedor': proveedores[4],
            'codigo_barras': '1234567890141',
            'ubicacion': 'Almacén E - Estante 2'
        },
        {
            'nombre': 'Cocina Mediterránea',
            'descripcion': 'Libro de recetas de cocina mediterránea',
            'categoria': 'Libros',
            'cantidad': 25,
            'cantidad_minima': 5,
            'precio_compra': 12.00,
            'precio_venta': 20.00,
            'proveedor': proveedores[4],
            'codigo_barras': '1234567890142',
            'ubicacion': 'Almacén E - Estante 3'
        },
        
        # Alimentos
        {
            'nombre': 'Café Premium Colombia',
            'descripcion': 'Café en grano premium de Colombia',
            'categoria': 'Alimentos',
            'cantidad': 80,
            'cantidad_minima': 16,
            'precio_compra': 10.00,
            'precio_venta': 18.00,
            'proveedor': proveedores[2],
            'codigo_barras': '1234567890143',
            'ubicacion': 'Almacén F - Estante 1'
        },
        {
            'nombre': 'Aceite de Oliva Extra Virgen',
            'descripcion': 'Aceite de oliva extra virgen español',
            'categoria': 'Alimentos',
            'cantidad': 50,
            'cantidad_minima': 10,
            'precio_compra': 8.00,
            'precio_venta': 15.00,
            'proveedor': proveedores[2],
            'codigo_barras': '1234567890144',
            'ubicacion': 'Almacén F - Estante 2'
        },
        {
            'nombre': 'Chocolate Artesanal',
            'descripcion': 'Chocolate artesanal belga',
            'categoria': 'Alimentos',
            'cantidad': 35,
            'cantidad_minima': 7,
            'precio_compra': 6.00,
            'precio_venta': 12.00,
            'proveedor': proveedores[2],
            'codigo_barras': '1234567890145',
            'ubicacion': 'Almacén F - Estante 3'
        }
    ]
    
    productos = []
    for data in productos_data:
        producto, created = Producto.objects.get_or_create(
            nombre=data['nombre'],
            defaults=data
        )
        productos.append(producto)
        if created:
            print(f"Producto creado: {producto.nombre}")
    
    return productos

def crear_ventas_historicas(productos):
    """Crear ventas históricas para los últimos 90 días"""
    fecha_inicio = datetime.now() - timedelta(days=90)
    
    for i in range(90):
        fecha_venta = fecha_inicio + timedelta(days=i)
        
        # Crear entre 1-8 ventas por día
        num_ventas_dia = random.randint(1, 8)
        
        for j in range(num_ventas_dia):
            producto = random.choice(productos)
            # Solo crear ventas para productos con stock disponible
            if producto.cantidad > 0:
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
    
    print(f"Creadas ventas históricas para 90 días")

def crear_movimientos_inventario(productos):
    """Crear movimientos de inventario adicionales"""
    # Crear algunos movimientos de entrada (reabastecimientos)
    for producto in productos[:10]:  # Solo para los primeros 10 productos
        fecha_movimiento = datetime.now() - timedelta(days=random.randint(1, 30))
        cantidad_entrada = random.randint(10, 50)
        
        MovimientoInventario.objects.create(
            producto=producto,
            tipo_movimiento='entrada',
            cantidad=cantidad_entrada,
            motivo=f"Reabastecimiento automático",
            fecha_movimiento=fecha_movimiento,
            usuario="Sistema"
        )
        
        # Actualizar stock
        producto.cantidad += cantidad_entrada
        producto.save()
    
    print("Movimientos de inventario creados")

def main():
    """Función principal para crear todos los datos de ejemplo"""
    print("Iniciando creacion de datos de ejemplo...")
    print("=" * 50)
    
    # Limpiar datos existentes (opcional)
    print("Limpiando datos existentes...")
    Venta.objects.all().delete()
    MovimientoInventario.objects.all().delete()
    Producto.objects.all().delete()
    Proveedor.objects.all().delete()
    
    # Crear datos
    print("\nCreando proveedores...")
    proveedores = crear_proveedores()
    
    print("\nCreando productos...")
    productos = crear_productos(proveedores)
    
    print("\nCreando ventas historicas...")
    crear_ventas_historicas(productos)
    
    print("\nCreando movimientos de inventario...")
    crear_movimientos_inventario(productos)
    
    print("\n" + "=" * 50)
    print("Datos de ejemplo creados exitosamente!")
    print("Resumen:")
    print(f"   - Proveedores: {Proveedor.objects.count()}")
    print(f"   - Productos: {Producto.objects.count()}")
    print(f"   - Ventas: {Venta.objects.count()}")
    print(f"   - Movimientos: {MovimientoInventario.objects.count()}")
    
    print("\nAhora puedes:")
    print("   - Ejecutar el servidor Django: python manage.py runserver")
    print("   - Usar el CLI: python consultar_inventario.py --interactive")
    print("   - Ejecutar el dashboard: python dashboard_app.py")

if __name__ == "__main__":
    main()

