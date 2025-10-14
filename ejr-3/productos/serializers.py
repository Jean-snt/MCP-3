from rest_framework import serializers
from .models import Producto, Proveedor, Venta, MovimientoInventario


class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = '__all__'


class ProductoSerializer(serializers.ModelSerializer):
    proveedor_nombre = serializers.CharField(source='proveedor.nombre', read_only=True)
    necesita_reabastecimiento = serializers.BooleanField(read_only=True)
    margen_ganancia = serializers.DecimalField(max_digits=5, decimal_places=2, read_only=True)

    class Meta:
        model = Producto
        fields = '__all__'


class VentaSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.CharField(source='producto.nombre', read_only=True)
    total_venta = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Venta
        fields = '__all__'


class MovimientoInventarioSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.CharField(source='producto.nombre', read_only=True)

    class Meta:
        model = MovimientoInventario
        fields = '__all__'


class ProductoVentaSerializer(serializers.Serializer):
    producto_id = serializers.IntegerField()
    cantidad_vendida = serializers.IntegerField(min_value=1)
    precio_unitario = serializers.DecimalField(max_digits=10, decimal_places=2)
    cliente = serializers.CharField(required=False, allow_blank=True)
    notas = serializers.CharField(required=False, allow_blank=True)

    def validate_producto_id(self, value):
        try:
            producto = Producto.objects.get(id=value, activo=True)
            if producto.cantidad <= 0:
                raise serializers.ValidationError("El producto no tiene stock disponible")
            return value
        except Producto.DoesNotExist:
            raise serializers.ValidationError("Producto no encontrado o inactivo")

    def validate_cantidad_vendida(self, value):
        producto_id = self.initial_data.get('producto_id')
        if producto_id:
            try:
                producto = Producto.objects.get(id=producto_id)
                if value > producto.cantidad:
                    raise serializers.ValidationError(f"No hay suficiente stock. Disponible: {producto.cantidad}")
            except Producto.DoesNotExist:
                pass
        return value


class AnalisisInventarioSerializer(serializers.Serializer):
    productos_bajo_stock = serializers.ListField()
    productos_mas_vendidos = serializers.ListField()
    tendencias_ventas = serializers.DictField()
    sugerencias_reabastecimiento = serializers.ListField()
