from django.contrib import admin
from .models import Producto, Proveedor, Venta, MovimientoInventario


@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ("nombre", "contacto", "telefono", "email", "activo")
    search_fields = ("nombre", "contacto", "email")
    list_filter = ("activo", "fecha_creacion")
    ordering = ("nombre",)


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "categoria", "cantidad", "cantidad_minima", "precio_venta", "necesita_reabastecimiento", "activo")
    search_fields = ("nombre", "codigo_barras", "descripcion")
    list_filter = ("categoria", "activo", "proveedor")
    ordering = ("nombre",)
    fieldsets = (
        ("Información Básica", {
            "fields": ("nombre", "descripcion", "categoria", "codigo_barras")
        }),
        ("Inventario", {
            "fields": ("cantidad", "cantidad_minima", "ubicacion")
        }),
        ("Precios", {
            "fields": ("precio_compra", "precio_venta")
        }),
        ("Proveedor", {
            "fields": ("proveedor",)
        }),
        ("Estado", {
            "fields": ("activo",)
        }),
    )


@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ("producto", "cantidad_vendida", "precio_unitario", "total_venta", "fecha_venta", "cliente")
    search_fields = ("producto__nombre", "cliente")
    list_filter = ("fecha_venta", "producto__categoria")
    ordering = ("-fecha_venta",)
    date_hierarchy = "fecha_venta"


@admin.register(MovimientoInventario)
class MovimientoInventarioAdmin(admin.ModelAdmin):
    list_display = ("producto", "tipo_movimiento", "cantidad", "motivo", "fecha_movimiento", "usuario")
    search_fields = ("producto__nombre", "motivo", "usuario")
    list_filter = ("tipo_movimiento", "fecha_movimiento")
    ordering = ("-fecha_movimiento",)
    date_hierarchy = "fecha_movimiento"




