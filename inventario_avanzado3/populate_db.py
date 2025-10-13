"""
Ejecutar: python inventory/populate_db.py
Crea proveedor, productos y ventas de ejemplo.
"""
import os, django, random
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smart_inventory_project.settings')
django.setup()

from inventory.models import Proveedor, Producto, Venta
from django.contrib.auth import get_user_model

User = get_user_model()

def run():
    prov, _ = Proveedor.objects.get_or_create(nombre='Proveedor Demo', email='demo@prov.com')
    p1, _ = Producto.objects.get_or_create(sku='P001', defaults={
        'nombre':'Producto 1', 'descripcion':'Demo', 'proveedor':prov, 'precio':10.0, 'stock_actual':50, 'punto_reorden':10
    })
    p2, _ = Producto.objects.get_or_create(sku='P002', defaults={
        'nombre':'Producto 2', 'descripcion':'Demo', 'proveedor':prov, 'precio':5.0, 'stock_actual':20, 'punto_reorden':5
    })
    # crear ventas aleatorias últimos 90 días
    now = datetime.utcnow()
    for product in [p1,p2]:
        for i in range(90):
            date = now - timedelta(days=90-i)
            # probabilidad de venta
            if random.random() < 0.6:
                qty = random.randint(1,5)
                Venta.objects.create(producto=product, cantidad=qty, precio_unitario=product.precio, fecha=date)
    print("Datos de ejemplo insertados.")

if __name__ == '__main__':
    run()
