from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Producto
from .forms import ProductoForm


class ProductoListView(ListView):
    model = Producto
    template_name = "productos/lista.html"
    context_object_name = "productos"
    ordering = ["nombre"]


class ProductoCreateView(CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = "productos/form.html"
    success_url = reverse_lazy("productos:lista")


class ProductoUpdateView(UpdateView):
    model = Producto
    form_class = ProductoForm
    template_name = "productos/form.html"
    success_url = reverse_lazy("productos:lista")


class ProductoDeleteView(DeleteView):
    model = Producto
    template_name = "productos/confirmar_eliminar.html"
    success_url = reverse_lazy("productos:lista")

