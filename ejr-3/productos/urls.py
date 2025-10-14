from django.urls import path
from .views import (
    DashboardView,
    ProductoListView,
    ProductoCreateView,
    ProductoUpdateView,
    ProductoDeleteView,
)

app_name = "productos"

urlpatterns = [
    path("", DashboardView.as_view(), name="dashboard"),
    path("productos/", ProductoListView.as_view(), name="lista"),
    path("nuevo/", ProductoCreateView.as_view(), name="crear"),
    path("<int:pk>/editar/", ProductoUpdateView.as_view(), name="editar"),
    path("<int:pk>/eliminar/", ProductoDeleteView.as_view(), name="eliminar"),
]

