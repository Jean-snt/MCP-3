import requests
import json

API_BASE = "http://127.0.0.1:8000/api"

def listar_productos():
    print("\n📦 LISTA DE PRODUCTOS:")
    resp = requests.get(f"{API_BASE}/products/")
    if resp.status_code == 200:
        for p in resp.json():
            print(f"- {p['nombre']} (SKU: {p['sku']}) | Stock: {p['stock_actual']}")
    else:
        print("❌ Error al obtener productos.")

def prediccion_demanda(sku, dias=30):
    print(f"\n🤖 Predicción de demanda para {sku}:")
    data = {"sku": sku, "days": dias}
    resp = requests.post(f"{API_BASE}/predictions/", json=data)
    if resp.status_code == 200:
        print(json.dumps(resp.json(), indent=4, ensure_ascii=False))
    else:
        print("❌ Error en la predicción:", resp.text)

def sugerencia_reabastecimiento(id_producto):
    print(f"\n📊 Sugerencia de reabastecimiento para producto ID {id_producto}:")
    resp = requests.get(f"{API_BASE}/products/{id_producto}/restock_suggestion/")
    if resp.status_code == 200:
        print(json.dumps(resp.json(), indent=4, ensure_ascii=False))
    else:
        print("❌ Error:", resp.text)

if __name__ == "__main__":
    print("=== SMART INVENTORY CLI ===")
    listar_productos()
    sku = input("\n👉 Ingresa el SKU para predecir demanda: ")
    prediccion_demanda(sku)
    pid = input("\n👉 Ingresa el ID del producto para sugerencia de reabastecimiento: ")
    sugerencia_reabastecimiento(pid)
