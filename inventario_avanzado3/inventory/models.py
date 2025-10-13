from django.db import models, transaction
from django.db.models import F
from django.contrib.auth import get_user_model

User = get_user_model()

class Proveedor(models.Model):
    nombre = models.CharField(max_length=200)
    email = models.EmailField(blank=True, null=True)
    telefono = models.CharField(max_length=50, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    def __str__(self): return self.nombre

class Producto(models.Model):
    sku = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.SET_NULL, null=True, blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock_actual = models.IntegerField(default=0)
    punto_reorden = models.IntegerField(default=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self): return f"{self.sku} - {self.nombre}"

class Venta(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT, related_name='ventas')
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    fecha = models.DateTimeField()
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.total is None:
            self.total = self.cantidad * self.precio_unitario
        with transaction.atomic():
            if not self.pk:
                # descontar stock de forma segura
                Producto.objects.filter(pk=self.producto.pk).update(stock_actual=F('stock_actual') - self.cantidad)
            super().save(*args, **kwargs)
            # registrar en historial
            HistorialInventario.objects.create(
                producto=self.producto,
                cambio=-self.cantidad,
                motivo='Venta',
                usuario=self.usuario
            )

class HistorialInventario(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='historial')
    cambio = models.IntegerField()  # + entrada, - salida
    motivo = models.CharField(max_length=200, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
        return f"{self.producto.sku} {self.cambio} ({self.motivo})"
