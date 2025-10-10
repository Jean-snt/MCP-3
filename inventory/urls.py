from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='home'),path('', views.product_list, name='home'),
    # Productos
    path('products/', views.product_list, name='product_list'),
    path('products/new/', views.product_create, name='product_create'),
    path('products/<int:pk>/edit/', views.product_update, name='product_update'),
    path('products/<int:pk>/delete/', views.product_delete, name='product_delete'),
    
    # Proveedores
    path('suppliers/', views.supplier_list, name='supplier_list'),
    path('suppliers/new/', views.supplier_create, name='supplier_create'),
    path('suppliers/<int:pk>/edit/', views.supplier_update, name='supplier_update'),
    
    # Ventas
    path('sales/', views.sale_list, name='sale_list'),
    path('sales/new/', views.sale_create, name='sale_create'),
    
    # IA (separada)
    path('ai-analysis/', views.ai_analysis, name='ai_analysis'),
    
    # Home
    path('', views.product_list, name='home'),
]