from rest_framework import serializers
from .models import Producto, Proveedor

class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = '__all__'

class ProductoSerializer(serializers.ModelSerializer):
    # Ahora puedes asignar proveedor por su ID
    proveedor = serializers.PrimaryKeyRelatedField(
        queryset=Proveedor.objects.all()
    )

    class Meta:
        model = Producto
        fields = '__all__'
