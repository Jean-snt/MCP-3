from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum, Count, Avg, Q, F
from django.utils import timezone
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from .models import Producto, Proveedor, Venta, MovimientoInventario
from .serializers import (
    ProductoSerializer, ProveedorSerializer, VentaSerializer, 
    MovimientoInventarioSerializer, ProductoVentaSerializer, AnalisisInventarioSerializer
)
from .ai_services import AIService


class ProveedorViewSet(viewsets.ModelViewSet):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer

    @action(detail=False, methods=['get'])
    def activos(self, request):
        """Obtener solo proveedores activos"""
        proveedores = self.queryset.filter(activo=True)
        serializer = self.get_serializer(proveedores, many=True)
        return Response(serializer.data)


class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

    @action(detail=False, methods=['get'])
    def bajo_stock(self, request):
        """Productos que necesitan reabastecimiento"""
        productos = self.queryset.filter(cantidad__lte=models.F('cantidad_minima'))
        serializer = self.get_serializer(productos, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def por_categoria(self, request):
        """Productos agrupados por categoría"""
        categoria = request.query_params.get('categoria')
        if categoria:
            productos = self.queryset.filter(categoria=categoria)
        else:
            productos = self.queryset.all()
        serializer = self.get_serializer(productos, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def registrar_venta(self, request, pk=None):
        """Registrar una venta para un producto"""
        producto = self.get_object()
        serializer = ProductoVentaSerializer(data=request.data)
        
        if serializer.is_valid():
            cantidad_vendida = serializer.validated_data['cantidad_vendida']
            precio_unitario = serializer.validated_data['precio_unitario']
            cliente = serializer.validated_data.get('cliente', '')
            notas = serializer.validated_data.get('notas', '')

            # Crear la venta
            venta = Venta.objects.create(
                producto=producto,
                cantidad_vendida=cantidad_vendida,
                precio_unitario=precio_unitario,
                cliente=cliente,
                notas=notas
            )

            # Actualizar stock
            producto.cantidad -= cantidad_vendida
            producto.save()

            # Registrar movimiento
            MovimientoInventario.objects.create(
                producto=producto,
                tipo_movimiento='salida',
                cantidad=-cantidad_vendida,
                motivo=f"Venta - Cliente: {cliente}",
                usuario=request.user.username if hasattr(request, 'user') else 'API'
            )

            return Response({
                'mensaje': 'Venta registrada exitosamente',
                'venta_id': venta.id,
                'stock_actual': producto.cantidad
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def ajustar_stock(self, request, pk=None):
        """Ajustar el stock de un producto"""
        producto = self.get_object()
        cantidad = request.data.get('cantidad')
        motivo = request.data.get('motivo', 'Ajuste manual')
        
        if cantidad is None:
            return Response({'error': 'Cantidad requerida'}, status=status.HTTP_400_BAD_REQUEST)

        # Determinar tipo de movimiento
        if cantidad > 0:
            tipo_movimiento = 'entrada'
        else:
            tipo_movimiento = 'salida'

        # Registrar movimiento
        MovimientoInventario.objects.create(
            producto=producto,
            tipo_movimiento=tipo_movimiento,
            cantidad=cantidad,
            motivo=motivo,
            usuario=request.user.username if hasattr(request, 'user') else 'API'
        )

        # Actualizar stock
        producto.cantidad += cantidad
        if producto.cantidad < 0:
            producto.cantidad = 0
        producto.save()

        return Response({
            'mensaje': 'Stock ajustado exitosamente',
            'stock_actual': producto.cantidad
        })


class VentaViewSet(viewsets.ModelViewSet):
    queryset = Venta.objects.all()
    serializer_class = VentaSerializer

    @action(detail=False, methods=['get'])
    def por_periodo(self, request):
        """Ventas en un período específico"""
        fecha_inicio = request.query_params.get('fecha_inicio')
        fecha_fin = request.query_params.get('fecha_fin')
        
        if fecha_inicio and fecha_fin:
            try:
                fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d')
                fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d')
                ventas = self.queryset.filter(
                    fecha_venta__date__range=[fecha_inicio.date(), fecha_fin.date()]
                )
            except ValueError:
                return Response({'error': 'Formato de fecha inválido'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            # Últimos 30 días por defecto
            fecha_fin = timezone.now()
            fecha_inicio = fecha_fin - timedelta(days=30)
            ventas = self.queryset.filter(fecha_venta__gte=fecha_inicio)

        serializer = self.get_serializer(ventas, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def resumen_ventas(self, request):
        """Resumen estadístico de ventas"""
        ventas = self.queryset.all()
        
        resumen = {
            'total_ventas': ventas.count(),
            'total_ingresos': sum(venta.total_venta for venta in ventas),
            'promedio_venta': ventas.aggregate(avg=Avg('precio_unitario'))['avg'] or 0,
            'producto_mas_vendido': ventas.values('producto__nombre').annotate(
                total=Sum('cantidad_vendida')
            ).order_by('-total').first()
        }
        
        return Response(resumen)


class AnalisisViewSet(viewsets.ViewSet):
    """ViewSet para análisis de inventario y predicciones"""

    @action(detail=False, methods=['get'])
    def dashboard(self, request):
        """Datos para el dashboard principal"""
        # Productos que necesitan reabastecimiento
        productos_bajo_stock = Producto.objects.filter(
            cantidad__lte=models.F('cantidad_minima')
        ).values('id', 'nombre', 'cantidad', 'cantidad_minima')

        # Productos más vendidos (últimos 30 días)
        fecha_limite = timezone.now() - timedelta(days=30)
        productos_mas_vendidos = Venta.objects.filter(
            fecha_venta__gte=fecha_limite
        ).values('producto__nombre').annotate(
            total_vendido=Sum('cantidad_vendida')
        ).order_by('-total_vendido')[:10]

        # Ventas por día (últimos 7 días)
        ventas_por_dia = []
        for i in range(7):
            fecha = timezone.now().date() - timedelta(days=i)
            ventas_dia = Venta.objects.filter(fecha_venta__date=fecha).aggregate(
                total=Sum('cantidad_vendida')
            )['total'] or 0
            ventas_por_dia.append({
                'fecha': fecha.strftime('%Y-%m-%d'),
                'ventas': ventas_dia
            })

        return Response({
            'productos_bajo_stock': list(productos_bajo_stock),
            'productos_mas_vendidos': list(productos_mas_vendidos),
            'ventas_por_dia': ventas_por_dia
        })

    @action(detail=False, methods=['get'])
    def prediccion_demanda(self, request):
        """Predicción de demanda usando IA"""
        producto_id = request.query_params.get('producto_id')
        dias_prediccion = int(request.query_params.get('dias', 7))
        
        if not producto_id:
            return Response({'error': 'producto_id requerido'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            producto = Producto.objects.get(id=producto_id)
            ai_service = AIService()
            prediccion = ai_service.predecir_demanda(producto, dias_prediccion)
            return Response(prediccion)
        except Producto.DoesNotExist:
            return Response({'error': 'Producto no encontrado'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['get'])
    def tendencias(self, request):
        """Análisis de tendencias de ventas"""
        ai_service = AIService()
        tendencias = ai_service.analizar_tendencias()
        return Response(tendencias)

    @action(detail=False, methods=['get'])
    def sugerencias_reabastecimiento(self, request):
        """Sugerencias inteligentes de reabastecimiento"""
        ai_service = AIService()
        sugerencias = ai_service.generar_sugerencias_reabastecimiento()
        return Response(sugerencias)
