from django.shortcuts import render

# Create your views here.
# productos/views.py
from rest_framework import viewsets
from .models import Producto, Proveedor
from .serializers import ProductoSerializer, ProveedorSerializer

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

class ProveedorViewSet(viewsets.ModelViewSet):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer
