from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class Proveedor(models.Model):
    nombre = models.CharField(max_length=100)
    contacto = models.CharField(max_length=100, blank=True)
    telefono = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    direccion = models.TextField(blank=True)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"


class Producto(models.Model):
    CATEGORIAS = [
        ('electronica', 'Electrónica'),
        ('ropa', 'Ropa'),
        ('hogar', 'Hogar'),
        ('deportes', 'Deportes'),
        ('libros', 'Libros'),
        ('alimentacion', 'Alimentación'),
        ('otros', 'Otros'),
    ]

    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    categoria = models.CharField(max_length=20, choices=CATEGORIAS, default='otros')
    cantidad = models.PositiveIntegerField(default=0)
    cantidad_minima = models.PositiveIntegerField(default=5, help_text="Cantidad mínima antes de alerta de reabastecimiento")
    precio_compra = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(Decimal('0.00'))])
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(Decimal('0.00'))])
    proveedor = models.ForeignKey(Proveedor, on_delete=models.SET_NULL, null=True, blank=True)
    codigo_barras = models.CharField(max_length=50, blank=True, unique=True, null=True)
    ubicacion = models.CharField(max_length=50, blank=True, help_text="Ubicación en el almacén")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} ({self.cantidad})"

    @property
    def necesita_reabastecimiento(self):
        return self.cantidad <= self.cantidad_minima

    @property
    def margen_ganancia(self):
        if self.precio_compra > 0:
            return ((self.precio_venta - self.precio_compra) / self.precio_compra) * 100
        return 0

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ['nombre']


class Venta(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad_vendida = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_venta = models.DateTimeField(auto_now_add=True)
    cliente = models.CharField(max_length=100, blank=True)
    notas = models.TextField(blank=True)

    def __str__(self):
        return f"{self.producto.nombre} - {self.cantidad_vendida} unidades - {self.fecha_venta.strftime('%Y-%m-%d')}"

    @property
    def total_venta(self):
        return self.cantidad_vendida * self.precio_unitario

    class Meta:
        verbose_name = "Venta"
        verbose_name_plural = "Ventas"
        ordering = ['-fecha_venta']


class MovimientoInventario(models.Model):
    TIPOS_MOVIMIENTO = [
        ('entrada', 'Entrada'),
        ('salida', 'Salida'),
        ('ajuste', 'Ajuste'),
    ]

    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    tipo_movimiento = models.CharField(max_length=10, choices=TIPOS_MOVIMIENTO)
    cantidad = models.IntegerField()  # Positivo para entrada, negativo para salida
    motivo = models.CharField(max_length=200)
    fecha_movimiento = models.DateTimeField(auto_now_add=True)
    usuario = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.producto.nombre} - {self.tipo_movimiento} - {self.cantidad}"

    class Meta:
        verbose_name = "Movimiento de Inventario"
        verbose_name_plural = "Movimientos de Inventario"
        ordering = ['-fecha_movimiento']

