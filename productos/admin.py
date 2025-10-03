from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Producto, Proveedor

@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ("nombre", "contacto", "telefono")

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "descripcion", "cantidad", "precio_venta", "proveedor")
    list_filter = ("proveedor",)
    search_fields = ("nombre", "descripcion")
