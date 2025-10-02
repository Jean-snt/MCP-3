from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal

class Supplier(models.Model):
    """Modelo para proveedores"""
    name = models.CharField(max_length=200, verbose_name="Nombre del Proveedor")
    contact_person = models.CharField(max_length=100, verbose_name="Persona de Contacto")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=20, verbose_name="Teléfono")
    address = models.TextField(verbose_name="Dirección")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"

class Category(models.Model):
    """Modelo para categorías de productos"""
    name = models.CharField(max_length=100, verbose_name="Nombre de Categoría")
    description = models.TextField(blank=True, verbose_name="Descripción")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"

class Product(models.Model):
    """Modelo expandido para productos con más campos para análisis"""
    name = models.CharField(max_length=100, verbose_name="Nombre del Producto")
    description = models.TextField(blank=True, verbose_name="Descripción")
    sku = models.CharField(max_length=50, unique=True, verbose_name="SKU", default="SKU-000")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Categoría")
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Proveedor")
    
    # Información de stock
    quantity = models.IntegerField(default=0, verbose_name="Cantidad en Stock")
    min_stock_level = models.IntegerField(default=10, verbose_name="Stock Mínimo")
    max_stock_level = models.IntegerField(default=100, verbose_name="Stock Máximo")
    
    # Información financiera
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Precio de Costo")
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Precio de Venta")
    
    # Operación y planificación
    lead_time_days = models.IntegerField(default=7, verbose_name="Lead time (días)")
    safety_stock = models.IntegerField(default=0, verbose_name="Stock de seguridad")
    seasonality_index = models.FloatField(default=1.0, validators=[MinValueValidator(0.1), MaxValueValidator(3.0)], verbose_name="Índice de estacionalidad")

    # Promociones
    promotion_active = models.BooleanField(default=False, verbose_name="Promoción activa")
    current_discount = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name="Descuento actual (%)")

    # Métricas para análisis
    total_sold = models.IntegerField(default=0, verbose_name="Total Vendido")
    last_sale_date = models.DateTimeField(null=True, blank=True, verbose_name="Última Venta")
    average_daily_sales = models.FloatField(default=0.0, verbose_name="Ventas Diarias Promedio")
    total_revenue = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'), verbose_name="Ingresos Acumulados")
    
    # Predicciones de IA
    predicted_demand_7d = models.FloatField(default=0.0, verbose_name="Demanda Predicha 7 días")
    predicted_demand_30d = models.FloatField(default=0.0, verbose_name="Demanda Predicha 30 días")
    reorder_suggestion = models.BooleanField(default=False, verbose_name="Sugerencia de Reorden")
    reorder_quantity = models.IntegerField(default=0, verbose_name="Cantidad Sugerida")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} (SKU: {self.sku})"
    
    @property
    def stock_status(self):
        """Determina el estado del stock"""
        if self.quantity <= self.min_stock_level:
            return "CRITICO"
        elif self.quantity <= self.min_stock_level * 1.5:
            return "BAJO"
        elif self.quantity >= self.max_stock_level:
            return "ALTO"
        else:
            return "NORMAL"
    
    @property
    def profit_margin(self):
        """Calcula el margen de ganancia"""
        if self.cost_price > 0:
            return ((self.selling_price - self.cost_price) / self.cost_price) * 100
        return 0
    
    @property
    def days_of_supply(self):
        """Calcula cuántos días de suministro quedan"""
        if self.average_daily_sales > 0:
            return self.quantity / self.average_daily_sales
        return float('inf')
    
    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ['-updated_at']

class Sale(models.Model):
    """Modelo para registrar ventas"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Producto")
    quantity_sold = models.IntegerField(validators=[MinValueValidator(1)], verbose_name="Cantidad Vendida")
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio Unitario")
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Monto Total")
    sale_date = models.DateTimeField(default=timezone.now, verbose_name="Fecha de Venta")
    customer_name = models.CharField(max_length=200, blank=True, verbose_name="Nombre del Cliente")
    notes = models.TextField(blank=True, verbose_name="Notas")
    
    def save(self, *args, **kwargs):
        # Calcular el monto total automáticamente
        self.total_amount = self.quantity_sold * self.unit_price
        
        # Actualizar métricas del producto
        self.product.quantity -= self.quantity_sold
        self.product.total_sold += self.quantity_sold
        self.product.last_sale_date = self.sale_date
        # Actualizar ingresos acumulados
        try:
            self.product.total_revenue = (self.product.total_revenue or Decimal('0.00')) + self.total_amount
        except Exception:
            self.product.total_revenue = self.total_amount
        
        super().save(*args, **kwargs)
        self.product.save()
    
    def __str__(self):
        return f"Venta de {self.quantity_sold} {self.product.name} - ${self.total_amount}"
    
    class Meta:
        verbose_name = "Venta"
        verbose_name_plural = "Ventas"
        ordering = ['-sale_date']

class PurchaseOrder(models.Model):
    """Modelo para órdenes de compra"""
    STATUS_CHOICES = [
        ('PENDING', 'Pendiente'),
        ('ORDERED', 'Ordenado'),
        ('RECEIVED', 'Recibido'),
        ('CANCELLED', 'Cancelado'),
    ]
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Producto")
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, verbose_name="Proveedor")
    quantity_ordered = models.IntegerField(validators=[MinValueValidator(1)], verbose_name="Cantidad Ordenada")
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Costo Unitario")
    total_cost = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Costo Total")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING', verbose_name="Estado")
    order_date = models.DateTimeField(default=timezone.now, verbose_name="Fecha de Orden")
    expected_delivery = models.DateTimeField(null=True, blank=True, verbose_name="Entrega Esperada")
    received_date = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Recepción")
    notes = models.TextField(blank=True, verbose_name="Notas")
    
    def save(self, *args, **kwargs):
        # Calcular el costo total automáticamente
        self.total_cost = self.quantity_ordered * self.unit_cost
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Orden {self.id}: {self.quantity_ordered} {self.product.name} - {self.get_status_display()}"
    
    class Meta:
        verbose_name = "Orden de Compra"
        verbose_name_plural = "Órdenes de Compra"
        ordering = ['-order_date']

class InventoryAlert(models.Model):
    """Modelo para alertas de inventario"""
    ALERT_TYPES = [
        ('LOW_STOCK', 'Stock Bajo'),
        ('OUT_OF_STOCK', 'Sin Stock'),
        ('HIGH_STOCK', 'Stock Alto'),
        ('REORDER_SUGGESTION', 'Sugerencia de Reorden'),
        ('PREDICTED_SHORTAGE', 'Escasez Predicha'),
    ]
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Producto")
    alert_type = models.CharField(max_length=30, choices=ALERT_TYPES, verbose_name="Tipo de Alerta")
    message = models.TextField(verbose_name="Mensaje")
    is_resolved = models.BooleanField(default=False, verbose_name="Resuelto")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    resolved_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Resolución")
    
    def __str__(self):
        return f"{self.get_alert_type_display()} - {self.product.name}"
    
    class Meta:
        verbose_name = "Alerta de Inventario"
        verbose_name_plural = "Alertas de Inventario"
        ordering = ['-created_at']