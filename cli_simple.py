import os
import django
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "inventario_project.settings")
django.setup()
from productos.models import Producto, Venta, Proveedor
from productos.ai_services import AIService
from django.db.models import F, Sum

class InventarioCLISimple:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            print("ADVERTENCIA: No se encontro GEMINI_API_KEY. Algunas funciones de IA no estaran disponibles.")
            self.model = None
        else:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel("gemini-2.5-flash")
        
        self.ai_service = AIService()

    def consultar_inventario(self):
        """Consulta basica del inventario"""
        disponibles = Producto.objects.filter(cantidad__gt=0).order_by("nombre")
        
        print("\n=== INVENTARIO DISPONIBLE ===")
        if disponibles.exists():
            for producto in disponibles:
                print(f"• {producto.nombre}: {producto.cantidad} unidades (${producto.precio_venta})")
        else:
            print("No hay productos disponibles en el inventario.")
        
        print(f"\nTotal de productos disponibles: {disponibles.count()}")

    def analizar_tendencias(self):
        """Analisis de tendencias de ventas"""
        print("\n=== ANALISIS DE TENDENCIAS ===")
        
        try:
            tendencias = self.ai_service.analizar_tendencias()
            
            print("\nProductos con mayor rotacion (ultimos 30 dias):")
            for i, producto in enumerate(tendencias['productos_alta_rotacion'][:5], 1):
                print(f"{i}. {producto['producto__nombre']} - {producto['total_vendido']} unidades")
            
            print("\nProductos con menor rotacion:")
            for i, producto in enumerate(tendencias['productos_baja_rotacion'][:5], 1):
                print(f"{i}. {producto['producto__nombre']} - {producto['total_vendido']} unidades")
            
        except Exception as e:
            print(f"Error en analisis de tendencias: {e}")

    def sugerencias_reabastecimiento(self):
        """Sugerencias de reabastecimiento"""
        print("\n=== SUGERENCIAS DE REABASTECIMIENTO ===")
        
        try:
            sugerencias = self.ai_service.generar_sugerencias_reabastecimiento()
            
            if not sugerencias['sugerencias']:
                print("No hay productos que necesiten reabastecimiento inmediato")
                return
            
            for i, sugerencia in enumerate(sugerencias['sugerencias'], 1):
                print(f"\n{i}. {sugerencia['producto']}")
                print(f"   Stock actual: {sugerencia['stock_actual']}")
                print(f"   Stock minimo: {sugerencia['stock_minimo']}")
                print(f"   Demanda diaria: {sugerencia['demanda_diaria_promedio']} unidades")
                print(f"   Dias restantes: {sugerencia['dias_restantes_estimados']}")
                print(f"   Cantidad sugerida: {sugerencia['cantidad_sugerida']}")
                print(f"   Urgencia: {sugerencia['urgencia']}")
                
        except Exception as e:
            print(f"Error generando sugerencias: {e}")

    def dashboard_resumen(self):
        """Resumen ejecutivo del inventario"""
        print("\n=== DASHBOARD EJECUTIVO ===")
        
        # Estadisticas basicas
        total_productos = Producto.objects.count()
        productos_activos = Producto.objects.filter(activo=True).count()
        productos_bajo_stock = Producto.objects.filter(cantidad__lte=F('cantidad_minima')).count()
        
        # Ventas del ultimo mes
        from datetime import datetime, timedelta
        fecha_limite = datetime.now() - timedelta(days=30)
        ventas_mes = Venta.objects.filter(fecha_venta__gte=fecha_limite)
        total_ventas = ventas_mes.count()
        ingresos_mes = sum(venta.total_venta for venta in ventas_mes)
        
        print(f"Total de productos: {total_productos}")
        print(f"Productos activos: {productos_activos}")
        print(f"Productos bajo stock: {productos_bajo_stock}")
        print(f"Ventas del mes: {total_ventas}")
        print(f"Ingresos del mes: ${ingresos_mes:,.2f}")
        
        # Top productos mas vendidos
        top_productos = ventas_mes.values('producto__nombre').annotate(
            total_vendido=Sum('cantidad_vendida')
        ).order_by('-total_vendido')[:5]
        
        print(f"\nTop 5 productos mas vendidos:")
        for i, prod in enumerate(top_productos, 1):
            print(f"{i}. {prod['producto__nombre']} - {prod['total_vendido']} unidades")

    def menu_interactivo(self):
        """Menu interactivo para el CLI"""
        while True:
            print("\n" + "="*60)
            print("INVENTARIO INTELIGENTE - CLI")
            print("="*60)
            print("1. Consultar inventario basico")
            print("2. Analisis de tendencias")
            print("3. Sugerencias de reabastecimiento")
            print("4. Dashboard ejecutivo")
            print("5. Salir")
            print("="*60)
            
            opcion = input("\nSelecciona una opcion (1-5): ").strip()
            
            if opcion == "1":
                self.consultar_inventario()
            elif opcion == "2":
                self.analizar_tendencias()
            elif opcion == "3":
                self.sugerencias_reabastecimiento()
            elif opcion == "4":
                self.dashboard_resumen()
            elif opcion == "5":
                print("Hasta luego!")
                break
            else:
                print("Opcion invalida")
            
            input("\nPresiona Enter para continuar...")

def main():
    """Funcion principal"""
    print("INVENTARIO INTELIGENTE - CLI SIMPLE")
    print("="*50)
    
    cli = InventarioCLISimple()
    cli.menu_interactivo()

if __name__ == "__main__":
    main()
