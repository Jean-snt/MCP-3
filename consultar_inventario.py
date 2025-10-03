import os
import django

# ------------------------------
# Configuración Django
# ------------------------------
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smart_inventory_project.settings')
django.setup()

from productos.models import Producto
from ventas.models import Venta
import vertexai
from vertexai.generative_models import GenerativeModel
import pandas as pd
from sklearn.linear_model import LinearRegression

# ------------------------------
# Configuración Vertex AI
# ------------------------------
PROJECT_ID = "stone-poetry-473315-a9"
LOCATION = "us-central1"

vertexai.init(project=PROJECT_ID, location=LOCATION)

# ------------------------------
# Funciones de backend
# ------------------------------
def consultar_inventario():
    return [f"{p.nombre} ({p.cantidad} unidades)" for p in Producto.objects.filter(cantidad__gt=0)]

def predecir_demanda(producto_id):
    ventas = Venta.objects.filter(producto_id=producto_id).order_by('fecha_venta')
    if ventas.count() < 2:
        return 0
    df = pd.DataFrame(list(ventas.values('fecha_venta', 'cantidad_vendida')))
    df['timestamp'] = pd.to_datetime(df['fecha_venta']).map(pd.Timestamp.timestamp)
    X = df[['timestamp']]
    y = df['cantidad_vendida']
    modelo = LinearRegression()
    modelo.fit(X, y)
    proximo_timestamp = X['timestamp'].max() + 86400
    prediccion = modelo.predict([[proximo_timestamp]])
    return max(0, int(prediccion[0]))

def sugerir_reabastecimiento(stock_minimo=5):
    sugerencias = []
    for p in Producto.objects.all():
        pred = predecir_demanda(p.id)

        # ✅ Nueva lógica: si stock < mínimo o la predicción es mayor que el stock
        if p.cantidad < stock_minimo or pred > p.cantidad:
            sugerencias.append(f"{p.nombre}: stock {p.cantidad}, demanda estimada {pred}")
    return sugerencias


# ------------------------------
# Función que llama a Gemini
# ------------------------------
def responder_con_ia(prompt_usuario):
    disponibles = consultar_inventario()
    reabastecimiento = sugerir_reabastecimiento()

    # Preparamos contexto claro y ordenado
    contexto = f"""
    🛒 Inventario actual:
    {chr(10).join(["- " + d for d in disponibles]) if disponibles else "No hay productos en stock."}

    📦 Productos que necesitan reabastecimiento:
    {chr(10).join(["- " + r for r in reabastecimiento]) if reabastecimiento else "Ninguno por el momento."}
    """

    prompt_final = f"""
    Actúa como un asistente de inventario inteligente. 
    Tu tarea es responder de manera clara y natural a las preguntas del usuario sobre el inventario.

    Contexto del inventario:
    {contexto}

    Usuario: {prompt_usuario}
    Asistente:
    """

    model = GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt_final)
    return response.text

# ------------------------------
# CLI
# ------------------------------
if __name__ == "__main__":
    print("🤖 Bienvenido al Asistente de Inventario con IA (Gemini)!")
    while True:
        user_input = input("\nPregunta a la IA (o 'salir'): ")
        if user_input.lower() == "salir":
            print("👋 Hasta luego, ¡éxitos con tu inventario!")
            break
        respuesta = responder_con_ia(user_input)
        print("\n" + respuesta + "\n")
