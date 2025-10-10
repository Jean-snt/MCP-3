import vertexai
from vertexai.generative_models import GenerativeModel
import os

def inicializar_vertex_ai(project_id=None, location="us-central1"):
    """
    Inicializa Vertex AI con manejo de errores robusto
    
    Args:
        project_id (str): ID del proyecto de Google Cloud
        location (str): Región de Vertex AI
    
    Returns:
        bool: True si se inicializó correctamente
    """
    try:
        # Usar project_id proporcionado o variable de entorno
        project_id = project_id or os.getenv('GOOGLE_CLOUD_PROJECT')
        
        if not project_id:
            raise ValueError("Se requiere project_id de Google Cloud")
        
        vertexai.init(project=project_id, location=location)
        print(f"✅ Vertex AI inicializado - Proyecto: {project_id}, Región: {location}")
        return True
        
    except Exception as e:
        print(f"❌ Error inicializando Vertex AI: {e}")
        return False

def obtener_modelo(modelo_principal="gemini-2.5-flash", fallbacks=None):
    """
    Obtiene modelo con sistema de fallback automático
    
    Args:
        modelo_principal (str): Modelo preferido
        fallbacks (list): Lista de modelos alternativos
    
    Returns:
        tuple: (modelo, nombre_modelo) o (None, None) si todos fallan
    """
    if fallbacks is None:
        fallbacks = ["gemini-1.5-flash", "gemini-1.0-pro", "gemini-1.0-pro-001"]
    
    modelos_a_probar = [modelo_principal] + fallbacks
    
    for modelo_nombre in modelos_a_probar:
        try:
            print(f"🔧 Probando modelo: {modelo_nombre}")
            modelo = GenerativeModel(modelo_nombre)
            
            # Test de conectividad con prompt mínimo
            test_response = modelo.generate_content("Responde 'OK'")
            
            print(f"✅ Modelo {modelo_nombre} cargado correctamente")
            return modelo, modelo_nombre
            
        except Exception as e:
            print(f"❌ Modelo {modelo_nombre} no disponible: {str(e)[:100]}...")
            continue
    
    print("❌ Ningún modelo de Gemini disponible en este proyecto")
    return None, None