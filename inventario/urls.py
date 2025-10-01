from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('consultar-ia/', views.consultar_inventario_ia, name='consultar_inventario_ia'),
    path('procesar-formulario/', views.procesar_formulario, name='procesar_formulario'),
    path('productos/', views.lista_productos, name='lista_productos'),
]
