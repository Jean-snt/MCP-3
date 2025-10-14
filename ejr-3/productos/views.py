from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.db.models import Count, Sum, F
from .models import Producto, Proveedor, Venta
from .forms import ProductoForm


class DashboardView(TemplateView):
    template_name = "dashboard.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Estadísticas generales
        context['total_productos'] = Producto.objects.count()
        context['total_proveedores'] = Proveedor.objects.count()
        context['total_ventas'] = Venta.objects.count()
        
        # Productos con stock bajo
        context['productos_bajo_stock'] = Producto.objects.filter(
            cantidad__lte=F('cantidad_minima')
        ).count()
        
        # Productos agotados
        context['productos_agotados'] = Producto.objects.filter(cantidad=0).count()
        
        # Productos recientes
        context['productos_recientes'] = Producto.objects.order_by('-id')[:5]
        
        # Ventas recientes
        context['ventas_recientes'] = Venta.objects.order_by('-fecha_venta')[:5]
        
        # Categorías más populares
        context['categorias_populares'] = Producto.objects.values('categoria').annotate(
            count=Count('id')
        ).order_by('-count')[:5]
        
        return context


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

