#!/usr/bin/env python3
import os
import sys
import django
import requests
import json
import pandas as pd
from datetime import datetime, timedelta
import argparse
from tabulate import tabulate

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from productos.models import Product, Sale, Supplier, Category, InventoryAlert
from productos.ml_services import DemandPredictionService, ReorderSuggestionService, TrendAnalysisService

class SimpleInventoryCLI:
    """CLI simple para gestión de inventario"""
    
    def __init__(self):
        self.prediction_service = DemandPredictionService()
        self.reorder_service = ReorderSuggestionService(self.prediction_service)
        self.trend_service = TrendAnalysisService()
    
    def mostrar_metricas(self):
        """Mostrar métricas principales del inventario"""
        try:
            from django.db.models import Sum, F
            
            total_products = Product.objects.count()
            total_sales = Sale.objects.count()
            total_revenue = Sale.objects.aggregate(total=Sum('total_amount'))['total'] or 0
            low_stock_count = Product.objects.filter(quantity__lte=F('min_stock_level')).count()
            need_reorder_count = Product.objects.filter(reorder_suggestion=True).count()
            
            print("\n=== METRICAS DEL INVENTARIO ===")
            print("=" * 50)
            print(f"Total de Productos: {total_products:,}")
            print(f"Ingresos Totales: ${total_revenue:,.2f}")
            print(f"Productos con Stock Bajo: {low_stock_count:,}")
            print(f"Productos que Necesitan Reabastecimiento: {need_reorder_count:,}")
            print(f"Ventas Totales: {total_sales:,}")
            print(f"Ultima Actualizacion: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
        except Exception as e:
            print(f"Error obteniendo metricas: {e}")
    
    def mostrar_productos_stock_bajo(self):
        """Mostrar productos con stock bajo"""
        try:
            from django.db.models import F
            
            productos = Product.objects.filter(quantity__lte=F('min_stock_level'))
            
            if not productos.exists():
                print("No hay productos con stock bajo")
                return
            
            print("\n=== PRODUCTOS CON STOCK BAJO ===")
            print("=" * 80)
            
            headers = ["ID", "Producto", "SKU", "Stock Actual", "Stock Minimo", "Estado"]
            rows = []
            
            for producto in productos:
                rows.append([
                    producto.id,
                    producto.name[:20] + "..." if len(producto.name) > 20 else producto.name,
                    producto.sku,
                    producto.quantity,
                    producto.min_stock_level,
                    producto.stock_status
                ])
            
            print(tabulate(rows, headers=headers, tablefmt="grid"))
            
        except Exception as e:
            print(f"Error obteniendo productos con stock bajo: {e}")
    
    def mostrar_sugerencias_reabastecimiento(self):
        """Mostrar sugerencias de reabastecimiento"""
        try:
            products = Product.objects.all()
            suggestions = []
            
            for product in products:
                suggestion = self.reorder_service.calculate_reorder_suggestion(product.id)
                if suggestion and suggestion['needs_reorder']:
                    suggestions.append(suggestion)
            
            if not suggestions:
                print("No hay sugerencias de reabastecimiento en este momento")
                return
            
            # Ordenar por prioridad (días de suministro)
            suggestions.sort(key=lambda x: x['days_of_supply'])
            
            print(f"\n=== SUGERENCIAS DE REABASTECIMIENTO ({len(suggestions)} productos) ===")
            print("=" * 100)
            
            headers = ["Producto", "Stock Actual", "Demanda 7d", "Demanda 30d", "Dias Suministro", "Cantidad Sugerida", "Razon"]
            rows = []
            
            for suggestion in suggestions:
                rows.append([
                    suggestion['product_name'][:25] + "..." if len(suggestion['product_name']) > 25 else suggestion['product_name'],
                    suggestion['current_stock'],
                    f"{suggestion['predicted_demand_7d']:.1f}",
                    f"{suggestion['predicted_demand_30d']:.1f}",
                    f"{suggestion['days_of_supply']:.1f}",
                    suggestion['suggested_quantity'],
                    suggestion['reason'][:30] + "..." if len(suggestion['reason']) > 30 else suggestion['reason']
                ])
            
            print(tabulate(rows, headers=headers, tablefmt="grid"))
            
        except Exception as e:
            print(f"Error obteniendo sugerencias de reabastecimiento: {e}")
    
    def mostrar_predicciones_demanda(self):
        """Mostrar predicciones de demanda"""
        try:
            products = Product.objects.all()
            predictions = []
            
            for product in products:
                prediction_data = self.reorder_service.calculate_reorder_suggestion(product.id)
                if prediction_data:
                    predictions.append(prediction_data)
            
            if not predictions:
                print("No hay predicciones disponibles. Entrene los modelos primero.")
                return
            
            print(f"\n=== PREDICCIONES DE DEMANDA ({len(predictions)} productos) ===")
            print("=" * 90)
            
            headers = ["Producto", "Stock Actual", "Demanda Predicha 7d", "Demanda Predicha 30d", "Confianza", "Necesita Reorden"]
            rows = []
            
            for pred in predictions[:10]:  # Mostrar solo los primeros 10
                rows.append([
                    pred['product_name'][:20] + "..." if len(pred['product_name']) > 20 else pred['product_name'],
                    pred['current_stock'],
                    f"{pred['predicted_demand_7d']:.1f}",
                    f"{pred['predicted_demand_30d']:.1f}",
                    pred['confidence'],
                    "SI" if pred['needs_reorder'] else "NO"
                ])
            
            print(tabulate(rows, headers=headers, tablefmt="grid"))
            
            if len(predictions) > 10:
                print(f"\n... y {len(predictions) - 10} productos mas")
            
        except Exception as e:
            print(f"Error obteniendo predicciones de demanda: {e}")
    
    def entrenar_modelos(self):
        """Entrenar modelos de Machine Learning"""
        print("\nEntrenando modelos de Machine Learning...")
        
        try:
            results = []
            products = Product.objects.all()
            
            for product in products:
                result = self.prediction_service.train_model(product.id)
                results.append({
                    'product_id': product.id,
                    'product_name': product.name,
                    'success': result.get('success', False) if result else False,
                    'metrics': result if result and result.get('success') else None
                })
            
            successful = len([r for r in results if r['success']])
            print(f"Entrenamiento completado: {successful}/{len(products)} modelos entrenados exitosamente")
            
            # Mostrar resultados detallados
            if successful > 0:
                print("\nProductos con modelos entrenados:")
                for result in [r for r in results if r['success']][:5]:
                    print(f"   - {result['product_name']}")
                
                if successful > 5:
                    print(f"   ... y {successful - 5} productos mas")
            
        except Exception as e:
            print(f"Error entrenando modelos: {e}")
    
    def mostrar_alertas(self):
        """Mostrar alertas activas"""
        try:
            alerts = InventoryAlert.objects.filter(is_resolved=False)
            
            if not alerts.exists():
                print("No hay alertas activas")
                return
            
            print(f"\n=== ALERTAS ACTIVAS ({alerts.count()} alertas) ===")
            print("=" * 80)
            
            headers = ["ID", "Producto", "Tipo", "Mensaje", "Fecha"]
            rows = []
            
            for alert in alerts:
                rows.append([
                    alert.id,
                    alert.product.name[:20] + "..." if len(alert.product.name) > 20 else alert.product.name,
                    alert.get_alert_type_display(),
                    alert.message[:30] + "..." if len(alert.message) > 30 else alert.message,
                    alert.created_at.strftime("%d/%m/%Y")
                ])
            
            print(tabulate(rows, headers=headers, tablefmt="grid"))
            
        except Exception as e:
            print(f"Error obteniendo alertas: {e}")
    
    def mostrar_menu(self):
        """Mostrar menú de opciones"""
        print("\n" + "="*60)
        print("SISTEMA DE INVENTARIO INTELIGENTE")
        print("="*60)
        print("1. Ver metricas principales")
        print("2. Productos con stock bajo")
        print("3. Sugerencias de reabastecimiento")
        print("4. Predicciones de demanda")
        print("5. Ver alertas activas")
        print("6. Entrenar modelos de ML")
        print("0. Salir")
        print("="*60)
    
    def ejecutar(self):
        """Ejecutar el CLI principal"""
        print("Sistema de Inventario Inteligente iniciado")
        print("Escriba 'salir' o 'exit' para terminar")
        
        while True:
            try:
                self.mostrar_menu()
                opcion = input("\nSeleccione una opcion (0-6): ").strip()
                
                if opcion == "0" or opcion.lower() in ["salir", "exit", "quit"]:
                    print("\nHasta luego!")
                    break
                
                elif opcion == "1":
                    self.mostrar_metricas()
                
                elif opcion == "2":
                    self.mostrar_productos_stock_bajo()
                
                elif opcion == "3":
                    self.mostrar_sugerencias_reabastecimiento()
                
                elif opcion == "4":
                    self.mostrar_predicciones_demanda()
                
                elif opcion == "5":
                    self.mostrar_alertas()
                
                elif opcion == "6":
                    self.entrenar_modelos()
                
                else:
                    print("Opcion no valida. Intente de nuevo.")
                
                input("\nPresione Enter para continuar...")
                
            except KeyboardInterrupt:
                print("\n\nHasta luego!")
                break
            except Exception as e:
                print(f"\nError: {e}")
                input("Presione Enter para continuar...")

def main():
    """Función principal"""
    parser = argparse.ArgumentParser(description="Sistema de Inventario Inteligente")
    parser.add_argument("--metricas", "-m", action="store_true", help="Mostrar métricas principales")
    parser.add_argument("--stock-bajo", "-s", action="store_true", help="Mostrar productos con stock bajo")
    parser.add_argument("--predicciones", "-p", action="store_true", help="Mostrar predicciones de demanda")
    parser.add_argument("--entrenar", "-e", action="store_true", help="Entrenar modelos de ML")
    
    args = parser.parse_args()
    
    cli = SimpleInventoryCLI()
    
    if args.metricas:
        cli.mostrar_metricas()
    elif args.stock_bajo:
        cli.mostrar_productos_stock_bajo()
    elif args.predicciones:
        cli.mostrar_predicciones_demanda()
    elif args.entrenar:
        cli.entrenar_modelos()
    else:
        cli.ejecutar()

if __name__ == "__main__":
    main()



