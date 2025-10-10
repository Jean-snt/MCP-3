import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta
import os
from .models import Product, Sale
from django.db.models import Sum, F

# Configuración de Vertex AI
try:
    import vertexai
    from vertexai.generative_models import GenerativeModel
    
    PROJECT_ID = "stone-poetry-473315-a9"
    LOCATION = "us-central1"
    
    # Inicializar Vertex AI
    vertexai.init(project=PROJECT_ID, location=LOCATION)
    
    # USAR gemini-2.5-flash como modelo principal
    modelo_nombre = "gemini-2.5-flash"
    
    try:
        print(f"🚀 Cargando modelo: {modelo_nombre}")
        modelo_ia = GenerativeModel(modelo_nombre)
        # Test rápido del modelo
        test_response = modelo_ia.generate_content("Responde 'CONECTADO'")
        VERTEX_AI_AVAILABLE = True
        MODELO_SELECCIONADO = modelo_nombre
        print(f"✅ {modelo_nombre} conectado correctamente")
        
    except Exception as e:
        print(f"❌ {modelo_nombre} no disponible: {e}")
        VERTEX_AI_AVAILABLE = False
        modelo_ia = None
        
except ImportError:
    VERTEX_AI_AVAILABLE = False
    modelo_ia = None
    MODELO_SELECCIONADO = None
    print("⚠️ Vertex AI no instalado")

def get_sales_data():
    """Obtiene datos de ventas para análisis"""
    sales = Sale.objects.all().select_related('product')
    
    if sales.count() < 3:
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
    """Obtiene sugerencias de IA usando gemini-2.5-flash"""
    if not VERTEX_AI_AVAILABLE:
        return {"error": "Vertex AI no disponible"}
    
    try:
        # Verificar datos mínimos
        if Sale.objects.count() < 2:
            return {"error": "Necesitas al menos 2 ventas para análisis"}
        
        # Obtener datos
        products = Product.objects.all()
        sales_data = get_sales_data()
        low_stock = [p for p in products if p.needs_restock()]
        
        # Preparar contexto
        contexto = f"""
        📊 ANÁLISIS DE INVENTARIO:

        📦 PRODUCTOS CON STOCK BAJO ({len(low_stock)}):
        {chr(10).join([f"• {p.name}: {p.quantity}/{p.min_stock} unidades" for p in low_stock])}

        🏪 INVENTARIO COMPLETO:
        {chr(10).join([f"• {p.name}: {p.quantity} unidades - ${p.selling_price}" for p in products])}

        📈 VENTAS REGISTRADAS: {Sale.objects.count()}
        """
        
        prompt = f"""
        Eres un experto en gestión de inventarios. Analiza esta situación y proporciona recomendaciones prácticas.
        
        {contexto}
        
        Responde en español con un análisis estructurado y recomendaciones accionables.
        """
        
        respuesta = modelo_ia.generate_content(prompt)
        
        return {
            "suggestions": respuesta.text,
            "modelo_usado": MODELO_SELECCIONADO,
        }
        
    except Exception as e:
        return {"error": f"Error en IA: {str(e)}"}

def get_basic_analysis():
    """Análisis básico siempre disponible"""
    try:
        products = Product.objects.all()
        sales = Sale.objects.all()
        
        return {
            "total_products": products.count(),
            "total_sales": sales.count(),
            "low_stock_products": [p for p in products if p.needs_restock()],
            "low_stock_count": len([p for p in products if p.needs_restock()]),
            "total_revenue": sum(float(s.quantity_sold * s.sale_price) for s in sales),
        }
    except Exception as e:
        return {"error": f"Error en análisis: {str(e)}"}