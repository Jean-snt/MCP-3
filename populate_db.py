import os
import django
from datetime import datetime, timedelta
import random

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smart_inventory_project.settings')
django.setup()

from inventory.models import Supplier, Product, Sale

def populate_database():
    """Pobla la base de datos con datos de ejemplo"""
    
    # Limpiar datos existentes
    Sale.objects.all().delete()
    Product.objects.all().delete()
    Supplier.objects.all().delete()
    
    # Crear proveedores
    suppliers = [
        Supplier(name="TecnoSuministros S.A.", contact_email="contacto@tecnosuministros.com", 
                phone="+1-555-0101", address="Av. Tecnología 123, Ciudad Digital"),
        Supplier(name="Componentes Elite", contact_email="ventas@componenteselite.com", 
                phone="+1-555-0102", address="Calle Circuito 456, Zona Industrial"),
        Supplier(name="Gadgets Innovadores", contact_email="info@gadgetsinnovadores.com", 
                phone="+1-555-0103", address="Plaza Innovación 789, Distrito Tech")
    ]
    
    for supplier in suppliers:
        supplier.save()
    
    # Crear productos
    products_data = [
        {"name": "Teclado Mecánico RGB", "description": "Teclado mecánico gaming con retroiluminación RGB", "category": "Periféricos", "quantity": 15, "min_stock": 5, "max_stock": 50, "cost_price": 45.00, "selling_price": 89.99, "supplier": suppliers[0]},
        {"name": "Mouse Inalámbrico", "description": "Mouse ergonómico inalámbrico 16000 DPI", "category": "Periféricos", "quantity": 30, "min_stock": 10, "max_stock": 100, "cost_price": 25.00, "selling_price": 49.99, "supplier": suppliers[0]},
        {"name": "Monitor 24 Pulgadas", "description": "Monitor LED Full HD 1920x1080 75Hz", "category": "Monitores", "quantity": 8, "min_stock": 3, "max_stock": 20, "cost_price": 120.00, "selling_price": 199.99, "supplier": suppliers[1]},
        {"name": "Auriculares Gaming", "description": "Auriculares surround 7.1 con micrófono retráctil", "category": "Audio", "quantity": 0, "min_stock": 5, "max_stock": 30, "cost_price": 35.00, "selling_price": 69.99, "supplier": suppliers[2]},
        {"name": "Tablet Gráfica", "description": "Tablet digitalizadora para diseño gráfico", "category": "Creatividad", "quantity": 12, "min_stock": 4, "max_stock": 25, "cost_price": 80.00, "selling_price": 149.99, "supplier": suppliers[1]},
        {"name": "Webcam 4K", "description": "Cámara web 4K con micrófono integrado", "category": "Video", "quantity": 25, "min_stock": 8, "max_stock": 40, "cost_price": 40.00, "selling_price": 79.99, "supplier": suppliers[2]}
    ]
    
    products = []
    for product_data in products_data:
        product = Product(**product_data)
        product.save()
        products.append(product)
    
    # Crear ventas de ejemplo (últimos 90 días)
    for i in range(200):
        product = random.choice(products)
        days_ago = random.randint(0, 90)
        sale_date = datetime.now() - timedelta(days=days_ago)
        
        # No vender productos sin stock
        if product.quantity == 0:
            continue
            
        quantity = random.randint(1, min(5, product.quantity))
        
        sale = Sale(
            product=product,
            quantity_sold=quantity,
            sale_price=product.selling_price,
            sale_date=sale_date,
            customer_info=f"Cliente Ejemplo {random.randint(1000, 9999)}"
        )
        sale.save()
    
    print("✅ Base de datos poblada exitosamente!")
    print(f"   - {len(suppliers)} proveedores creados")
    print(f"   - {len(products)} productos creados")
    print(f"   - {Sale.objects.count()} ventas registradas")
    print(f"   - {len([p for p in products if p.needs_restock()])} productos necesitan reabastecimiento")

if __name__ == '__main__':
    populate_database()