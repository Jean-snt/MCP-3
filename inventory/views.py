import os
import django
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q, F, Sum
from .models import Product, Supplier, Sale
from .forms import ProductForm, SupplierForm, SaleForm
from .ai_logic import get_ai_suggestions, VERTEX_AI_AVAILABLE

# Vistas para Productos
def product_list(request):
    """Lista todos los productos"""
    products = Product.objects.all().order_by('name')
    low_stock_count = products.filter(quantity__lte=F('min_stock')).count()
    
    query = request.GET.get('q')
    if query:
        products = products.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query) |
            Q(category__icontains=query)
        )
    
    return render(request, 'inventory/product_list.html', {
        'products': products,
        'low_stock_count': low_stock_count,
        'query': query
    })

def product_create(request):
    """Crea un nuevo producto"""
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Producto creado exitosamente!')
            return redirect('product_list')
    else:
        form = ProductForm()
    
    return render(request, 'inventory/product_form.html', {
        'form': form, 
        'title': 'Crear Producto'
    })

def product_update(request, pk):
    """Actualiza un producto existente"""
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Producto actualizado exitosamente!')
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'inventory/product_form.html', {
        'form': form, 
        'title': 'Editar Producto'
    })

def product_delete(request, pk):
    """Elimina un producto"""
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        messages.success(request, '✅ Producto eliminado exitosamente!')
        return redirect('product_list')
    
    return render(request, 'inventory/product_confirm_delete.html', {
        'product': product
    })

# Vistas para Proveedores
def supplier_list(request):
    """Lista todos los proveedores"""
    suppliers = Supplier.objects.all().order_by('name')
    return render(request, 'inventory/supplier_list.html', {
        'suppliers': suppliers
    })

def supplier_create(request):
    """Crea un nuevo proveedor"""
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Proveedor creado exitosamente!')
            return redirect('supplier_list')
    else:
        form = SupplierForm()
    
    return render(request, 'inventory/supplier_form.html', {
        'form': form, 
        'title': 'Crear Proveedor'
    })

def supplier_update(request, pk):
    """Actualiza un proveedor existente"""
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Proveedor actualizado exitosamente!')
            return redirect('supplier_list')
    else:
        form = SupplierForm(instance=supplier)
    
    return render(request, 'inventory/supplier_form.html', {
        'form': form, 
        'title': 'Editar Proveedor'
    })

# Vistas para Ventas
def sale_list(request):
    """Lista todas las ventas"""
    sales = Sale.objects.all().order_by('-sale_date')
    return render(request, 'inventory/sale_list.html', {
        'sales': sales
    })

def sale_create(request):
    """Registra una nueva venta"""
    if request.method == 'POST':
        form = SaleForm(request.POST)
        if form.is_valid():
            sale = form.save(commit=False)
            # Actualizar stock del producto
            product = sale.product
            if sale.quantity_sold > product.quantity:
                messages.error(request, '❌ No hay suficiente stock para esta venta')
                return render(request, 'inventory/sale_form.html', {
                    'form': form, 
                    'title': 'Registrar Venta'
                })
            
            product.quantity -= sale.quantity_sold
            product.save()
            sale.save()
            
            messages.success(request, '✅ Venta registrada exitosamente!')
            return redirect('sale_list')
    else:
        form = SaleForm()
    
    return render(request, 'inventory/sale_form.html', {
        'form': form, 
        'title': 'Registrar Venta'
    })

# Vista para IA
def ai_analysis(request):
    """Muestra análisis de IA"""
    # Verificar si hay datos suficientes
    if Sale.objects.count() < 2:
        messages.warning(request, '⚠️ Necesitas registrar al menos 2 ventas para usar el análisis de IA')
        return redirect('sale_list')
    
    # Obtener sugerencias de IA
    suggestions = get_ai_suggestions()
    
    return render(request, 'inventory/ai_analysis.html', {
        'suggestions': suggestions,
        'total_sales': Sale.objects.count(),
        'total_products': Product.objects.count()
    })

# Vista de inicio (opcional - redirige a productos)
def home(request):
    """Página de inicio - redirige a la lista de productos"""
    return redirect('product_list')