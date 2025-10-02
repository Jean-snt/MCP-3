from django.urls import path
from . import views
from . import advanced_views

urlpatterns = [
    # URLs originales
    path('', views.inicio, name='inicio'),
    path('consultar-ia/', views.consultar_inventario_ia, name='consultar_inventario_ia'),
    path('procesar-formulario/', views.procesar_formulario, name='procesar_formulario'),
    path('productos/', views.lista_productos, name='lista_productos'),
    
    # URLs avanzadas
    path('dashboard/', advanced_views.dashboard_view, name='dashboard'),
    path('analytics/', advanced_views.analytics_view, name='analytics'),
    path('predictions/', advanced_views.predictions_view, name='predictions'),
    path('train-models/', advanced_views.train_models_view, name='train_models'),
    path('alerts/', advanced_views.alerts_view, name='alerts'),
    path('generate-alerts/', advanced_views.generate_alerts_view, name='generate_alerts'),
    path('resolve-alert/<int:alert_id>/', advanced_views.resolve_alert_view, name='resolve_alert'),
    path('product/<int:product_id>/', advanced_views.product_detail_view, name='product_detail'),
    
    # APIs simples (JSON)
    path('api/analytics/', advanced_views.api_analytics_view, name='api_analytics'),
    path('api/predictions/', advanced_views.api_predictions_view, name='api_predictions'),
]
