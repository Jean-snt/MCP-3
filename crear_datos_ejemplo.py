#!/usr/bin/env python3
import os
import sys
import django
from datetime import datetime, timedelta
import random

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from productos.models import Product, Sale, Supplier, Category, PurchaseOrder
from django.utils import timezone
from decimal import Decimal

def crear_categorias():
    """Crear categorías de ejemplo"""
    categorias = [
        {'name': 'Electrónica', 'description': 'Dispositivos electrónicos y accesorios'},
        {'name': 'Papelería', 'description': 'Artículos de oficina y papelería'},
        {'name': 'Hogar', 'description': 'Artículos para el hogar'},
        {'name': 'Tecnología', 'description': 'Equipos tecnológicos'},
        {'name': 'Accesorios', 'description': 'Accesorios variados'},
    ]
    
    created_categories = []
    for cat_data in categorias:
        cat, created = Category.objects.get_or_create(
            name=cat_data['name'],
            defaults={'description': cat_data['description']}
        )
        created_categories.append(cat)
        if created:
            print(f"✅ Categoría creada: {cat.name}")
    
    return created_categories

def crear_proveedores():
    """Crear proveedores de ejemplo"""
    proveedores = [
        {
            'name': 'TechSupply S.A.',
            'contact_person': 'Juan Pérez',
            'email': 'contacto@techsupply.com',
            'phone': '+34 912 345 678',
            'address': 'Calle Tech 123, Madrid'
        },
        {
            'name': 'OfficeMax Distribuidores',
            'contact_person': 'María García',
            'email': 'ventas@officemax.com',
            'phone': '+34 913 456 789',
            'address': 'Av. Oficina 456, Barcelona'
        },
        {
            'name': 'HomeGoods Import',
            'contact_person': 'Carlos Ruiz',
            'email': 'info@homegoods.com',
            'phone': '+34 914 567 890',
            'address': 'Plaza Hogar 789, Valencia'
        },
    ]
    
    created_suppliers = []
    for sup_data in proveedores:
        sup, created = Supplier.objects.get_or_create(
            email=sup_data['email'],
            defaults=sup_data
        )
        created_suppliers.append(sup)
        if created:
            print(f"✅ Proveedor creado: {sup.name}")
    
    return created_suppliers

def crear_productos(categorias, proveedores):
    """Crear productos de ejemplo"""
    productos = [
        {'name': 'Laptop Dell XPS 13', 'category': 'Tecnología', 'price': 1299.99, 'quantity': 15},
        {'name': 'Mouse Inalámbrico Logitech', 'category': 'Electrónica', 'price': 29.99, 'quantity': 45},
        {'name': 'Teclado Mecánico RGB', 'category': 'Electrónica', 'price': 89.99, 'quantity': 30},
        {'name': 'Monitor 24" Full HD', 'category': 'Tecnología', 'price': 199.99, 'quantity': 20},
        {'name': 'Auriculares Bluetooth', 'category': 'Electrónica', 'price': 59.99, 'quantity': 35},
        {'name': 'Cuaderno A4 100 hojas', 'category': 'Papelería', 'price': 3.99, 'quantity': 120},
        {'name': 'Bolígrafos Pack x12', 'category': 'Papelería', 'price': 5.99, 'quantity': 80},
        {'name': 'Lámpara de Escritorio LED', 'category': 'Hogar', 'price': 24.99, 'quantity': 25},
        {'name': 'Organizador de Cables', 'category': 'Accesorios', 'price': 12.99, 'quantity': 50},
        {'name': 'Webcam HD 1080p', 'category': 'Tecnología', 'price': 79.99, 'quantity': 18},
        {'name': 'Mousepad Ergonómico', 'category': 'Accesorios', 'price': 15.99, 'quantity': 40},
        {'name': 'Hub USB-C 7 puertos', 'category': 'Tecnología', 'price': 39.99, 'quantity': 22},
    ]
    
    cat_dict = {cat.name: cat for cat in categorias}
    created_products = []
    
    for i, prod_data in enumerate(productos):
        category = cat_dict.get(prod_data['category'])
        supplier = random.choice(proveedores)
        
        product, created = Product.objects.get_or_create(
            name=prod_data['name'],
            defaults={
                'description': f'Producto de calidad premium - {prod_data["name"]}',
                'sku': f'SKU-{1000 + i}',
                'quantity': prod_data['quantity'],
                'min_stock_level': 10,
                'max_stock_level': 100,
                'cost_price': Decimal(str(prod_data['price'] * 0.6)),
                'selling_price': Decimal(str(prod_data['price'])),
                'category': category,
                'supplier': supplier,
                'safety_stock': 5,
                'lead_time_days': random.randint(3, 14),
            }
        )
        created_products.append(product)
        if created:
            print(f"✅ Producto creado: {product.name} - Stock: {product.quantity}")
    
    return created_products

def crear_ventas(productos):
    """Crear ventas de ejemplo"""
    print("\n📊 Creando ventas de ejemplo...")
    
    clientes = [
        'Juan Martínez', 'Ana López', 'Carlos García', 'María Rodríguez',
        'Pedro Sánchez', 'Laura Fernández', 'José González', 'Carmen Díaz'
    ]
    
    ventas_creadas = 0
    # Crear ventas de los últimos 30 días
    for producto in productos:
        # Crear entre 3 y 8 ventas por producto
        num_ventas = random.randint(3, 8)
        
        for _ in range(num_ventas):
            days_ago = random.randint(0, 30)
            sale_date = timezone.now() - timedelta(days=days_ago)
            quantity = random.randint(1, 5)
            
            sale = Sale.objects.create(
                product=producto,
                quantity_sold=quantity,
                unit_price=producto.selling_price,
                total_amount=producto.selling_price * quantity,
                sale_date=sale_date,
                customer_name=random.choice(clientes),
                notes=f'Venta procesada correctamente'
            )
            ventas_creadas += 1
    
    print(f"✅ {ventas_creadas} ventas creadas")
    return ventas_creadas

def crear_ordenes_compra(productos, proveedores):
    """Crear órdenes de compra de ejemplo"""
    print("\n📦 Creando órdenes de compra...")
    
    estados = ['PENDING', 'ORDERED', 'RECEIVED']
    ordenes_creadas = 0
    
    # Crear 2-3 órdenes por proveedor
    for proveedor in proveedores:
        num_ordenes = random.randint(2, 3)
        productos_proveedor = [p for p in productos if p.supplier == proveedor]
        
        for _ in range(num_ordenes):
            producto = random.choice(productos_proveedor)
            quantity = random.randint(20, 50)
            status = random.choice(estados)
            
            days_ago = random.randint(1, 15)
            order_date = timezone.now() - timedelta(days=days_ago)
            expected_delivery = order_date + timedelta(days=producto.lead_time_days)
            
            order = PurchaseOrder.objects.create(
                product=producto,
                supplier=proveedor,
                quantity_ordered=quantity,
                unit_cost=producto.cost_price,
                total_cost=producto.cost_price * quantity,
                status=status,
                order_date=order_date,
                expected_delivery=expected_delivery,
                received_date=expected_delivery if status == 'RECEIVED' else None,
                notes=f'Orden de reabastecimiento - {producto.name}'
            )
            ordenes_creadas += 1
    
    print(f"✅ {ordenes_creadas} órdenes de compra creadas")
    return ordenes_creadas

def main():
    print("🚀 Iniciando creación de datos de ejemplo...\n")
    
    # Crear datos
    print("📂 Creando categorías...")
    categorias = crear_categorias()
    
    print("\n🏢 Creando proveedores...")
    proveedores = crear_proveedores()
    
    print("\n📦 Creando productos...")
    productos = crear_productos(categorias, proveedores)
    
    crear_ventas(productos)
    crear_ordenes_compra(productos, proveedores)
    
    print("\n" + "="*60)
    print("✅ ¡DATOS DE EJEMPLO CREADOS EXITOSAMENTE!")
    print("="*60)
    print(f"📊 Resumen:")
    print(f"   - Categorías: {len(categorias)}")
    print(f"   - Proveedores: {len(proveedores)}")
    print(f"   - Productos: {len(productos)}")
    print(f"   - Ventas: Múltiples por producto")
    print(f"   - Órdenes de Compra: Múltiples por proveedor")
    print("\n🌐 Ahora puedes acceder al sistema en: http://127.0.0.1:8000/")

if __name__ == "__main__":
    main()

