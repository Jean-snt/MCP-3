from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Sum, Count, F
from django.utils import timezone
from datetime import timedelta
import json

from .models import Product, Sale, Supplier, Category, PurchaseOrder, InventoryAlert
from .ml_services import DemandPredictionService, ReorderSuggestionService, TrendAnalysisService

def dashboard_view(request):
    """Dashboard principal con métricas y análisis"""
    # Métricas básicas
    total_products = Product.objects.count()
    total_sales = Sale.objects.count()
    # Ingresos: usar ventas si existen; si no, fallback a ingresos acumulados en productos
    total_revenue = Sale.objects.aggregate(total=Sum('total_amount'))['total']
    if total_revenue is None:
        total_revenue = Product.objects.aggregate(total=Sum('total_revenue'))['total'] or 0
    
    # Productos por estado de stock
    low_stock_count = Product.objects.filter(
        quantity__lte=F('min_stock_level')
    ).count()
    
    need_reorder_count = Product.objects.filter(reorder_suggestion=True).count()
    
    # Ventas del último mes
    last_month = timezone.now() - timedelta(days=30)
    monthly_sales = Sale.objects.filter(sale_date__gte=last_month).count()
    monthly_revenue = Sale.objects.filter(sale_date__gte=last_month).aggregate(
        total=Sum('total_amount')
    )['total'] or 0
    
    # Top productos vendidos
    top_selling = Sale.objects.values('product__name').annotate(
        total_sold=Sum('quantity_sold'),
        total_revenue=Sum('total_amount')
    ).order_by('-total_sold')[:5]
    
    # Productos con stock bajo
    low_stock_products = Product.objects.filter(
        quantity__lte=F('min_stock_level')
    ).order_by('quantity')[:5]
    
    # Si no hay productos con stock bajo, mostrar top por stock como referencia
    if not low_stock_products.exists():
        low_stock_products = Product.objects.all().order_by('-quantity')[:5]

    # Alertas recientes
    recent_alerts = InventoryAlert.objects.filter(
        is_resolved=False
    ).order_by('-created_at')[:5]
    
    context = {
        'total_products': total_products,
        'total_sales': total_sales,
        'total_revenue': total_revenue,
        'low_stock_count': low_stock_count,
        'need_reorder_count': need_reorder_count,
        'monthly_sales': monthly_sales,
        'monthly_revenue': monthly_revenue,
        'top_selling': top_selling,
        'low_stock_products': low_stock_products,
        'recent_alerts': recent_alerts,
    }
    
    return render(request, 'inventario/dashboard.html', context)

def analytics_view(request):
    """Vista de análisis detallado"""
    # Análisis de tendencias
    analysis_service = TrendAnalysisService()
    trends = analysis_service.analyze_trends(30)
    # Fallback: si no hay ventas históricas, poblar "Top productos" con mayor stock
    try:
        if not trends.get('top_selling_products'):
            fallback = []
            for p in Product.objects.all().order_by('-quantity')[:10]:
                fallback.append({
                    'product__name': p.name,
                    'total_sold': p.total_sold or 0,
                    'total_revenue': 0,
                })
            trends['top_selling_products'] = fallback
    except Exception:
        pass
    
    # Productos por categoría
    products_by_category = Product.objects.values('category__name').annotate(
        count=Count('id'),
        total_stock=Sum('quantity')
    ).order_by('-count')
    
    # Ventas por mes (últimos 6 meses)
    six_months_ago = timezone.now() - timedelta(days=180)
    sales_by_month_qs = Sale.objects.filter(sale_date__gte=six_months_ago)
    if sales_by_month_qs.exists():
        sales_by_month = sales_by_month_qs.extra(
            select={'month': "strftime('%%Y-%%m', sale_date)"}
        ).values('month').annotate(
            total_sales=Sum('quantity_sold'),
            total_revenue=Sum('total_amount')
        ).order_by('month')
    else:
        # Fallback vacío con el mes actual para que la UI se vea poblada
        sales_by_month = []
    
    context = {
        'trends': trends,
        'products_by_category': products_by_category,
        'sales_by_month': sales_by_month,
    }
    
    return render(request, 'inventario/analytics.html', context)

def predictions_view(request):
    """Vista de predicciones de demanda"""
    prediction_service = DemandPredictionService()
    reorder_service = ReorderSuggestionService(prediction_service)
    
    # Obtener predicciones para todos los productos
    products = Product.objects.all()
    predictions = []
    
    for product in products:
        prediction_data = reorder_service.calculate_reorder_suggestion(product.id)
        if prediction_data:
            predictions.append(prediction_data)
    
    # Ordenar por prioridad (días de suministro)
    predictions.sort(key=lambda x: x['days_of_supply'])
    
    context = {
        'predictions': predictions,
        'total_products': len(predictions),
        'products_needing_reorder': len([p for p in predictions if p['needs_reorder']]),
    }
    
    return render(request, 'inventario/predictions.html', context)

def train_models_view(request):
    """Vista para entrenar modelos de ML"""
    if request.method == 'POST':
        prediction_service = DemandPredictionService()
        results = []
        
        products = Product.objects.all()
        for product in products:
            result = prediction_service.train_model(product.id)
            results.append({
                'product_id': product.id,
                'product_name': product.name,
                'success': result.get('success', False) if result else False,
                'metrics': result if result and result.get('success') else None
            })
        
        successful = len([r for r in results if r['success']])
        messages.success(
            request, 
            f'Entrenamiento completado: {successful}/{len(products)} modelos entrenados exitosamente'
        )
        
        return redirect('train_models')
    
    # Mostrar estado actual de los modelos
    products = Product.objects.all()
    model_status = []
    
    for product in products:
        # Verificar si existe modelo entrenado
        import os
        from django.conf import settings
        model_path = os.path.join(settings.BASE_DIR, 'ml_models', f'model_{product.id}.pkl')
        has_model = os.path.exists(model_path)
        
        model_status.append({
            'product': product,
            'has_model': has_model,
            'predicted_demand_7d': product.predicted_demand_7d,
            'predicted_demand_30d': product.predicted_demand_30d,
            'reorder_suggestion': product.reorder_suggestion,
        })
    
    context = {
        'model_status': model_status,
    }
    
    return render(request, 'inventario/train_models.html', context)

def alerts_view(request):
    """Vista de alertas de inventario"""
    alerts = InventoryAlert.objects.all().order_by('-created_at')
    
    # Filtros
    alert_type = request.GET.get('type')
    is_resolved = request.GET.get('resolved')
    
    if alert_type:
        alerts = alerts.filter(alert_type=alert_type)
    
    if is_resolved is not None:
        alerts = alerts.filter(is_resolved=is_resolved == 'true')
    
    context = {
        'alerts': alerts,
        'alert_types': InventoryAlert.ALERT_TYPES,
    }
    
    return render(request, 'inventario/alerts.html', context)

def generate_alerts_view(request):
    """Generar alertas automáticamente"""
    if request.method == 'POST':
        alerts_created = 0
        
        # Alerta de stock bajo
        low_stock_products = Product.objects.filter(
            quantity__lte=F('min_stock_level')
        )
        
        for product in low_stock_products:
            alert, created = InventoryAlert.objects.get_or_create(
                product=product,
                alert_type='LOW_STOCK',
                is_resolved=False,
                defaults={
                    'message': f'Stock bajo: {product.quantity} unidades (mínimo: {product.min_stock_level})'
                }
            )
            if created:
                alerts_created += 1
        
        # Alerta de productos sin stock
        out_of_stock_products = Product.objects.filter(quantity=0)
        
        for product in out_of_stock_products:
            alert, created = InventoryAlert.objects.get_or_create(
                product=product,
                alert_type='OUT_OF_STOCK',
                is_resolved=False,
                defaults={
                    'message': f'Producto sin stock: {product.name}'
                }
            )
            if created:
                alerts_created += 1
        
        # Alerta de stock alto
        high_stock_products = Product.objects.filter(
            quantity__gte=F('max_stock_level')
        )
        
        for product in high_stock_products:
            alert, created = InventoryAlert.objects.get_or_create(
                product=product,
                alert_type='HIGH_STOCK',
                is_resolved=False,
                defaults={
                    'message': f'Stock alto: {product.quantity} unidades (máximo: {product.max_stock_level})'
                }
            )
            if created:
                alerts_created += 1
        
        messages.success(request, f'{alerts_created} nuevas alertas generadas')
        
        return redirect('alerts')
    
    return redirect('alerts')

def resolve_alert_view(request, alert_id):
    """Resolver una alerta"""
    alert = get_object_or_404(InventoryAlert, id=alert_id)
    alert.is_resolved = True
    alert.resolved_at = timezone.now()
    alert.save()
    
    messages.success(request, f'Alerta "{alert.get_alert_type_display()}" marcada como resuelta')
    return redirect('alerts')

def product_detail_view(request, product_id):
    """Vista detallada de un producto con análisis"""
    product = get_object_or_404(Product, id=product_id)
    
    # Obtener ventas del producto
    sales = Sale.objects.filter(product=product).order_by('-sale_date')[:10]
    
    # Calcular métricas
    total_sales = Sale.objects.filter(product=product).aggregate(
        total=Sum('quantity_sold')
    )['total'] or 0
    
    total_revenue = Sale.objects.filter(product=product).aggregate(
        total=Sum('total_amount')
    )['total'] or (product.total_revenue or 0)
    
    # Predicciones
    prediction_service = DemandPredictionService()
    prediction_7d = prediction_service.predict_demand(product.id, 7)
    prediction_30d = prediction_service.predict_demand(product.id, 30)
    
    context = {
        'product': product,
        'sales': sales,
        'total_sales': total_sales,
        'total_revenue': total_revenue,
        'prediction_7d': prediction_7d,
        'prediction_30d': prediction_30d,
    }
    
    return render(request, 'inventario/product_detail.html', context)

def api_analytics_view(request):
    """API simple para obtener métricas (JSON)"""
    # Métricas básicas
    total_products = Product.objects.count()
    total_sales = Sale.objects.count()
    total_revenue = Sale.objects.aggregate(total=Sum('total_amount'))['total'] or 0
    
    # Productos por estado de stock
    low_stock_count = Product.objects.filter(
        quantity__lte=F('min_stock_level')
    ).count()
    
    need_reorder_count = Product.objects.filter(reorder_suggestion=True).count()
    
    # Ventas del último mes
    last_month = timezone.now() - timedelta(days=30)
    monthly_sales = Sale.objects.filter(sale_date__gte=last_month).count()
    monthly_revenue = Sale.objects.filter(sale_date__gte=last_month).aggregate(
        total=Sum('total_amount')
    )['total'] or 0
    
    data = {
        'total_products': total_products,
        'total_sales': total_sales,
        'total_revenue': float(total_revenue),
        'low_stock_products': low_stock_count,
        'products_needing_reorder': need_reorder_count,
        'monthly_sales': monthly_sales,
        'monthly_revenue': float(monthly_revenue),
        'analysis_date': timezone.now().isoformat()
    }
    
    return JsonResponse(data)

def api_predictions_view(request):
    """API simple para obtener predicciones (JSON)"""
    prediction_service = DemandPredictionService()
    reorder_service = ReorderSuggestionService(prediction_service)
    
    products = Product.objects.all()
    predictions = []
    
    for product in products:
        prediction_data = reorder_service.calculate_reorder_suggestion(product.id)
        if prediction_data:
            predictions.append(prediction_data)
    
    # Ordenar por prioridad
    predictions.sort(key=lambda x: x['days_of_supply'])
    
    data = {
        'predictions': predictions,
        'total_products': len(predictions),
        'products_needing_reorder': len([p for p in predictions if p['needs_reorder']]),
        'analysis_date': timezone.now().isoformat()
    }
    
    return JsonResponse(data)

