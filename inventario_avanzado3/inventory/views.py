from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .models import Producto, Proveedor, Venta, HistorialInventario
from .serializers import ProductoSerializer, ProveedorSerializer, VentaSerializer, HistorialInventarioSerializer
from . import ai_logic


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = [AllowAny] # Permitir acceso sin autenticación
    
    @action(detail=True, methods=['get'])
    def restock_suggestion(self, request, pk=None):
        producto = self.get_object()
        sugerencia = ai_logic.suggest_restock(producto)
        return Response(sugerencia)

    @action(detail=True, methods=['get'])
    def stock_alert(self, request, pk=None):
        producto = self.get_object()
        if producto.stock_actual <= producto.punto_reorden:
            return Response({'alert': 'stock_bajo','stock_actual':producto.stock_actual})
        return Response({'alert':'ok','stock_actual':producto.stock_actual})

class ProveedorViewSet(viewsets.ModelViewSet):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer

class VentaViewSet(viewsets.ModelViewSet):
    queryset = Venta.objects.all().order_by('-fecha')
    serializer_class = VentaSerializer

class HistorialViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = HistorialInventario.objects.all().order_by('-fecha')
    serializer_class = HistorialInventarioSerializer

# API endpoint de predicciones
class PredictionsAPIView(APIView):
    def post(self, request):
        """
        Espera JSON: { "sku": "ABC123", "days": 30 }
        """
        sku = request.data.get('sku')
        days = int(request.data.get('days', 30))
        if not sku:
            return Response({"error":"sku requerido"}, status=400)
        # obtener ventas históricas del sku
        ventas = Venta.objects.filter(producto__sku=sku).order_by('fecha').values('fecha','cantidad')
        import pandas as pd
        if not ventas:
            return Response({"error":"No hay ventas para este SKU"}, status=404)
        df = pd.DataFrame(list(ventas))
        df = df.rename(columns={'fecha':'date','cantidad':'demand'})
        preds = ai_logic.predict_demand_for_sku(sku, df, days=days)
        return Response({'sku':sku,'predictions':preds})

# Analytics simple
@api_view(['GET'])
@permission_classes([AllowAny])
def analytics_endpoint(request):
    analytics = ai_logic.global_analytics()
    return Response(analytics)

# router
router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'providers', ProveedorViewSet)
router.register(r'sales', VentaViewSet)
router.register(r'history', HistorialViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('predictions/', PredictionsAPIView.as_view(), name='predictions'),
    path('analytics/', analytics_endpoint, name='analytics'),
]
