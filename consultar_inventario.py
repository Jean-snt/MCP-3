import os
import django
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "inventario_project.settings")
django.setup()
from productos.models import Producto

def consultar_inventario() -> None:

    disponibles = Producto.objects.filter(cantidad__gt=0).order_by("nombre")
    lista = "\n".join([f"{p.nombre} ({p.cantidad} unidades)" for p in disponibles])

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("No encontré la variable GEMINI_API_KEY. Configúrala primero en tu .env.")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.5-flash")
  
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

    response = model.generate_content(prompt)
    print((response.text or "").strip())


if __name__ == "__main__":
    consultar_inventario()

