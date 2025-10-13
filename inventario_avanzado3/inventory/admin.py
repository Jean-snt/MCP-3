from django.contrib import admin
from .models import Proveedor, Producto, Venta, HistorialInventario

@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('nombre','email','telefono')

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('sku','nombre','stock_actual','punto_reorden','precio')

@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ('producto','cantidad','precio_unitario','total','fecha')

@admin.register(HistorialInventario)
class HistorialAdmin(admin.ModelAdmin):
    list_display = ('producto','cambio','motivo','fecha')
