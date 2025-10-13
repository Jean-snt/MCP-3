from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views

router = DefaultRouter()
router.register(r'products', views.ProductViewSet)
router.register(r'providers', views.ProveedorViewSet)
router.register(r'sales', views.VentaViewSet)
router.register(r'history', views.HistorialViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('predictions/', views.PredictionsAPIView.as_view(), name='predictions'),
    path('analytics/', views.analytics_endpoint, name='analytics'),
]
