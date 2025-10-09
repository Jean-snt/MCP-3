#!/usr/bin/env python3
"""
Ejemplo de uso del Sistema de Inventario Inteligente
Demuestra las principales funcionalidades del sistema
"""

import os
import django
import requests
import json
from datetime import datetime, timedelta

# Configurar Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "inventario_project.settings")
django.setup()

from productos.models import Producto, Venta, Proveedor
from productos.ai_services import AIService
from django.db.models import F, Sum

def ejemplo_consulta_basica():
    """Ejemplo de consulta básica del inventario"""
    print("=" * 60)
    print("📦 EJEMPLO: Consulta Básica del Inventario")
    print("=" * 60)
    
    # Obtener productos disponibles
    productos = Producto.objects.filter(cantidad__gt=0).order_by('nombre')
    
    print(f"Total de productos disponibles: {productos.count()}")
    print("\nProductos en stock:")
    for producto in productos[:10]:  # Mostrar solo los primeros 10
        print(f"• {producto.nombre}: {producto.cantidad} unidades (${producto.precio_venta})")
    
    if productos.count() > 10:
        print(f"... y {productos.count() - 10} productos más")

def ejemplo_analisis_ia():
    """Ejemplo de análisis con IA"""
    print("\n" + "=" * 60)
    print("🤖 EJEMPLO: Análisis con Inteligencia Artificial")
    print("=" * 60)
    
    ai_service = AIService()
    
    # Obtener producto con más ventas para análisis
    producto_popular = Venta.objects.values('producto').annotate(
        total_vendido=Sum('cantidad_vendida')
    ).order_by('-total_vendido').first()
    
    if producto_popular:
        producto = Producto.objects.get(id=producto_popular['producto'])
        print(f"Analizando producto: {producto.nombre}")
        
        # Predicción de demanda
        print("\n🔮 Predicción de Demanda:")
        prediccion = ai_service.predecir_demanda(producto, 7)
        print(f"Confianza: {prediccion['confianza']}%")
        print(f"Demanda promedio: {prediccion['demanda_promedio_historica']} unidades/día")
        
        print("\nPredicciones para los próximos 7 días:")
        for pred in prediccion['predicciones'][:3]:  # Mostrar solo 3 días
            print(f"• {pred['fecha']}: {pred['demanda_predicha']} unidades")
    
    # Análisis de tendencias
    print("\n📊 Análisis de Tendencias:")
    tendencias = ai_service.analizar_tendencias()
    
    print("Productos con mayor rotación:")
    for i, producto in enumerate(tendencias['productos_alta_rotacion'][:3], 1):
        print(f"{i}. {producto['producto__nombre']} - {producto['total_vendido']} unidades")

def ejemplo_sugerencias_reabastecimiento():
    """Ejemplo de sugerencias de reabastecimiento"""
    print("\n" + "=" * 60)
    print("💡 EJEMPLO: Sugerencias de Reabastecimiento")
    print("=" * 60)
    
    ai_service = AIService()
    sugerencias = ai_service.generar_sugerencias_reabastecimiento()
    
    if sugerencias['sugerencias']:
        print(f"Total de productos que necesitan reabastecimiento: {len(sugerencias['sugerencias'])}")
        
        for i, sugerencia in enumerate(sugerencias['sugerencias'][:3], 1):
            print(f"\n{i}. {sugerencia['producto']}")
            print(f"   Stock actual: {sugerencia['stock_actual']}")
            print(f"   Stock mínimo: {sugerencia['stock_minimo']}")
            print(f"   Demanda diaria: {sugerencia['demanda_diaria_promedio']} unidades")
            print(f"   Días restantes: {sugerencia['dias_restantes_estimados']}")
            print(f"   Cantidad sugerida: {sugerencia['cantidad_sugerida']}")
            print(f"   Urgencia: {sugerencia['urgencia']}")
    else:
        print("✅ No hay productos que necesiten reabastecimiento inmediato")

def ejemplo_api_rest():
    """Ejemplo de uso de la API REST"""
    print("\n" + "=" * 60)
    print("🌐 EJEMPLO: Uso de la API REST")
    print("=" * 60)
    
    base_url = "http://localhost:8000/api"
    
    try:
        # Obtener productos
        print("Obteniendo productos desde la API...")
        response = requests.get(f"{base_url}/productos/")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API funcionando correctamente")
            print(f"Total de productos en API: {data.get('count', 'N/A')}")
            
            # Mostrar algunos productos
            if 'results' in data and data['results']:
                print("\nPrimeros productos desde API:")
                for producto in data['results'][:3]:
                    print(f"• {producto['nombre']}: {producto['cantidad']} unidades")
        else:
            print(f"❌ Error en API: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ No se puede conectar con la API")
        print("💡 Asegúrate de que el servidor Django esté ejecutándose:")
        print("   python manage.py runserver")

def ejemplo_registro_venta():
    """Ejemplo de registro de una venta"""
    print("\n" + "=" * 60)
    print("💰 EJEMPLO: Registro de Venta")
    print("=" * 60)
    
    # Obtener un producto disponible
    producto = Producto.objects.filter(cantidad__gt=0).first()
    
    if producto:
        print(f"Producto seleccionado: {producto.nombre}")
        print(f"Stock actual: {producto.cantidad}")
        print(f"Precio: ${producto.precio_venta}")
        
        # Simular una venta
        cantidad_vendida = min(2, producto.cantidad)  # Vender máximo 2 unidades
        
        venta = Venta.objects.create(
            producto=producto,
            cantidad_vendida=cantidad_vendida,
            precio_unitario=producto.precio_venta,
            cliente="Cliente Ejemplo",
            notas="Venta de demostración"
        )
        
        # Actualizar stock
        producto.cantidad -= cantidad_vendida
        producto.save()
        
        print(f"\n✅ Venta registrada:")
        print(f"   Cantidad vendida: {cantidad_vendida}")
        print(f"   Total: ${venta.total_venta}")
        print(f"   Stock restante: {producto.cantidad}")
    else:
        print("❌ No hay productos disponibles para la venta")

def ejemplo_estadisticas():
    """Ejemplo de estadísticas del sistema"""
    print("\n" + "=" * 60)
    print("📊 EJEMPLO: Estadísticas del Sistema")
    print("=" * 60)
    
    # Estadísticas básicas
    total_productos = Producto.objects.count()
    productos_activos = Producto.objects.filter(activo=True).count()
    productos_bajo_stock = Producto.objects.filter(cantidad__lte=F('cantidad_minima')).count()
    
    # Ventas del último mes
    fecha_limite = datetime.now() - timedelta(days=30)
    ventas_mes = Venta.objects.filter(fecha_venta__gte=fecha_limite)
    total_ventas = ventas_mes.count()
    ingresos_mes = sum(venta.total_venta for venta in ventas_mes)
    
    print(f"📦 Total de productos: {total_productos}")
    print(f"✅ Productos activos: {productos_activos}")
    print(f"⚠️  Productos bajo stock: {productos_bajo_stock}")
    print(f"💰 Ventas del mes: {total_ventas}")
    print(f"💵 Ingresos del mes: ${ingresos_mes:,.2f}")
    
    # Top productos más vendidos
    top_productos = ventas_mes.values('producto__nombre').annotate(
        total_vendido=Sum('cantidad_vendida')
    ).order_by('-total_vendido')[:5]
    
    print(f"\n🏆 Top 5 productos más vendidos:")
    for i, prod in enumerate(top_productos, 1):
        print(f"{i}. {prod['producto__nombre']} - {prod['total_vendido']} unidades")

def main():
    """Función principal con ejemplos"""
    print("🤖 SISTEMA DE INVENTARIO INTELIGENTE")
    print("Ejemplos de uso y funcionalidades")
    print("=" * 60)
    
    try:
        # Ejecutar ejemplos
        ejemplo_consulta_basica()
        ejemplo_analisis_ia()
        ejemplo_sugerencias_reabastecimiento()
        ejemplo_estadisticas()
        ejemplo_registro_venta()
        ejemplo_api_rest()
        
        print("\n" + "=" * 60)
        print("✅ ¡Ejemplos completados exitosamente!")
        print("=" * 60)
        print("\n💡 Próximos pasos:")
        print("1. Ejecutar servidor Django: python manage.py runserver")
        print("2. Abrir dashboard: python dashboard_app.py")
        print("3. Usar CLI: python consultar_inventario.py --interactive")
        print("4. Acceder a admin: http://localhost:8000/admin/")
        print("5. Ver API: http://localhost:8000/api/")
        
    except Exception as e:
        print(f"\n❌ Error ejecutando ejemplos: {e}")
        print("💡 Asegúrate de que:")
        print("   • Las migraciones estén aplicadas: python manage.py migrate")
        print("   • Los datos de ejemplo estén creados: python seed_data.py")

if __name__ == "__main__":
    main()
