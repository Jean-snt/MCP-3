from django.db import models


class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    cantidad = models.PositiveIntegerField(default=0)

    def __str__(self) -> str:
        return f"{self.nombre} ({self.cantidad})"

