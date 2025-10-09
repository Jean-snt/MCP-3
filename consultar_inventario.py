import os
import django
import google.generativeai as genai
import requests
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "inventario_project.settings")
django.setup()
from productos.models import Producto, Venta, Proveedor
from productos.ai_services import AIService
from django.db.models import F

class InventarioCLI:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("No encontré la variable GEMINI_API_KEY. Configúrala primero en tu .env.")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel("gemini-2.5-flash")
        self.ai_service = AIService()
        self.base_url = "http://localhost:8000/api"

    def consultar_inventario(self):
        """Consulta básica del inventario"""
        disponibles = Producto.objects.filter(cantidad__gt=0).order_by("nombre")
        lista = "\n".join([f"{p.nombre} ({p.cantidad} unidades)" for p in disponibles])

        prompt = f"""
Eres un asistente de inventario. Recibirás una lista ya filtrada de productos DISPONIBLES
(cantidad > 0). Devuelve la respuesta en ESPAÑOL con este formato EXACTO y sin texto adicional:

Hola, los productos disponibles en el inventario son:\n
<PRODUCTO 1> (<CANTIDAD 1> unidades)
<PRODUCTO 2> (<CANTIDAD 2> unidades)
...

Usa EXCLUSIVAMENTE la siguiente lista como fuente. Si está vacía, responde:
"No hay productos disponibles en el inventario."

Lista proporcionada:
{lista}
"""

        response = self.model.generate_content(prompt)
        print((response.text or "").strip())

    def analizar_tendencias(self):
        """Análisis de tendencias de ventas"""
        print("\n🔍 ANÁLISIS DE TENDENCIAS")
        print("=" * 50)
        
        try:
            # Usar el servicio de IA para análisis
            tendencias = self.ai_service.analizar_tendencias()
            
            print(f"\n📊 Productos con mayor rotación (últimos 30 días):")
            for i, producto in enumerate(tendencias['productos_alta_rotacion'][:5], 1):
                print(f"{i}. {producto['producto__nombre']} - {producto['total_vendido']} unidades")
            
            print(f"\n📉 Productos con menor rotación:")
            for i, producto in enumerate(tendencias['productos_baja_rotacion'][:5], 1):
                print(f"{i}. {producto['producto__nombre']} - {producto['total_vendido']} unidades")
            
            print(f"\n📈 Ventas por categoría:")
            for categoria in tendencias['ventas_por_categoria'][:5]:
                print(f"• {categoria['producto__categoria']}: {categoria['total_vendido']} unidades")
            
        except Exception as e:
            print(f"Error en análisis de tendencias: {e}")

    def predecir_demanda(self, producto_id=None):
        """Predicción de demanda para productos"""
        print("\n🔮 PREDICCIÓN DE DEMANDA")
        print("=" * 50)
        
        if producto_id:
            try:
                producto = Producto.objects.get(id=producto_id)
                prediccion = self.ai_service.predecir_demanda(producto, 7)
                
                print(f"\nProducto: {prediccion['producto']}")
                print(f"Confianza: {prediccion['confianza']}%")
                print(f"Datos históricos: {prediccion['datos_historicos']} días")
                print(f"Demanda promedio: {prediccion['demanda_promedio_historica']} unidades/día")
                
                print(f"\n📅 Predicciones para los próximos 7 días:")
                for pred in prediccion['predicciones']:
                    print(f"• {pred['fecha']} ({pred['dia_semana']}): {pred['demanda_predicha']} unidades")
                    
            except Producto.DoesNotExist:
                print(f"Producto con ID {producto_id} no encontrado")
        else:
            # Mostrar predicciones para productos con más ventas
            productos_populares = Venta.objects.filter(
                fecha_venta__gte=datetime.now() - timedelta(days=30)
            ).values('producto').annotate(
                total_vendido=Sum('cantidad_vendida')
            ).order_by('-total_vendido')[:3]
            
            for prod_data in productos_populares:
                producto = Producto.objects.get(id=prod_data['producto'])
                prediccion = self.ai_service.predecir_demanda(producto, 3)
                print(f"\n• {producto.nombre}: {prediccion['demanda_promedio_historica']} unidades/día promedio")

    def sugerencias_reabastecimiento(self):
        """Sugerencias inteligentes de reabastecimiento"""
        print("\n💡 SUGERENCIAS DE REABASTECIMIENTO")
        print("=" * 50)
        
        try:
            sugerencias = self.ai_service.generar_sugerencias_reabastecimiento()
            
            if not sugerencias['sugerencias']:
                print("✅ No hay productos que necesiten reabastecimiento inmediato")
                return
            
            for i, sugerencia in enumerate(sugerencias['sugerencias'], 1):
                print(f"\n{i}. {sugerencia['producto']}")
                print(f"   Stock actual: {sugerencia['stock_actual']}")
                print(f"   Stock mínimo: {sugerencia['stock_minimo']}")
                print(f"   Demanda diaria: {sugerencia['demanda_diaria_promedio']} unidades")
                print(f"   Días restantes: {sugerencia['dias_restantes_estimados']}")
                print(f"   Cantidad sugerida: {sugerencia['cantidad_sugerida']}")
                print(f"   Urgencia: {sugerencia['urgencia']}")
                print(f"   Proveedor: {sugerencia['proveedor']}")
                
        except Exception as e:
            print(f"Error generando sugerencias: {e}")

    def dashboard_resumen(self):
        """Resumen ejecutivo del inventario"""
        print("\n📊 DASHBOARD EJECUTIVO")
        print("=" * 50)
        
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
        
        # Top 5 productos más vendidos
        top_productos = ventas_mes.values('producto__nombre').annotate(
            total_vendido=Sum('cantidad_vendida')
        ).order_by('-total_vendido')[:5]
        
        print(f"\n🏆 Top 5 productos más vendidos:")
        for i, prod in enumerate(top_productos, 1):
            print(f"{i}. {prod['producto__nombre']} - {prod['total_vendido']} unidades")

    def menu_interactivo(self):
        """Menú interactivo para el CLI"""
        while True:
            print("\n" + "="*60)
            print("🤖 INVENTARIO INTELIGENTE - CLI")
            print("="*60)
            print("1. Consultar inventario básico")
            print("2. Análisis de tendencias")
            print("3. Predicción de demanda")
            print("4. Sugerencias de reabastecimiento")
            print("5. Dashboard ejecutivo")
            print("6. Salir")
            print("="*60)
            
            opcion = input("\nSelecciona una opción (1-6): ").strip()
            
            if opcion == "1":
                self.consultar_inventario()
            elif opcion == "2":
                self.analizar_tendencias()
            elif opcion == "3":
                producto_id = input("Ingresa ID del producto (Enter para análisis general): ").strip()
                if producto_id:
                    try:
                        self.predecir_demanda(int(producto_id))
                    except ValueError:
                        print("ID inválido")
                else:
                    self.predecir_demanda()
            elif opcion == "4":
                self.sugerencias_reabastecimiento()
            elif opcion == "5":
                self.dashboard_resumen()
            elif opcion == "6":
                print("¡Hasta luego! 👋")
                break
            else:
                print("Opción inválida")
            
            input("\nPresiona Enter para continuar...")

def consultar_inventario() -> None:
    """Función original para compatibilidad"""
    cli = InventarioCLI()
    cli.consultar_inventario()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        cli = InventarioCLI()
        cli.menu_interactivo()
    else:
        consultar_inventario()

