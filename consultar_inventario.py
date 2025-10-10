import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smart_inventory_project.settings')
django.setup()

from inventory.models import Product, Sale
from inventory.ai_logic import get_ai_suggestions

def main():
    print("🔍 SISTEMA DE INVENTARIO INTELIGENTE")
    print("=====================================")
    
    while True:
        print("\n1. 📦 Ver productos")
        print("2. 📊 Ver ventas")
        print("3. 🤖 Consultar análisis IA")
        print("4. 🚪 Salir")
        
        opcion = input("\nSelecciona una opción: ").strip()
        
        if opcion == '1':
            productos = Product.objects.all()
            print(f"\n📦 PRODUCTOS ({productos.count()}):")
            for p in productos:
                estado = "🔴 BAJO STOCK" if p.needs_restock() else "🟢 OK"
                print(f"  • {p.name}: {p.quantity} unidades {estado}")
                
        elif opcion == '2':
            ventas = Sale.objects.all().order_by('-sale_date')[:10]
            print(f"\n💰 ÚLTIMAS VENTAS ({ventas.count()}):")
            for v in ventas:
                print(f"  • {v.product.name}: {v.quantity_sold} unidades - ${v.total_revenue():.2f}")
                
        elif opcion == '3':
            print("\n🤖 CONSULTANDO IA...")
            sugerencias = get_ai_suggestions()
            
            if 'error' in sugerencias:
                print(f"❌ {sugerencias['error']}")
            else:
                print("💡 SUGERENCIAS:")
                print(sugerencias['suggestions'])
                
        elif opcion == '4':
            print("👋 ¡Hasta luego!")
            break
        else:
            print("❌ Opción inválida")

if __name__ == '__main__':
    main()