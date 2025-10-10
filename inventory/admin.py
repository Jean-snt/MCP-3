from django.contrib import admin
from .models import Supplier, Product, Sale

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['name', 'contact_email', 'phone', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'contact_email']
    ordering = ['name']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'quantity', 'min_stock', 'selling_price', 'supplier', 'needs_restock']
    list_filter = ['category', 'supplier', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['quantity', 'min_stock', 'selling_price']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['name']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('name', 'description', 'category', 'supplier')
        }),
        ('Inventario', {
            'fields': ('quantity', 'min_stock', 'max_stock')
        }),
        ('Precios', {
            'fields': ('cost_price', 'selling_price')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def needs_restock(self, obj):
        return obj.quantity <= obj.min_stock
    needs_restock.boolean = True
    needs_restock.short_description = '¿Necesita Stock?'

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ['product', 'quantity_sold', 'sale_price', 'total_revenue', 'sale_date']
    list_filter = ['sale_date', 'product']
    search_fields = ['product__name', 'customer_info']
    readonly_fields = ['sale_date']
    date_hierarchy = 'sale_date'
    
    def total_revenue(self, obj):
        return f"${obj.quantity_sold * obj.sale_price:.2f}"
    total_revenue.short_description = 'Ingreso Total'