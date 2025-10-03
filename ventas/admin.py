from django.contrib import admin
from .models import Venta
# Register your models here.
@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ('producto', 'cantidad_vendida', 'fecha_venta')
    list_filter = ('fecha_venta',)
    search_fields = ('producto__nombre',)