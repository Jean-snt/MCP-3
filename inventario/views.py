from django.shortcuts import render
from django.http import JsonResponse
from .models import Product
import vertexai
from vertexai.generative_models import GenerativeModel
import os
import json

# Create your views here.

def detectar_accion_simple(user_query):
    """Detección inteligente de acciones cuando Vertex AI falla"""
    query = user_query.lower().strip()
    
    # Detectar salir
    if any(word in query for word in ['salir', 'exit', 'quit', 'cerrar', 'terminar', 'adios', 'adiós', 'chao', 'bye', 'hasta luego', 'nos vemos', 'hasta la vista']):
        return {"action": "salir", "name": None, "quantity": None, "description": None, "id": None}
    
    # Detectar eliminar
    elif any(word in query for word in ['eliminar', 'borrar', 'quitar', 'delete', 'elimina', 'borra', 'quita', 'sacar', 'retirar']):
        return {"action": "eliminar", "name": None, "quantity": None, "description": None, "id": None}
    
    # Detectar añadir (más flexible)
    elif any(word in query for word in ['añadir', 'agregar', 'crear', 'nuevo', 'quiero', 'necesito', 'agregue', 'añada', 'inscribir', 'registrar', 'meter']):
        return {"action": "añadir", "name": None, "quantity": None, "description": None, "id": None}
    
    # Detectar actualizar
    elif any(word in query for word in ['actualizar', 'cambiar', 'modificar', 'editar', 'update', 'cambio', 'ajustar', 'revisar']):
        return {"action": "actualizar", "name": None, "quantity": None, "description": None, "id": None}
    
    # Detectar mostrar producto específico
    elif any(word in query for word in ['mostrar', 'muestra', 'ver', 'detalles', 'producto', 'dime sobre', 'información de', 'datos de', 'características']):
        return {"action": "mostrar_producto", "name": None, "quantity": None, "description": None, "id": None}
    
    
    # Detectar productos disponibles
    elif any(word in query for word in ['disponible', 'stock', 'hay', 'tengo', 'existe', 'disponibles', 'en stock', 'inventario']):
        return {"action": "listar_disponibles", "name": None, "quantity": None, "description": None, "id": None}
    
    # Preguntas generales - usar IA conversacional
    elif any(word in query for word in ['qué', 'que', 'como', 'cómo', 'por que', 'por qué', 'cuando', 'cuándo', 'donde', 'dónde', 'quien', 'quién', 'explica', 'ayuda', 'ayudame', 'ayúdame', 'información', 'help', 'hola', 'hi', 'buenos días', 'buenas tardes', 'buenas noches']):
        return {"action": "conversacional", "name": None, "quantity": None, "description": None, "id": None}
    
    # Por defecto, conversacional para ser más inteligente
    else:
        return {"action": "conversacional", "name": None, "quantity": None, "description": None, "id": None}

def ejecutar_accion(action_data, productos_data):
    """Ejecutar la acción solicitada"""
    action = action_data.get('action', 'listar')
    
    try:
        if action == 'salir':
            return {
                'mensaje': "👋 ¡Hasta luego! Que tengas un excelente día. Gracias por usar el sistema de inventario inteligente.",
                'datos': {'accion': 'salir'}
            }
        elif action == 'listar':
            return listar_todos_productos(productos_data)
        elif action == 'listar_disponibles':
            return listar_productos_disponibles(productos_data)
        elif action == 'mostrar_producto':
            return mostrar_producto_especifico(action_data, productos_data)
        elif action == 'eliminar':
            return eliminar_producto(action_data, productos_data)
        elif action == 'actualizar':
            return actualizar_producto(action_data)
        elif action == 'añadir':
            return añadir_producto(action_data)
        elif action == 'conversacional':
            return respuesta_conversacional(action_data, productos_data)
        else:
            return {
                'mensaje': f"Acción '{action}' no reconocida. Puedes usar: listar, eliminar, actualizar, añadir, mostrar producto, o simplemente preguntarme lo que quieras.",
                'datos': {}
            }
    except Exception as e:
        return {
            'mensaje': f"Error al ejecutar la acción '{action}': {str(e)}",
            'datos': {}
        }

def listar_todos_productos(productos_data):
    """Listar todos los productos"""
    if not productos_data:
        return {
            'mensaje': "El inventario está vacío. No hay productos registrados.",
            'datos': {'productos': []}
        }
    
    mensaje = "📦 **INVENTARIO COMPLETO**\n\n"
    for producto in productos_data:
        status = "✅ Disponible" if producto['cantidad'] > 0 else "❌ Agotado"
        mensaje += f"• **{producto['nombre']}** (ID: {producto['id']})\n"
        mensaje += f"  Cantidad: {producto['cantidad']} unidades - {status}\n"
        if producto['descripcion']:
            mensaje += f"  Descripción: {producto['descripcion'][:60]}...\n"
        mensaje += "\n"
    
    return {
        'mensaje': mensaje,
        'datos': {'productos': productos_data, 'total': len(productos_data)}
    }

def listar_productos_disponibles(productos_data):
    """Listar solo productos disponibles"""
    disponibles = [p for p in productos_data if p['cantidad'] > 0]
    
    if not disponibles:
        return {
            'mensaje': "❌ No hay productos disponibles en stock. Todos están agotados.",
            'datos': {'productos': []}
        }
    
    mensaje = "✅ **PRODUCTOS DISPONIBLES**\n\n"
    for producto in disponibles:
        mensaje += f"• **{producto['nombre']}** - {producto['cantidad']} unidades\n"
        if producto['descripcion']:
            mensaje += f"  _{producto['descripcion'][:60]}..._\n"
        mensaje += "\n"
    
    mensaje += f"📊 **Total:** {len(disponibles)} productos disponibles"
    
    return {
        'mensaje': mensaje,
        'datos': {'productos': disponibles, 'total': len(disponibles)}
    }

def mostrar_producto_especifico(action_data, productos_data):
    """Mostrar detalles de un producto específico"""
    nombre_buscar = action_data.get('name', '').lower()
    
    if not nombre_buscar:
        return {
            'mensaje': "Por favor especifica qué producto quieres ver. Ejemplo: 'muestra el teclado'",
            'datos': {}
        }
    
    # Buscar producto por nombre (coincidencia parcial)
    producto_encontrado = None
    for producto in productos_data:
        if nombre_buscar in producto['nombre'].lower():
            producto_encontrado = producto
            break
    
    if not producto_encontrado:
        return {
            'mensaje': f"❌ No encontré ningún producto que contenga '{nombre_buscar}'. Usa 'listar' para ver todos los productos.",
            'datos': {}
        }
    
    mensaje = f"📋 **DETALLES DEL PRODUCTO**\n\n"
    mensaje += f"🆔 **ID:** {producto_encontrado['id']}\n"
    mensaje += f"📦 **Nombre:** {producto_encontrado['nombre']}\n"
    mensaje += f"🔢 **Cantidad:** {producto_encontrado['cantidad']} unidades\n"
    mensaje += f"📄 **Descripción:** {producto_encontrado['descripcion']}\n"
    
    if producto_encontrado['cantidad'] > 0:
        mensaje += f"✅ **Estado:** Disponible en stock"
    else:
        mensaje += f"❌ **Estado:** Agotado"
    
    return {
        'mensaje': mensaje,
        'datos': {'producto': producto_encontrado}
    }

def eliminar_producto(action_data, productos_data):
    """Eliminar un producto"""
    nombre_eliminar = action_data.get('name', '')
    if nombre_eliminar:
        nombre_eliminar = str(nombre_eliminar).strip()
    else:
        nombre_eliminar = ''
    
    if not nombre_eliminar:
        # Mostrar lista de productos para seleccionar
        return {
            'mensaje': "🗑️ **ELIMINAR PRODUCTO**\n\n¿Qué producto quieres eliminar? Selecciona uno de la lista:",
            'datos': {
                'tipo': 'formulario',
                'accion': 'eliminar',
                'campos': {
                    'producto': {
                        'label': 'Selecciona el producto a eliminar',
                        'valor': '',
                        'requerido': True,
                        'tipo': 'select',
                        'opciones': [
                            {'valor': p['id'], 'texto': f"{p['nombre']} (ID: {p['id']}) - {p['cantidad']} unidades"}
                            for p in productos_data
                        ]
                    }
                }
            }
        }
    
    # Buscar y eliminar producto
    try:
        from inventario.models import Product
        productos_eliminados = Product.objects.filter(name__icontains=nombre_eliminar).delete()
        
        if productos_eliminados[0] > 0:
            return {
                'mensaje': f"✅ **PRODUCTO ELIMINADO**\n\nSe eliminó '{nombre_eliminar}' del inventario.\nProductos eliminados: {productos_eliminados[0]}",
                'datos': {'eliminados': productos_eliminados[0]}
            }
        else:
            return {
                'mensaje': f"❌ No encontré ningún producto que contenga '{nombre_eliminar}'. Usa 'listar' para ver todos los productos.",
                'datos': {}
            }
    except Exception as e:
        return {
            'mensaje': f"❌ Error al eliminar el producto: {str(e)}",
            'datos': {}
        }

def actualizar_producto(action_data):
    """Actualizar un producto (solo cantidad por simplicidad)"""
    nombre_actualizar = action_data.get('name', '')
    if nombre_actualizar:
        nombre_actualizar = nombre_actualizar.strip()
    nueva_cantidad = action_data.get('quantity')
    
    if not nombre_actualizar or nueva_cantidad is None:
        return {
            'mensaje': "Para actualizar un producto necesito el nombre y la nueva cantidad. Ejemplo: 'actualiza el teclado a 20'",
            'datos': {}
        }
    
    try:
        from inventario.models import Product
        producto = Product.objects.filter(name__icontains=nombre_actualizar).first()
        
        if not producto:
            return {
                'mensaje': f"❌ No encontré el producto '{nombre_actualizar}'. Usa 'listar' para ver todos los productos.",
                'datos': {}
            }
        
        cantidad_anterior = producto.quantity
        producto.quantity = max(0, nueva_cantidad)
        producto.save()
        
        return {
            'mensaje': f"✅ **PRODUCTO ACTUALIZADO**\n\n**{producto.name}**\nCantidad anterior: {cantidad_anterior}\nCantidad nueva: {producto.quantity}",
            'datos': {'producto': {'id': producto.id, 'name': producto.name, 'quantity': producto.quantity}}
        }
    except Exception as e:
        return {
            'mensaje': f"❌ Error al actualizar el producto: {str(e)}",
            'datos': {}
        }

def añadir_producto(action_data):
    """Añadir un nuevo producto"""
    nombre_nuevo = action_data.get('name', '')
    if nombre_nuevo:
        nombre_nuevo = str(nombre_nuevo).strip()
    else:
        nombre_nuevo = ''
    
    cantidad = action_data.get('quantity', 0)
    if cantidad is None:
        cantidad = 0
    
    descripcion = action_data.get('description', '')
    if descripcion is None:
        descripcion = ''
    
    # Si no hay información suficiente, solicitar datos
    if not nombre_nuevo or not descripcion:
        return {
            'mensaje': "📝 **AGREGAR NUEVO PRODUCTO**\n\nPara añadir un producto necesito más información. Por favor completa los siguientes datos:",
            'datos': {
                'tipo': 'formulario',
                'accion': 'añadir',
                'campos': {
                    'nombre': {
                        'label': 'Nombre del producto',
                        'valor': nombre_nuevo if nombre_nuevo else '',
                        'requerido': True,
                        'placeholder': 'Ej: Teclado Mecánico RGB'
                    },
                    'cantidad': {
                        'label': 'Cantidad inicial',
                        'valor': cantidad if cantidad and cantidad > 0 else '',
                        'requerido': True,
                        'placeholder': 'Ej: 10',
                        'tipo': 'number'
                    },
                    'descripcion': {
                        'label': 'Descripción del producto',
                        'valor': descripcion if descripcion else '',
                        'requerido': True,
                        'placeholder': 'Ej: Teclado mecánico gaming con retroiluminación RGB'
                    }
                }
            }
        }
    
    try:
        from inventario.models import Product
        nuevo_producto = Product.objects.create(
            name=nombre_nuevo,
            quantity=max(0, cantidad),
            description=descripcion
        )
        
        return {
            'mensaje': f"✅ **PRODUCTO AÑADIDO**\n\n**{nuevo_producto.name}** (ID: {nuevo_producto.id})\nCantidad: {nuevo_producto.quantity} unidades\nDescripción: {nuevo_producto.description}",
            'datos': {'producto': {'id': nuevo_producto.id, 'name': nuevo_producto.name, 'quantity': nuevo_producto.quantity}}
        }
    except Exception as e:
        return {
            'mensaje': f"❌ Error al añadir el producto: {str(e)}",
            'datos': {}
        }

# Funciones de imágenes eliminadas para simplificar el sistema

def respuesta_conversacional(action_data, productos_data):
    """Respuesta conversacional súper inteligente usando Vertex AI"""
    try:
        # Configuración de Vertex AI
        PROJECT_ID = "stone-poetry-473315-a9"
        LOCATION = "us-central1"
        PRIMARY_MODEL = "gemini-1.5-flash"
        FALLBACK_MODEL = "gemini-2.5-flash"
        
        # Inicializar Vertex AI
        vertexai.init(project=PROJECT_ID, location=LOCATION)
        
        # Crear prompt conversacional súper avanzado
        total_productos = len(productos_data)
        productos_disponibles = len([p for p in productos_data if p['cantidad'] > 0])
        productos_agotados = total_productos - productos_disponibles
        
        user_query = action_data.get('user_query', '')
        
        prompt = f"""
        Eres un asistente virtual EXTREMADAMENTE inteligente y conversacional. 
        Eres como ChatGPT pero con acceso a información de inventario.
        
        PREGUNTA ESPECÍFICA DEL USUARIO: "{user_query}"
        
        INFORMACIÓN DEL INVENTARIO (solo para contexto):
        - Total de productos: {total_productos}
        - Productos disponibles: {productos_disponibles}
        - Productos agotados: {productos_agotados}
        - Lista: {json.dumps(productos_data, ensure_ascii=False, indent=2)}
        
        REGLAS IMPORTANTES:
        1. SIEMPRE responde PRIMERO la pregunta específica del usuario: "{user_query}"
        2. Si es una pregunta general (no de inventario), responde directamente como ChatGPT
        3. Solo menciona el inventario si es relevante o al final como información adicional
        4. No te enfoques solo en inventario si la pregunta es sobre otro tema
        
        PERSONALIDAD:
        - Muy amigable, natural y conversacional
        - Usas emojis apropiados
        - Respondes como una persona real, no como un robot
        - Puedes hacer chistes, ser empático, dar consejos
        - Hablas en español natural de Latinoamérica
        
        FORMATO DE RESPUESTA:
        - Máximo 200 palabras
        - Responde DIRECTAMENTE la pregunta del usuario
        - Si es relevante, menciona el inventario al final
        - Usa emojis para hacer más amigable
        
        EJEMPLOS CORRECTOS:
        - Pregunta: "¿Cuál es la capital de España?" → "¡Madrid! 🇪🇸 La capital de España es Madrid, una ciudad increíble con mucha historia y cultura. ¿Te gustaría saber algo más sobre Madrid o España?"
        - Pregunta: "¿Qué es la fotosíntesis?" → "¡Excelente pregunta! 🌱 La fotosíntesis es el proceso por el cual las plantas convierten la luz solar en energía... [explicación]. ¿Te interesa saber más sobre biología?"
        - Pregunta: "¿Cómo está mi inventario?" → "Tu inventario tiene {total_productos} productos ({productos_disponibles} disponibles, {productos_agotados} agotados). 📊 [análisis específico]"
        
        CONTEXTO: El usuario está en un sistema de inventario, pero puede preguntar CUALQUIER COSA.
        
        Responde DIRECTAMENTE la pregunta: "{user_query}". No te enfoques solo en inventario.
        """
        
        # Intentar con el modelo principal
        last_error = None
        for model_name in (PRIMARY_MODEL, FALLBACK_MODEL):
            try:
                model = GenerativeModel(model_name)
                response = model.generate_content(prompt)
                respuesta = response.text if hasattr(response, "text") else str(response)
                return {
                    'mensaje': f"🤖 **{respuesta}**",
                    'datos': {'tipo': 'conversacional'}
                }
            except Exception as e:
                last_error = e
                continue
        
        # Si falla, respuesta por defecto más inteligente
        raise last_error
        
    except Exception as e:
        # Respuesta de fallback más conversacional
        user_query = action_data.get('user_query', '').lower()
        
        # Respuestas directas para preguntas comunes
        if 'capital' in user_query and 'españa' in user_query:
            return {
                'mensaje': f"🤖 **¡Madrid! 🇪🇸**\n\nLa capital de España es Madrid, una ciudad increíble con mucha historia, cultura y vida nocturna. ¡Es una de mis ciudades favoritas! 😊\n\n¿Te gustaría saber algo más sobre Madrid o España?",
                'datos': {'tipo': 'conversacional'}
            }
        elif 'capital' in user_query and 'francia' in user_query:
            return {
                'mensaje': f"🤖 **¡París! 🇫🇷**\n\nLa capital de Francia es París, la Ciudad de la Luz. Con la Torre Eiffel, el Louvre y los Champs-Élysées, ¡es una ciudad mágica! ✨\n\n¿Te interesa saber más sobre París?",
                'datos': {'tipo': 'conversacional'}
            }
        elif 'qué es' in user_query and 'ia' in user_query:
            return {
                'mensaje': f"🤖 **¡Excelente pregunta!**\n\nLa Inteligencia Artificial (IA) es la capacidad de las máquinas para simular inteligencia humana, aprender y tomar decisiones. ¡Como yo! 😊\n\n¿Te gustaría saber más sobre cómo funciona la IA?",
                'datos': {'tipo': 'conversacional'}
            }
        elif 'hola' in user_query or 'hi' in user_query:
            return {
                'mensaje': f"🤖 **¡Hola! 😊**\n\n¡Qué gusto verte! Soy tu asistente inteligente y estoy aquí para ayudarte con cualquier cosa que necesites.\n\nPuedo responder preguntas sobre cualquier tema, ayudarte con tu inventario, o simplemente charlar. ¿En qué te puedo ayudar?",
                'datos': {'tipo': 'conversacional'}
            }
        else:
            # Respuesta genérica pero útil
            if total_productos == 0:
                return {
                    'mensaje': f"🤖 **¡Hola! 😊**\n\nSoy tu asistente inteligente. Veo que tu inventario está vacío, ¡perfecto momento para empezar! 🚀\n\nPuedo ayudarte con:\n• 📝 Agregar productos: 'añade 5 teclados'\n• 📊 Ver el inventario: 'muestra todo'\n• ❓ Responder cualquier pregunta que tengas\n\n¿Qué te gustaría hacer?",
                    'datos': {'tipo': 'conversacional'}
                }
            else:
                return {
                    'mensaje': f"🤖 **¡Hola! 😊**\n\nSoy tu asistente inteligente. Tu inventario tiene {total_productos} productos ({productos_disponibles} disponibles, {productos_agotados} agotados). 📊\n\nPuedo ayudarte con:\n• 📝 Gestión de productos (añadir, eliminar, actualizar)\n• 📊 Análisis del inventario\n• 💬 Responder cualquier pregunta que tengas\n• 🎯 Darte consejos y sugerencias\n\n¿En qué te puedo ayudar hoy?",
                    'datos': {'tipo': 'conversacional'}
                }

def inicio(request):
    """Vista principal del inventario"""
    productos = Product.objects.all()
    context = {
        'productos': productos,
        'total_productos': productos.count(),
        'productos_disponibles': productos.filter(quantity__gt=0).count(),
        'productos_agotados': productos.filter(quantity=0).count(),
    }
    return render(request, 'inventario/inicio.html', context)

def lista_productos(request):
    """Vista para mostrar todos los productos"""
    productos = Product.objects.all()
    context = {
        'productos': productos,
    }
    return render(request, 'inventario/lista_productos.html', context)

def consultar_inventario_ia(request):
    """Vista para consultar inventario usando Vertex AI con acciones automáticas"""
    if request.method == 'POST':
        try:
            # Obtener la consulta del usuario
            data = json.loads(request.body) if request.body else {}
            user_query = data.get('query', 'inventario')
            
            # Obtener todos los productos para el contexto
            todos_productos = Product.objects.all()
            productos_data = []
            for producto in todos_productos:
                productos_data.append({
                    'id': producto.id,
                    'nombre': producto.name,
                    'descripcion': producto.description,
                    'cantidad': producto.quantity
                })
            
            # Usar Vertex AI para interpretar la acción
            try:
                # Configuración de Vertex AI (misma que en consultar_inventario.py)
                PROJECT_ID = "stone-poetry-473315-a9"
                LOCATION = "us-central1"
                PRIMARY_MODEL = "gemini-1.5-flash"
                FALLBACK_MODEL = "gemini-2.5-flash"
                
                # Inicializar Vertex AI
                vertexai.init(project=PROJECT_ID, location=LOCATION)
                
                # Crear prompt para interpretar acciones súper inteligente
                prompt = f"""
                Eres un asistente súper inteligente que convierte instrucciones naturales en JSON.
                Analiza el contexto completo y responde SOLO con JSON válido.
                
                CAMPOS JSON:
                {{"action": one_of['listar','listar_disponibles','mostrar_producto','eliminar','actualizar','añadir','salir','conversacional'],
                 "name": string|null, "quantity": int|null, "description": string|null, "id": int|null}}
                
                INVENTARIO ACTUAL:
                {json.dumps(productos_data, ensure_ascii=False, indent=2)}
                
                REGLAS DE INTERPRETACIÓN:
                1. Si es una PREGUNTA (qué, cómo, por qué, cuándo, dónde, quién) → "conversacional"
                2. Si es un SALUDO (hola, hi, buenos días) → "conversacional"  
                3. Si menciona "disponible", "stock", "hay" → "listar_disponibles"
                4. Si menciona "todo", "completo", "listar" → "listar"
                5. Si menciona "eliminar", "borrar", "quitar" → "eliminar"
                6. Si menciona "añadir", "agregar", "crear", "nuevo" → "añadir"
                7. Si menciona "actualizar", "cambiar", "modificar" → "actualizar"
                8. Si menciona "mostrar", "ver", "detalles" → "mostrar_producto"
                9. Si menciona "salir", "cerrar", "terminar" → "salir"
                
                EJEMPLOS AVANZADOS:
                - "¿cómo estoy?" → {{"action":"conversacional", "name":null, "quantity":null, "description":null, "id":null}}
                - "hola, ¿qué tal?" → {{"action":"conversacional", "name":null, "quantity":null, "description":null, "id":null}}
                - "qué productos tengo disponibles" → {{"action":"listar_disponibles", "name":null, "quantity":null, "description":null, "id":null}}
                - "muestra todo mi inventario" → {{"action":"listar", "name":null, "quantity":null, "description":null, "id":null}}
                - "elimina el mouse inalámbrico" → {{"action":"eliminar", "name":"mouse inalámbrico", "quantity":null, "description":null, "id":null}}
                - "quiero añadir 5 teclados gaming" → {{"action":"añadir", "name":"teclados gaming", "quantity":5, "description":null, "id":null}}
                - "necesito crear un nuevo producto" → {{"action":"añadir", "name":null, "quantity":null, "description":null, "id":null}}
                - "actualiza el monitor a 15 unidades" → {{"action":"actualizar", "name":"monitor", "quantity":15, "description":null, "id":null}}
                - "muestra información del teclado" → {{"action":"mostrar_producto", "name":"teclado", "quantity":null, "description":null, "id":null}}
                - "quiero salir del sistema" → {{"action":"salir", "name":null, "quantity":null, "description":null, "id":null}}
                - "¿qué es la inteligencia artificial?" → {{"action":"conversacional", "name":null, "quantity":null, "description":null, "id":null}}
                
                CONSULTA DEL USUARIO: {user_query}
                
                JSON RESPUESTA:
                """
                
                # Intentar con el modelo principal
                last_error = None
                for model_name in (PRIMARY_MODEL, FALLBACK_MODEL):
                    try:
                        model = GenerativeModel(model_name)
                        response = model.generate_content(prompt)
                        text = response.text if hasattr(response, "text") else str(response)
                        
                        # Extraer JSON
                        start = text.find("{")
                        end = text.rfind("}")
                        if start != -1 and end != -1 and end > start:
                            text = text[start : end + 1]
                        
                        action_data = json.loads(text)
                        break
                    except Exception as e:
                        last_error = e
                        continue
                else:
                    # Si ambos modelos fallan, usar detección simple
                    action_data = detectar_accion_simple(user_query)
                    
            except Exception as e:
                # Si falla Vertex AI, usar detección simple
                print(f"Error con Vertex AI: {e}")
                action_data = detectar_accion_simple(user_query)
            
            # Añadir la consulta original al action_data
            action_data['user_query'] = user_query
            
            # Ejecutar la acción
            resultado = ejecutar_accion(action_data, productos_data)
            
            return JsonResponse({
                'success': True,
                'respuesta': resultado['mensaje'],
                'accion': action_data.get('action', 'desconocida'),
                'datos': resultado.get('datos', {})
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': f'Error al procesar la consulta: {str(e)}'
            })
    
    return render(request, 'inventario/consultar_ia.html')

def procesar_formulario(request):
    """Vista para procesar formularios de productos"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body) if request.body else {}
            accion = data.get('accion')
            campos = data.get('campos', {})
            
            if accion == 'añadir':
                return procesar_añadir_producto(campos)
            elif accion == 'eliminar':
                return procesar_eliminar_producto(campos)
            else:
                return JsonResponse({
                    'success': False,
                    'error': f'Acción no reconocida: {accion}'
                })
                
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': f'Error al procesar formulario: {str(e)}'
            })
    
    return JsonResponse({
        'success': False,
        'error': 'Método no permitido'
    })

def procesar_añadir_producto(campos):
    """Procesar el formulario de añadir producto"""
    try:
        from inventario.models import Product
        
        nombre = campos.get('nombre', '')
        if nombre:
            nombre = nombre.strip()
        descripcion = campos.get('descripcion', '')
        if descripcion:
            descripcion = descripcion.strip()
        
        # Manejo más robusto de la cantidad
        try:
            cantidad_str = campos.get('cantidad', '0')
            if cantidad_str:
                cantidad_str = cantidad_str.strip()
            if cantidad_str == '':
                cantidad = 0
            else:
                cantidad = int(cantidad_str)
        except (ValueError, TypeError):
            cantidad = 0
        
        if not nombre or not descripcion:
            return JsonResponse({
                'success': False,
                'error': 'Nombre y descripción son obligatorios'
            })
        
        # Validar que la cantidad sea un número positivo
        if cantidad < 0:
            cantidad = 0
        
        nuevo_producto = Product.objects.create(
            name=nombre,
            quantity=cantidad,
            description=descripcion
        )
        
        return JsonResponse({
            'success': True,
            'respuesta': f"✅ **PRODUCTO AÑADIDO**\n\n**{nuevo_producto.name}** (ID: {nuevo_producto.id})\nCantidad: {nuevo_producto.quantity} unidades\nDescripción: {nuevo_producto.description}",
            'accion': 'añadir',
            'datos': {'producto': {'id': nuevo_producto.id, 'name': nuevo_producto.name, 'quantity': nuevo_producto.quantity}}
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Error al añadir producto: {str(e)}'
        })

def procesar_eliminar_producto(campos):
    """Procesar el formulario de eliminar producto"""
    try:
        from inventario.models import Product
        
        producto_id = int(campos.get('producto', 0))
        
        if not producto_id:
            return JsonResponse({
                'success': False,
                'error': 'Debes seleccionar un producto'
            })
        
        producto = Product.objects.filter(id=producto_id).first()
        if not producto:
            return JsonResponse({
                'success': False,
                'error': 'Producto no encontrado'
            })
        
        nombre_producto = producto.name
        producto.delete()
        
        return JsonResponse({
            'success': True,
            'respuesta': f"✅ **PRODUCTO ELIMINADO**\n\nSe eliminó '{nombre_producto}' del inventario.",
            'accion': 'eliminar',
            'datos': {'eliminado': nombre_producto}
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Error al eliminar producto: {str(e)}'
        })
