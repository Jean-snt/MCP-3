from django.contrib import admin
from .models import Product, Supplier, Category, Sale, PurchaseOrder, InventoryAlert

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['name']

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['name', 'contact_person', 'email', 'phone', 'created_at']
    search_fields = ['name', 'contact_person', 'email']
    list_filter = ['created_at']
    ordering = ['name']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'sku', 'category', 'supplier', 'quantity', 
        'stock_status', 'selling_price', 'reorder_suggestion', 'updated_at'
    ]
    list_filter = [
        'category', 'supplier', 'reorder_suggestion', 'created_at', 'updated_at'
    ]
    search_fields = ['name', 'sku', 'description']
    readonly_fields = [
        'total_sold', 'last_sale_date', 'average_daily_sales',
        'predicted_demand_7d', 'predicted_demand_30d', 'stock_status', 'total_revenue',
        'profit_margin', 'days_of_supply'
    ]
    ordering = ['-updated_at']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('name', 'sku', 'description', 'category', 'supplier')
        }),
        ('Stock', {
            'fields': ('quantity', 'min_stock_level', 'max_stock_level', 'safety_stock')
        }),
        ('Precios', {
            'fields': ('cost_price', 'selling_price')
        }),
        ('Planificación', {
            'fields': ('lead_time_days', 'seasonality_index', 'promotion_active', 'current_discount')
        }),
        ('Métricas Calculadas', {
            'fields': ('stock_status', 'profit_margin', 'days_of_supply'),
            'classes': ('collapse',)
        }),
        ('Ventas', {
            'fields': ('total_sold', 'last_sale_date', 'average_daily_sales'),
            'classes': ('collapse',)
        }),
        ('Predicciones IA', {
            'fields': ('predicted_demand_7d', 'predicted_demand_30d', 'reorder_suggestion', 'reorder_quantity'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = [
        'product', 'quantity_sold', 'unit_price', 'total_amount', 
        'customer_name', 'sale_date'
    ]
    list_filter = ['sale_date', 'product__category']
    search_fields = ['product__name', 'customer_name', 'notes']
    readonly_fields = ['total_amount']
    ordering = ['-sale_date']
    date_hierarchy = 'sale_date'

@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'product', 'supplier', 'quantity_ordered', 'unit_cost', 
        'total_cost', 'status', 'order_date'
    ]
    list_filter = ['status', 'order_date', 'supplier']
    search_fields = ['product__name', 'supplier__name', 'notes']
    readonly_fields = ['total_cost']
    ordering = ['-order_date']
    date_hierarchy = 'order_date'

@admin.register(InventoryAlert)
class InventoryAlertAdmin(admin.ModelAdmin):
    list_display = [
        'product', 'alert_type', 'is_resolved', 'created_at', 'resolved_at'
    ]
    list_filter = ['alert_type', 'is_resolved', 'created_at']
    search_fields = ['product__name', 'message']
    readonly_fields = ['created_at', 'resolved_at']
    ordering = ['-created_at']
    
    actions = ['mark_as_resolved']
    
    def mark_as_resolved(self, request, queryset):
        from django.utils import timezone
        updated = queryset.update(is_resolved=True, resolved_at=timezone.now())
        self.message_user(request, f'{updated} alertas marcadas como resueltas.')
    mark_as_resolved.short_description = "Marcar como resueltas"