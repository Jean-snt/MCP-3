# dashboard_app.py (reemplaza completamente tu archivo actual)
from dash import Dash, html, dcc, Input, Output
import pandas as pd
import plotly.express as px
import requests
import traceback

# -------------------
# Configuración
# -------------------
API_BASE = "http://127.0.0.1:8000/api"
USERNAME = "mil"   # si usas auth por user/pass en la API; si no, ajusta requests accordingly
PASSWORD = "123"

# Crear app (suppress no es necesario si layout contiene todo, pero lo ponemos por seguridad)
app = Dash(__name__, suppress_callback_exceptions=True)
server = app.server

# -------------------
# Helpers robustos
# -------------------
def fetch_endpoint(endpoint):
 """
 Llama al endpoint y devuelve la lista de resultados.
 Maneja paginación DRF (results) y errores.
 """
 url = f"{API_BASE}/{endpoint}/"
 try:
     r = requests.get(url, auth=(USERNAME, PASSWORD), timeout=8)
 except Exception as e:
     print("Error de conexión:", e)
     return [], f"Error de conexión: {e}"

 try:
     data = r.json()
 except Exception as e:
     print("Respuesta no JSON:", r.text[:500])
     return [], f"Respuesta no JSON: {e}"

 if r.status_code != 200:
     return [], f"Status {r.status_code}: {data}"

 # Si DRF devuelve paginado
 if isinstance(data, dict) and 'results' in data:
     return data['results'], None

 if isinstance(data, list):
     return data, None

 # si devuelve un dict individual (no lista)
 return [], "Respuesta no es lista ni paginada"

def safe_df(obj_list):
 """
 Convierte lista (posible vacía) a DataFrame seguro con columnas mínimas.
 """
 if not obj_list:
     return pd.DataFrame()
 try:
     return pd.DataFrame(obj_list)
 except Exception:
     # intentar normalizar objetos anidados
     try:
         return pd.json_normalize(obj_list)
     except Exception:
         return pd.DataFrame()

def to_numeric_col(df, col):
 if col in df.columns:
     df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
     df[col] = df[col].clip(lower=0)
 else:
     df[col] = 0
 return df

def extract_product_name_from_sales(df_sales, products_list):
 """
 Genera columna 'producto_nombre' en df_sales soportando:
 - ventas.producto = id (FK)
 - ventas.producto = objeto {id,nombre,...}
 - ventas.producto_nombre ya presente
 """
 if df_sales.empty:
     return df_sales

 # si existe producto_nombre ya
 if 'producto_nombre' in df_sales.columns:
     return df_sales

 # si 'producto' es dict/object
 if 'producto' in df_sales.columns:
     # si primer valor es dict -> extraer nombre
     first = df_sales['producto'].iloc[0]
     if isinstance(first, dict):
         df_sales['producto_nombre'] = df_sales['producto'].apply(lambda v: v.get('nombre') if isinstance(v, dict) else str(v))
         return df_sales

 # si tenemos products_list, crear map id->nombre
 mapping = {}
 for p in products_list:
     if isinstance(p, dict):
         pid = p.get('id') or p.get('pk') or None
         name = p.get('nombre') or p.get('name') or p.get('sku') or None
         if pid is not None and name is not None:
             mapping[pid] = name

 if 'producto' in df_sales.columns:
     df_sales['producto_nombre'] = df_sales['producto'].map(mapping).fillna(df_sales['producto'].astype(str))
 else:
     df_sales['producto_nombre'] = 'Desconocido'
 return df_sales

# -------------------
# Layout (AQUI ESTÁN TODOS LOS IDS)
# -------------------
app.layout = html.Div([
 html.H1("📊 Panel de Control - Smart Inventory", style={'textAlign': 'center'}),
 # Interval (este ID debe existir)
 dcc.Interval(id='interval-component', interval=30*1000, n_intervals=0),

 html.Div(id='status-box', style={'textAlign': 'center', 'color': 'red', 'margin': '6px'}),

 html.Div([
     html.H3("📦 Stock Actual de Productos"),
     dcc.Graph(id='grafico-stock', config={'displayModeBar': False})
 ]),

 html.Div([
     html.H3("💰 Precios de Productos"),
     dcc.Graph(id='grafico-precios', config={'displayModeBar': False})
 ]),

 html.Div([
     html.H3("📈 Predicción de Demanda (IA)"),
     dcc.Dropdown(id='sku-dropdown', placeholder='Selecciona SKU', style={'width':'40%'}),
     dcc.Graph(id='grafico-prediccion', config={'displayModeBar': False})
 ]),

 html.Div([
     html.H3("🧾 Historial de Ventas"),
     dcc.Graph(id='grafico-ventas', config={'displayModeBar': False})
 ])
])

# -------------------
# Callback principal
# -------------------
@app.callback(
 [
     Output('status-box', 'children'),
     Output('grafico-stock', 'figure'),
     Output('grafico-precios', 'figure'),
     Output('grafico-prediccion', 'figure'),
     Output('grafico-ventas', 'figure'),
     Output('sku-dropdown', 'options'),
     Output('sku-dropdown', 'value'),
 ],
 Input('interval-component', 'n_intervals')
)
def actualizar_todo(n_intervals):
 status_msgs = []

 products_data, err_p = fetch_endpoint('products')
 sales_data, err_s = fetch_endpoint('sales')

 if err_p:
     status_msgs.append(f"Products error: {err_p}")
 if err_s:
     status_msgs.append(f"Sales error: {err_s}")

 df_prod = safe_df(products_data)
 df_sales = safe_df(sales_data)

 # asegurar columnas y tipos
 if not df_prod.empty:
     # normalizar nombres de columnas comunes
     if 'nombre' not in df_prod.columns and 'name' in df_prod.columns:
         df_prod.rename(columns={'name': 'nombre'}, inplace=True)
     df_prod = to_numeric_col(df_prod, 'stock_actual')
     df_prod = to_numeric_col(df_prod, 'precio')
 else:
     df_prod = pd.DataFrame(columns=['id','sku','nombre','stock_actual','precio'])

 if not df_sales.empty:
     if 'cantidad' not in df_sales.columns:
         # intentar diferentes nombres
         for c in ['qty','quantity','cantidad_vendida']:
             if c in df_sales.columns:
                 df_sales.rename(columns={c:'cantidad'}, inplace=True)
                 break
     df_sales = to_numeric_col(df_sales, 'cantidad')
     # asegurar fecha en formato datetime
     if 'fecha' in df_sales.columns:
         df_sales['fecha'] = pd.to_datetime(df_sales['fecha'], errors='coerce')
     else:
         # si no existe, crear a partir de index (fallback)
         df_sales['fecha'] = pd.NaT
 else:
     df_sales = pd.DataFrame(columns=['producto','cantidad','fecha'])

 # extraer nombre de producto en ventas
 df_sales = extract_product_name_from_sales(df_sales, products_data)

 # --- GRAFICO STOCK (sin negativos y con escala controlada) ---
 if not df_prod.empty and 'nombre' in df_prod.columns:
     max_stock = int(df_prod['stock_actual'].max()) if not df_prod['stock_actual'].isna().all() else 1
     range_color = (0, max_stock if max_stock>0 else 1)
     fig_stock = px.bar(df_prod, x='nombre', y='stock_actual', color='stock_actual',
                        color_continuous_scale='Blues', range_color=range_color,
                        title='Stock por Producto')
     fig_stock.update_layout(yaxis=dict(title='Unidades', rangemode='tozero'), plot_bgcolor='white')
 else:
     fig_stock = px.bar(title='No hay datos de productos')

 # --- GRAFICO PRECIOS ---
 if not df_prod.empty and 'nombre' in df_prod.columns:
     max_price = float(df_prod['precio'].max()) if not df_prod['precio'].isna().all() else 1.0
     fig_precios = px.bar(df_prod, x='nombre', y='precio', color='precio',
                          color_continuous_scale='Greens', range_color=(0, max_price if max_price>0 else 1))
     fig_precios.update_layout(yaxis=dict(title='Precio'), plot_bgcolor='white')
 else:
     fig_precios = px.bar(title='No hay datos de precios')

 # --- GRAFICO VENTAS (scatter por fecha, con producto nombre) ---
 if not df_sales.empty and 'fecha' in df_sales.columns:
     # quitar filas sin fecha o cantidad
     df_sales = df_sales.dropna(subset=['fecha','cantidad'])
     fig_ventas = px.scatter(df_sales, x='fecha', y='cantidad', color='producto_nombre',
                             title='Historial de Ventas por Producto')
     fig_ventas.update_layout(yaxis=dict(title='Cantidad', rangemode='tozero'), plot_bgcolor='white')
 else:
     fig_ventas = px.scatter(title='No hay datos de ventas')

 # --- PREDICCIÓN (IA simple: regresión lineal por SKU) ---
 # construiremos una figura vacía y la llenaremos cuando el usuario seleccione SKU (para now, ponemos por defecto el primero)
 default_sku = None
 sku_options = []
 if products_data:
     for p in products_data:
         if isinstance(p, dict):
             sku = p.get('sku') or p.get('id')
             nombre = p.get('nombre') or p.get('name') or str(sku)
             sku_options.append({'label': nombre, 'value': sku})
     if sku_options:
         default_sku = sku_options[0]['value']

 # construir dummy prediccion (vacía) — el callback del dropdown real podría pedir /predictions/
 fig_pred = px.line(title='Selecciona un SKU para ver predicción')

 status = " | ".join(status_msgs) if status_msgs else "Conectado correctamente."
 return status, fig_stock, fig_precios, fig_pred, fig_ventas, sku_options, default_sku

# -------------------
# Callback para predicción por SKU (cuando el usuario elige)
# -------------------
@app.callback(
 Output('grafico-prediccion', 'figure'),
 Input('sku-dropdown', 'value')
)
def actualizar_prediccion_por_sku(sku):
 if not sku:
     return px.line(title='Selecciona un SKU para ver predicción')

 # LLAMADA al endpoint de predicciones (ajusta si tu endpoint requiere auth/header)
 try:
     r = requests.post(f"{API_BASE}/predictions/", json={"sku": sku, "days": 14}, auth=(USERNAME, PASSWORD), timeout=8)
     if r.status_code == 200:
         data = r.json()
         preds = data.get('predictions') or []
         if preds:
             dfp = pd.DataFrame(preds)
             # intentar normalizar nombres: 'fecha' y 'prediccion' esperados
             if 'fecha' in dfp.columns and 'prediccion' in dfp.columns:
                 dfp['fecha'] = pd.to_datetime(dfp['fecha'], errors='coerce')
                 dfp = dfp.dropna(subset=['fecha','prediccion'])
                 dfp['prediccion'] = pd.to_numeric(dfp['prediccion'], errors='coerce').fillna(0)
                 fig = px.line(dfp, x='fecha', y='prediccion', title=f'Predicción SKU {sku} (próx 14 días)', markers=True)
                 fig.update_layout(yaxis=dict(title='Predicción (unidades)', rangemode='tozero'), plot_bgcolor='white')
                 return fig
     # fallback simple: mensaje
     return px.line(title=f'No hay predicciones disponibles para {sku}')
 except Exception as e:
     print("Error al obtener predicción:", e)
     return px.line(title=f'Error al obtener predicción: {e}')

# -------------------
# Ejecutar app
# -------------------
if __name__ == '__main__':
 app.run_server(debug=True, port=8050)