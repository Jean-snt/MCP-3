import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta
import os
from .models import Product, Sale
from django.db.models import Sum, F

# Intentar importar Vertex AI con manejo de errores
try:
    import vertexai
    from vertexai.generative_models import GenerativeModel
    
    # Configuración de Vertex AI
    PROJECT_ID = "stone-poetry-473315-a9"
    LOCATION = "us-central1"
    
    # Inicializar Vertex AI
    vertexai.init(project=PROJECT_ID, location=LOCATION)
    modelo_ia = GenerativeModel("gemini-2.5-flash")
    VERTEX_AI_AVAILABLE = True
    
except ImportError:
    VERTEX_AI_AVAILABLE = False
    modelo_ia = None
    print("⚠️ Vertex AI no está disponible. Las funciones de IA no estarán activas.")

def get_sales_data():
    """Obtiene datos de ventas para análisis"""
    sales = Sale.objects.all().select_related('product')
    
    if sales.count() < 5:
        return pd.DataFrame()
    
    data = []
    for sale in sales:
        data.append({
            'date': sale.sale_date,
            'product_name': sale.product.name,
            'quantity_sold': sale.quantity_sold,
            'revenue': float(sale.quantity_sold * sale.sale_price),
        })
    
    return pd.DataFrame(data)

def get_ai_suggestions():
    """Obtiene sugerencias de IA basadas en datos existentes"""
    # Verificar si Vertex AI está disponible
    if not VERTEX_AI_AVAILABLE:
        return {"error": "Vertex AI no está configurado. Ejecuta: pip install google-cloud-aiplatform"}
    
    try:
        # Verificar datos mínimos
        if Sale.objects.count() < 5:
            return {"error": "Se necesitan al menos 5 ventas registradas para generar análisis"}
        
        # Obtener datos actuales
        products = Product.objects.all()
        sales_data = get_sales_data()
        
        # Preparar contexto para IA
        low_stock_products = [p for p in products if p.needs_restock()]
        
        # Construir el texto de productos con stock bajo
        low_stock_text = "\n".join([
            f"- {p.name}: Stock actual {p.quantity}, Mínimo requerido {p.min_stock}"
            for p in low_stock_products
        ])
        
        # Construir el texto de ventas
        if not sales_data.empty:
            sales_summary = sales_data.groupby('product_name')['quantity_sold'].sum().to_dict()
            sales_text = "\n".join([
                f"- {product}: {quantity} unidades" 
                for product, quantity in sales_summary.items()
            ])
        else:
            sales_text = "No hay datos de ventas suficientes"
        
        # Construir el texto de productos disponibles
        products_text = "\n".join([
            f"- {product.name}: {product.quantity} unidades, Precio: ${product.selling_price}"
            for product in products
        ])
        
        # Crear el contexto formateado
        contexto_formateado = f"""
        INFORMACIÓN DEL INVENTARIO:
        
        Productos con stock bajo ({len(low_stock_products)}):
        {low_stock_text}
        
        Ventas registradas ({len(sales_data)}):
        {sales_text}
        
        PRODUCTOS DISPONIBLES:
        {products_text}
        """
        
        # Plantilla del prompt
        plantilla_prompt = """
        Contexto:
        {contexto_formateado}

        Instrucciones:
        Eres un asistente especializado en gestión de inventarios. 
        Analiza los datos del inventario y proporciona sugerencias prácticas y específicas.

        Requisitos:
        - El análisis debe basarse en los datos proporcionados
        - Debe ser práctico y accionable
        - Incluye recomendaciones específicas para reabastecimiento
        - Sugiere optimizaciones basadas en el historial de ventas
        - Responde en español con un análisis claro

        Genera exactamente UN análisis con recomendaciones específicas.
        """
        
        prompt_final = plantilla_prompt.format(contexto_formateado=contexto_formateado)
        
        # Generar respuesta usando Vertex AI
        respuesta = modelo_ia.generate_content(prompt_final)
        
        return {"suggestions": respuesta.text}
        
    except Exception as e:
        return {"error": f"Error en análisis de IA: {str(e)}"}

# Función adicional para análisis básico sin IA
def get_basic_analysis():
    """Análisis básico sin IA"""
    try:
        products = Product.objects.all()
        sales = Sale.objects.all()
        
        analysis = {
            "total_products": products.count(),
            "total_sales": sales.count(),
            "low_stock_products": [p.name for p in products if p.needs_restock()],
            "total_revenue": sum(float(sale.quantity_sold * sale.sale_price) for sale in sales),
            "top_products": list(Sale.objects.values('product__name')
                                .annotate(total_sold=Sum('quantity_sold'))
                                .order_by('-total_sold')[:3])
        }
        
        return analysis
        
    except Exception as e:
        return {"error": f"Error en análisis básico: {str(e)}"}