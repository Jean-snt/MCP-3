from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from uuid import uuid4
from django.http import JsonResponse
from .models import Product
import os
import json
from .ml_services import DemandPredictionService, ReorderSuggestionService, TrendAnalysisService

# Carga perezosa de Vertex AI (si está instalado y configurado)
def _maybe_load_vertex():
    try:
        import vertexai
        from vertexai.generative_models import GenerativeModel
        return vertexai, GenerativeModel
    except Exception:
        return None, None

# Create your views here.
def _generate_unique_sku():
    """Genera un SKU único estilo SKU-XXXXXXXX."""
    from inventario.models import Product
    for _ in range(5):
        candidate = f"SKU-{uuid4().hex[:8].upper()}"
        if not Product.objects.filter(sku=candidate).exists():
            return candidate
    # Fallback con más entropía
    return f"SKU-{uuid4().hex[:12].upper()}"


def detectar_accion_simple(user_query):
    """Detección inteligente de acciones cuando Vertex AI falla"""
    query = user_query.lower().strip()
    # Tokens por palabra para evitar falsos positivos por subcadenas (p.ej. "inventario" contiene "venta")
    tokens = set(
        [t for t in query.replace(',', ' ').replace('.', ' ').replace('\n', ' ').split() if t]
    )
    
    # Detectar salir
    if any(word in query for word in ['salir', 'exit', 'quit', 'cerrar', 'terminar', 'adios', 'adiós', 'chao', 'bye', 'hasta luego', 'nos vemos', 'hasta la vista']):
        return {"action": "salir", "name": None, "quantity": None, "description": None, "id": None}
    
    # Listar inventario (sinónimos empresariales)
    elif (
        'inventario' in tokens
        or any(word in query for word in [
            'muestra el inventario','mostrar inventario','ver inventario','lista productos','listar productos',
            'que productos','qué productos','ver mis productos','ver stock','reporte de inventario','consulta de inventario'
        ])
        or 'listar' in tokens
    ):
        return {"action": "listar", "name": None, "quantity": None, "description": None, "id": None}
    
    # Detectar eliminar
    elif any(word in query for word in ['eliminar', 'borrar', 'quitar', 'delete', 'elimina', 'borra', 'quita', 'sacar', 'retirar']):
        return {"action": "eliminar", "name": None, "quantity": None, "description": None, "id": None}
    
    # Detectar predicción de demanda (antes que añadir para evitar falsos positivos por "quiero")
    elif any(word in query for word in ['predecir', 'prediccion', 'predicción', 'predice', 'pronostico', 'pronóstico','forecast']):
        return {"action": "predecir", "name": None, "quantity": None, "description": None, "id": None}

    # Detectar tendencias/análisis (antes que añadir para evitar falso positivo por "quiero")
    elif any(word in query for word in ['tendencia', 'tendencias', 'analisis', 'análisis', 'patrones', 'analizar', 'reporte', 'resumen','kpi','indicadores']):
        return {"action": "tendencias", "name": None, "quantity": None, "description": None, "id": None}

    # Registrar venta (evitar match de subcadenas como "inventario")
    elif (
        'venta' in tokens
        or 'vender' in tokens
        or 'registrar' in tokens and 'venta' in tokens
        or 'facturar' in tokens
    ):
        return {"action": "registrar_venta", "name": None, "quantity": None, "description": None, "id": None}

    # Detectar añadir (más flexible)
    elif any(word in query for word in ['añadir', 'agregar', 'crear', 'nuevo', 'quiero', 'necesito', 'agregue', 'añada', 'inscribir', 'registrar', 'meter']):
        return {"action": "añadir", "name": None, "quantity": None, "description": None, "id": None}
    
    # Detectar actualizar
    elif any(word in query for word in ['actualizar', 'cambiar', 'modificar', 'editar', 'update', 'cambio', 'ajustar', 'revisar']):
        return {"action": "actualizar", "name": None, "quantity": None, "description": None, "id": None}
    
    # Detectar sugerencias de reabastecimiento
    elif any(word in query for word in ['reabaste', 'reabastecimiento', 'reorden', 'reordenar', 'sugerencia', 'sugerir']):
        return {"action": "sugerir_reabastecimiento", "name": None, "quantity": None, "description": None, "id": None}
    
    # Detectar tendencias/análisis
    elif any(word in query for word in ['tendencia', 'tendencias', 'analisis', 'análisis', 'patrones']):
        return {"action": "tendencias", "name": None, "quantity": None, "description": None, "id": None}
    
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
        elif action == 'predecir':
            return predecir_demanda(action_data)
        elif action == 'sugerir_reabastecimiento':
            return sugerir_reabastecimiento(action_data)
        elif action == 'tendencias':
            return analizar_tendencias(action_data)
        elif action == 'registrar_venta':
            return flujo_registrar_venta(action_data)
        elif action == 'conversacional':
            return respuesta_conversacional(action_data, productos_data)
        else:
            return {
                'mensaje': f"Acción '{action}' no reconocida. Puedes usar: listar, eliminar, actualizar, añadir, mostrar producto, predecir, sugerir reabastecimiento, tendencias o conversar.",
                'datos': {}
            }
    except Exception as e:
        return {
            'mensaje': f"Error al ejecutar la acción '{action}': {str(e)}",
            'datos': {}
        }

def listar_todos_productos(productos_data):
    """Listar todos los productos con formato empresarial (estado, precio, promo)."""
    if not productos_data:
        return {
            'mensaje': "El inventario está vacío. No hay productos registrados.",
            'datos': {'productos': []}
        }
    
    mensaje = "📦 **INVENTARIO COMPLETO**\n\n"
    for producto in productos_data:
        cantidad = producto.get('cantidad', 0)
        precio = producto.get('precio', 0)
        safety = producto.get('min_stock', 0) or 0
        estado = 'NORMAL'
        if cantidad <= 0:
            estado = 'CRITICO'
        elif cantidad <= (safety if safety else max(1, int(cantidad*0.2))):
            estado = 'BAJO'
        promo = ''
        # Si hubiéramos incluido promo en productos_data, la mostraríamos aquí
        mensaje += (
            f"• **{producto['nombre']}** (ID: {producto['id']})\n"
            f"  Stock: {cantidad} | Estado: {estado} | Precio: $ {precio:.2f} {promo}\n"
        )
        if producto.get('descripcion'):
            mensaje += f"  {producto['descripcion'][:80]}\n"
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
                            {'valor': p['id'], 'texto': f"{p['nombre']} (ID: {p['id']}) - {p['cantidad']} unidades - $ {p.get('precio', 0):.2f}"}
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
    """Actualizar un producto (cantidad, precio, costo, min/max stock)"""
    nombre_actualizar = action_data.get('name', '')
    if nombre_actualizar:
        nombre_actualizar = nombre_actualizar.strip()
    nueva_cantidad = action_data.get('quantity')
    nuevo_precio = action_data.get('selling_price')
    nuevo_costo = action_data.get('cost_price')
    nuevo_min = action_data.get('min_stock')
    nuevo_max = action_data.get('max_stock')
    
    if not nombre_actualizar:
        # Solicitar datos con formulario completo
        return {
            'mensaje': "🛠️ **ACTUALIZAR PRODUCTO**\n\nIndica los campos a actualizar:",
            'datos': {
                'tipo': 'formulario',
                'accion': 'actualizar',
                'campos': {
                    'producto': {
                        'label': 'Nombre del producto',
                        'valor': '',
                        'requerido': True,
                        'placeholder': 'Ej: Teclado Mecánico'
                    },
                    'cantidad': {
                        'label': 'Nueva cantidad',
                        'valor': '',
                        'requerido': False,
                        'tipo': 'number'
                    },
                    'precio': {
                        'label': 'Nuevo precio de venta',
                        'valor': '',
                        'requerido': False,
                        'tipo': 'number'
                    },
                    'costo': {
                        'label': 'Nuevo precio de costo',
                        'valor': '',
                        'requerido': False,
                        'tipo': 'number'
                    },
                    'min_stock': {
                        'label': 'Nuevo stock mínimo',
                        'valor': '',
                        'requerido': False,
                        'tipo': 'number'
                    },
                    'max_stock': {
                        'label': 'Nuevo stock máximo',
                        'valor': '',
                        'requerido': False,
                        'tipo': 'number'
                    }
                }
            }
        }
    
    try:
        from inventario.models import Product
        producto = Product.objects.filter(name__icontains=nombre_actualizar).first()
        
        if not producto:
            return {
                'mensaje': f"❌ No encontré el producto '{nombre_actualizar}'. Usa 'listar' para ver todos los productos.",
                'datos': {}
            }
        
        cambios = {}
        if nueva_cantidad is not None:
            producto.quantity = max(0, int(nueva_cantidad))
            cambios['cantidad'] = producto.quantity
        if nuevo_precio is not None:
            try:
                producto.selling_price = float(nuevo_precio)
                cambios['precio'] = float(producto.selling_price)
            except Exception:
                pass
        if nuevo_costo is not None:
            try:
                producto.cost_price = float(nuevo_costo)
                cambios['costo'] = float(producto.cost_price)
            except Exception:
                pass
        if nuevo_min is not None:
            try:
                producto.min_stock_level = int(nuevo_min)
                cambios['min_stock'] = producto.min_stock_level
            except Exception:
                pass
        if nuevo_max is not None:
            try:
                producto.max_stock_level = int(nuevo_max)
                cambios['max_stock'] = producto.max_stock_level
            except Exception:
                pass
        
        producto.save()
        
        return {
            'mensaje': f"✅ **PRODUCTO ACTUALIZADO**\n\n**{producto.name}**\nCambios: {cambios}",
            'datos': {'producto': {'id': producto.id, 'name': producto.name, **cambios}}
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
    
    # Aceptar tanto 'quantity' como 'stock' (compatibilidad)
    cantidad = action_data.get('stock', action_data.get('quantity', 0))
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
                    'stock': {
                        'label': 'Stock inicial',
                        'valor': cantidad if cantidad and cantidad > 0 else '',
                        'requerido': True,
                        'placeholder': 'Ej: 10',
                        'tipo': 'number'
                    },
                    'precio': {
                        'label': 'Precio de venta (USD)',
                        'valor': '',
                        'requerido': True,
                        'placeholder': 'Ej: 49.99',
                        'tipo': 'number'
                    },
                    'descripcion': {
                        'label': 'Descripción del producto',
                        'valor': descripcion if descripcion else '',
                        'requerido': True,
                        'placeholder': 'Ej: Teclado mecánico gaming con retroiluminación RGB'
                    },
                    'safety_stock': {
                        'label': 'Stock de seguridad',
                        'valor': 0,
                        'requerido': False,
                        'placeholder': 'Ej: 5',
                        'tipo': 'number'
                    },
                    'seasonality_index': {
                        'label': 'Índice de estacionalidad (0.1-3.0)',
                        'valor': 1.0,
                        'requerido': False,
                        'placeholder': 'Ej: 1.2',
                        'tipo': 'number'
                    },
                    'promotion_active': {
                        'label': 'Promoción activa',
                        'valor': False,
                        'requerido': False,
                        'tipo': 'select',
                        'opciones': [
                            {'valor': False, 'texto': 'No'},
                            {'valor': True, 'texto': 'Sí'}
                        ]
                    },
                    'current_discount': {
                        'label': 'Descuento actual (%)',
                        'valor': 0,
                        'requerido': False,
                        'placeholder': 'Ej: 10',
                        'tipo': 'number'
                    }
                }
            }
        }
    
    try:
        from inventario.models import Product
        nuevo_producto = Product.objects.create(
            name=nombre_nuevo,
            quantity=max(0, cantidad),
            description=descripcion,
            selling_price=action_data.get('precio') or 0,
            sku=_generate_unique_sku()
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
    """Respuesta conversacional: usa Vertex AI si está disponible; si no, fallback local."""
    raw_query = action_data.get('user_query') or ''
    user_query = raw_query.lower()
    total_productos = len(productos_data)
    productos_disponibles = len([p for p in productos_data if p['cantidad'] > 0])
    productos_agotados = total_productos - productos_disponibles

    # Intentar Vertex AI si hay configuración
    vertexai, GenerativeModel = _maybe_load_vertex()
    project_id = os.getenv('VERTEX_PROJECT_ID')
    location = os.getenv('VERTEX_LOCATION', 'us-central1')
    model_primary = os.getenv('VERTEX_MODEL', 'gemini-1.5-flash')
    model_fallback = os.getenv('VERTEX_MODEL_FALLBACK', 'gemini-2.5-flash')

    if vertexai and GenerativeModel and project_id:
        try:
            vertexai.init(project=project_id, location=location)
            prompt = (
                f"Responde en español de forma concisa y amable a: '{raw_query}'. "
                f"Contexto de inventario: total={total_productos}, disp={productos_disponibles}, agotados={productos_agotados}."
            )
            for model_name in (model_primary, model_fallback):
                try:
                    model = GenerativeModel(model_name)
                    response = model.generate_content(prompt)
                    text = response.text if hasattr(response, 'text') else str(response)
                    if text:
                        return {
                            'mensaje': f"🤖 **{text}**",
                            'datos': {'tipo': 'conversacional', 'provider': 'vertex'}
                        }
                except Exception:
                    continue
        except Exception:
            pass

    # Fallback local
    if 'capital' in user_query and 'españa' in user_query:
        return {
            'mensaje': "🤖 **¡Madrid! 🇪🇸**\n\nLa capital de España es Madrid.",
            'datos': {'tipo': 'conversacional', 'provider': 'local'}
        }
    if 'capital' in user_query and 'francia' in user_query:
        return {
            'mensaje': "🤖 **¡París! 🇫🇷**\n\nLa capital de Francia es París.",
            'datos': {'tipo': 'conversacional', 'provider': 'local'}
        }

    if total_productos == 0:
        texto = (
            "🤖 **¡Hola! 😊**\n\nTu inventario está vacío. "
            "Puedo ayudarte a añadir productos, listar inventario o analizar tendencias."
        )
    else:
        texto = (
            f"🤖 **¡Hola! 😊**\n\nInventario: {total_productos} productos "
            f"({productos_disponibles} disponibles, {productos_agotados} agotados). "
            "Puedo listar, analizar y predecir demanda."
        )

    return {
        'mensaje': texto,
        'datos': {'tipo': 'conversacional', 'provider': 'local'}
    }

# --- Acciones IA ---

def predecir_demanda(action_data):
    # Leer horizonte; si no hay, pedirlo al usuario
    def _to_int(value, default=None):
        try:
            if value is None:
                return default
            text = str(value).strip()
            if text == '':
                return default
            return int(float(text))
        except Exception:
            return default

    periodo = _to_int(action_data.get('periodo') or action_data.get('dias') or action_data.get('days'), None)
    if periodo is None:
        return {
            'mensaje': "🔮 Elige el horizonte de la predicción:",
            'datos': {
                'tipo': 'formulario',
                'accion': 'predecir',
                'campos': {
                    'periodo': {
                        'label': 'Horizonte (días)',
                        'tipo': 'select',
                        'requerido': True,
                        'opciones': [
                            {'valor': 3, 'texto': '3 días'},
                            {'valor': 7, 'texto': '7 días'},
                            {'valor': 30, 'texto': '30 días'},
                            {'valor': 60, 'texto': '60 días'}
                        ]
                    }
                }
            }
        }

    service = DemandPredictionService()
    productos = Product.objects.all()
    resultados = []
    for p in productos:
        pred_custom = service.predict_demand(p.id, periodo)
        resultados.append({
            'product_id': p.id,
            'product_name': p.name,
            'current_stock': p.quantity,
            'avg_period': pred_custom['average_daily'] if pred_custom else 0,
            'total_period': pred_custom['total_demand'] if pred_custom else 0,
            'seasonality_index': getattr(p, 'seasonality_index', 1.0) or 1.0,
            'promotion_active': getattr(p, 'promotion_active', False),
            'current_discount': float(getattr(p, 'current_discount', 0) or 0),
        })
    # Ordenar por mayor demanda en el período y tomar top 5
    resultados.sort(key=lambda x: x['total_period'], reverse=True)
    top = resultados[:5]
    # Construir mensaje legible
    mensaje = f"🔮 Predicciones para {periodo} días\n\n"
    if top:
        mensaje += "Principales productos por demanda:\n"
        for r in top:
            dias_supply = (r['current_stock'] / r['avg_period']) if r['avg_period'] else float('inf')
            dias_txt = (f"{dias_supply:.1f} días" if dias_supply != float('inf') else "∞ días")
            mensaje += (
                f"• {r['product_name']}: stock {r['current_stock']}, "
                f"demanda total {r['total_period']:.1f}, promedio diario {r['avg_period']:.1f}, "
                f"suministro {dias_txt}"
            )
            if r.get('promotion_active'):
                mensaje += " (promo activa)"
            mensaje += "\n"
    else:
        mensaje += "No hay productos registrados."
    return {
        'mensaje': mensaje,
        'datos': {'predictions': resultados}
    }

def sugerir_reabastecimiento(action_data):
    pred_service = DemandPredictionService()
    reorder_service = ReorderSuggestionService(pred_service)
    productos = Product.objects.all()
    sugerencias = []
    for p in productos:
        data = reorder_service.calculate_reorder_suggestion(p.id)
        if data:
            sugerencias.append(data)
    sugerencias.sort(key=lambda x: x['days_of_supply'])
    return {
        'mensaje': "🛒 Sugerencias de reabastecimiento generadas.",
        'datos': {'sugerencias': sugerencias}
    }

def analizar_tendencias(action_data):
    # Leer período; si no hay, pedirlo
    def _to_int(value, default=None):
        try:
            if value is None:
                return default
            text = str(value).strip()
            if text == '':
                return default
            return int(float(text))
        except Exception:
            return default

    periodo = _to_int(action_data.get('periodo') or action_data.get('dias') or action_data.get('days'), None)
    if periodo is None:
        return {
            'mensaje': "📈 Elige el período para el análisis:",
            'datos': {
                'tipo': 'formulario',
                'accion': 'tendencias',
                'campos': {
                    'periodo': {
                        'label': 'Período (días)',
                        'tipo': 'select',
                        'requerido': True,
                        'opciones': [
                            {'valor': 3, 'texto': '3 días'},
                            {'valor': 7, 'texto': '7 días'},
                            {'valor': 30, 'texto': '30 días'},
                            {'valor': 60, 'texto': '60 días'}
                        ]
                    }
                }
            }
        }

    service = TrendAnalysisService()
    trends = service.analyze_trends(periodo)
    # Construir resumen legible
    total_products = trends.get('total_products', 0)
    total_revenue = float(trends.get('total_revenue', 0))
    low_stock = trends.get('low_stock_products', [])
    need_reorder = trends.get('products_needing_reorder', 0)
    top = trends.get('top_selling_products', [])[:5]

    mensaje = f"📈 Análisis de tendencias (últimos {periodo} días)\n\n"
    mensaje += f"Productos: {total_products} | Ingresos: $ {total_revenue:,.2f} | Reorden: {need_reorder}\n\n"
    if top:
        mensaje += "Top ventas:\n"
        for item in top:
            nombre = item.get('product__name')
            vendidos = item.get('total_sold', 0)
            ingreso = float(item.get('total_revenue', 0) or 0)
            mensaje += f"• {nombre}: {vendidos} unidades, $ {ingreso:,.2f}\n"
        mensaje += "\n"
    if low_stock:
        mensaje += "Stock bajo:\n"
        for p in low_stock[:5]:
            nombre = p.get('name')
            qty = p.get('quantity', 0)
            minlvl = p.get('min_stock_level', 0)
            mensaje += f"• {nombre}: {qty}/{minlvl}\n"
    else:
        mensaje += "No hay productos con stock bajo."

    return {
        'mensaje': mensaje,
        'datos': {'trends': {
            'top_selling_products': top,
            'low_stock_products': low_stock,
            'total_revenue': total_revenue,
            'total_products': total_products,
            'products_needing_reorder': need_reorder
        }}
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
                    'cantidad': producto.quantity,
                    'precio': float(producto.selling_price or 0),
                    'costo': float(producto.cost_price or 0),
                    'min_stock': producto.min_stock_level,
                    'max_stock': producto.max_stock_level,
                    'estado_stock': producto.stock_status,
                    'pred_demanda_7d': producto.predicted_demand_7d,
                    'pred_demanda_30d': producto.predicted_demand_30d,
                    'sugerir_reorden': producto.reorder_suggestion,
                    'cantidad_reorden': producto.reorder_quantity,
                })
            
            # Interpretación local basada en reglas y palabras clave (sin servicios externos)
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

@csrf_exempt
def procesar_formulario(request):
    """Vista para procesar formularios de productos"""
    if request.method == 'POST':
        try:
            # Intentar leer como JSON; si falla, caer a form/urlencoded
            data = {}
            try:
                if request.body:
                    data = json.loads(request.body)
            except Exception:
                # Fallback: construir data desde request.POST (form submit)
                data = {
                    'accion': request.POST.get('accion'),
                    'campos': {}
                }
                # Copiar todos los parámetros simples como campos
                for key, value in request.POST.items():
                    if key in ['accion', 'csrfmiddlewaretoken']:
                        continue
                    data['campos'][key] = value

            accion = data.get('accion')
            campos = data.get('campos', {})

            # Normalización: si solo llega período/días, interpretar como predicción o análisis
            period_keys = {'periodo', 'dias', 'days'}
            if any(k in campos for k in period_keys) and accion in [None, 'añadir']:
                accion = data.get('accion_sugerida') or 'predecir'
            
            if accion == 'añadir':
                return procesar_añadir_producto(campos)
            elif accion == 'eliminar':
                return procesar_eliminar_producto(campos)
            elif accion == 'actualizar':
                return procesar_actualizar_producto(campos)
            elif accion == 'predecir':
                res = predecir_demanda(campos)
                return JsonResponse({'success': True, 'respuesta': res.get('mensaje', ''), 'accion': 'predecir', 'datos': res.get('datos', {})})
            elif accion == 'sugerir_reabastecimiento':
                res = sugerir_reabastecimiento(campos)
                return JsonResponse({'success': True, 'respuesta': res.get('mensaje', ''), 'accion': 'sugerir_reabastecimiento', 'datos': res.get('datos', {})})
            elif accion == 'tendencias':
                res = analizar_tendencias(campos)
                return JsonResponse({'success': True, 'respuesta': res.get('mensaje', ''), 'accion': 'tendencias', 'datos': res.get('datos', {})})
            elif accion == 'registrar_venta':
                res = procesar_registrar_venta(campos)
                return res
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
        
        # Manejo de stock (solo "stock")
        try:
            stock_str = campos.get('stock', '0')
            if stock_str:
                stock_str = str(stock_str).strip()
            if stock_str == '':
                cantidad = 0
            else:
                cantidad = int(float(stock_str))
        except (ValueError, TypeError):
            cantidad = 0
        
        # Campo precio y planificación opcional
        def to_decimal(value, default='0'):
            try:
                text = (value if value is not None else default)
                text = str(text).strip()
                if text == '':
                    return 0
                return float(text)
            except Exception:
                return 0
        
        precio = to_decimal(campos.get('precio'))
        # Nuevos opcionales
        # lead_time_days removido del formulario; usaremos valor por defecto del modelo si se requiere
        lead_time_days = None
        try:
            safety_stock = int(float((campos.get('safety_stock') or '0').strip()))
        except Exception:
            safety_stock = 0
        try:
            seasonality_index = float((campos.get('seasonality_index') or '1').strip())
        except Exception:
            seasonality_index = 1.0
        # Promoción
        promotion_active = str(campos.get('promotion_active', 'False')).lower() in ['true', '1', 'si', 'sí', 'yes']
        try:
            current_discount = float((campos.get('current_discount') or '0').strip())
        except Exception:
            current_discount = 0
        
        if not nombre or not descripcion:
            return JsonResponse({
                'success': False,
                'error': 'Nombre y descripción son obligatorios'
            })
        
        if cantidad < 0:
            cantidad = 0
        
        kwargs = dict(
            name=nombre,
            quantity=cantidad,
            description=descripcion,
            selling_price=precio,
            sku=_generate_unique_sku(),
            safety_stock=safety_stock,
            seasonality_index=seasonality_index,
            promotion_active=promotion_active,
            current_discount=current_discount
        )
        # No pasar lead_time_days si es None
        nuevo_producto = Product.objects.create(**{k: v for k, v in kwargs.items() if v is not None})
        
        return JsonResponse({
            'success': True,
            'respuesta': f"✅ **PRODUCTO AÑADIDO**\n\n**{nuevo_producto.name}** (ID: {nuevo_producto.id})\nCantidad: {nuevo_producto.quantity} unidades\nPrecio: ${nuevo_producto.selling_price}\nDescripción: {nuevo_producto.description}",
            'accion': 'añadir',
            'datos': {'producto': {'id': nuevo_producto.id, 'name': nuevo_producto.name, 'quantity': nuevo_producto.quantity, 'selling_price': float(nuevo_producto.selling_price)}}
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

def procesar_actualizar_producto(campos):
    """Procesar el formulario de actualizar producto"""
    try:
        from inventario.models import Product
        
        nombre_actualizar = campos.get('producto', '')
        if not nombre_actualizar:
            return JsonResponse({
                'success': False,
                'error': 'Debes seleccionar un producto para actualizar'
            })
        
        producto = Product.objects.filter(name__icontains=nombre_actualizar).first()
        if not producto:
            return JsonResponse({
                'success': False,
                'error': f"❌ No encontré el producto '{nombre_actualizar}'. Usa 'listar' para ver todos los productos."
            })
        
        # Aceptar 'stock' como alias de 'cantidad' para compatibilidad
        nueva_cantidad = campos.get('stock') if campos.get('stock') is not None else campos.get('cantidad')
        nuevo_precio = campos.get('precio')
        nuevo_costo = campos.get('costo')
        nuevo_min = campos.get('min_stock')
        nuevo_max = campos.get('max_stock')
        
        cambios = {}
        if nueva_cantidad is not None:
            try:
                producto.quantity = max(0, int(nueva_cantidad))
                cambios['cantidad'] = producto.quantity
            except Exception:
                pass
        if nuevo_precio is not None:
            try:
                producto.selling_price = float(nuevo_precio)
                cambios['precio'] = float(producto.selling_price)
            except Exception:
                pass
        if nuevo_costo is not None:
            try:
                producto.cost_price = float(nuevo_costo)
                cambios['costo'] = float(producto.cost_price)
            except Exception:
                pass
        if nuevo_min is not None:
            try:
                producto.min_stock_level = int(nuevo_min)
                cambios['min_stock'] = producto.min_stock_level
            except Exception:
                pass
        if nuevo_max is not None:
            try:
                producto.max_stock_level = int(nuevo_max)
                cambios['max_stock'] = producto.max_stock_level
            except Exception:
                pass
        
        producto.save()
        
        return JsonResponse({
            'success': True,
            'respuesta': f"✅ **PRODUCTO ACTUALIZADO**\n\n**{producto.name}**\nCambios: {cambios}",
            'accion': 'actualizar',
            'datos': {'producto': {'id': producto.id, 'name': producto.name, **cambios}}
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Error al actualizar producto: {str(e)}'
        })

def flujo_registrar_venta(action_data):
    """Muestra formulario para registrar una venta (producto del inventario)."""
    from inventario.models import Product
    opciones = [
        {'valor': p.id, 'texto': f"{p.name} (stock: {p.quantity})"}
        for p in Product.objects.all().order_by('name')
    ]
    return {
        'mensaje': "🧾 **REGISTRAR VENTA**\n\nCompleta los datos de la venta:",
        'datos': {
            'tipo': 'formulario',
            'accion': 'registrar_venta',
            'campos': {
                'producto': {
                    'label': 'Producto del inventario',
                    'valor': '',
                    'requerido': True,
                    'tipo': 'select',
                    'opciones': opciones
                },
                'cantidad': {
                    'label': 'Cantidad vendida',
                    'valor': action_data.get('quantity') or '',
                    'requerido': True,
                    'tipo': 'number',
                    'placeholder': 'Ej: 2'
                },
                'precio_unitario': {
                    'label': 'Precio unitario (USD)',
                    'valor': action_data.get('unit_price') or '',
                    'requerido': False,
                    'tipo': 'number',
                    'placeholder': 'Ej: 49.99'
                },
                'cliente': {
                    'label': 'Cliente (opcional)',
                    'valor': '',
                    'requerido': False,
                    'placeholder': 'Nombre del cliente'
                }
            }
        }
    }

def procesar_registrar_venta(campos):
    """Procesa el formulario de registrar venta"""
    try:
        from inventario.models import Product, Sale
        # Puede venir ID desde el select
        producto = None
        prod_raw = campos.get('producto')
        if prod_raw is not None and str(prod_raw).strip() != '':
            try:
                producto = Product.objects.filter(id=int(prod_raw)).first()
            except Exception:
                producto = None
        # Fallback por nombre si no llegó un ID válido
        if not producto:
            nombre = (str(prod_raw) if prod_raw is not None else '').strip()
            if not nombre:
                return JsonResponse({'success': False, 'error': 'Debes seleccionar un producto'})
            producto = Product.objects.filter(name__icontains=nombre).first()
        if not producto:
            return JsonResponse({'success': False, 'error': 'Producto no encontrado'})

        # Cantidad
        try:
            cantidad = int(float((campos.get('cantidad') or '1').strip()))
            if cantidad <= 0:
                cantidad = 1
        except Exception:
            cantidad = 1
        # Precio unitario: usar el del producto si no se envía
        try:
            precio_unit = float((campos.get('precio_unitario') or '0').strip())
        except Exception:
            precio_unit = 0
        if precio_unit <= 0:
            precio_unit = float(producto.selling_price or 0)

        # Verificar stock suficiente
        if producto.quantity is not None and cantidad > max(0, int(producto.quantity)):
            return JsonResponse({'success': False, 'error': f"Stock insuficiente. Disponible: {producto.quantity}"})

        # Crear venta
        venta = Sale.objects.create(
            product=producto,
            quantity_sold=cantidad,
            unit_price=precio_unit,
            customer_name=(campos.get('cliente') or '').strip()
        )

        return JsonResponse({
            'success': True,
            'respuesta': f"✅ Venta registrada: {producto.name} x{cantidad} a ${precio_unit:.2f} (Total ${float(venta.total_amount):.2f})",
            'accion': 'registrar_venta',
            'datos': {'venta_id': venta.id}
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': f'Error al registrar venta: {str(e)}'})
