from rest_framework import serializers
from .models import Proveedor, Producto, Venta, HistorialInventario

class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = '__all__'

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'

class VentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venta
        fields = '__all__'

class HistorialInventarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistorialInventario
        fields = '__all__'
