from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import ProveedorViewSet, ProductoViewSet, VentaViewSet, AnalisisViewSet

router = DefaultRouter()
router.register(r'proveedores', ProveedorViewSet)
router.register(r'productos', ProductoViewSet)
router.register(r'ventas', VentaViewSet)
router.register(r'analisis', AnalisisViewSet, basename='analisis')

urlpatterns = [
    path('api/', include(router.urls)),
]
