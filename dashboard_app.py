import dash
from dash import dcc, html, Input, Output, dash_table
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import requests
import json
from datetime import datetime, timedelta
import dash_bootstrap_components as dbc

# Configuración de la aplicación Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Inventario Inteligente - Dashboard"

# URL base de la API
API_BASE_URL = "http://localhost:8000/api"

class DashboardData:
    """Clase para manejar la obtención de datos de la API"""
    
    def __init__(self):
        self.base_url = API_BASE_URL
    
    def get_data(self, endpoint):
        """Obtener datos de un endpoint de la API"""
        try:
            response = requests.get(f"{self.base_url}/{endpoint}")
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error {response.status_code}: {response.text}")
                return None
        except requests.exceptions.ConnectionError:
            print("Error: No se puede conectar con la API. Asegúrate de que el servidor Django esté ejecutándose.")
            return None
    
    def get_dashboard_data(self):
        """Obtener datos para el dashboard principal"""
        return self.get_data("analisis/dashboard/")
    
    def get_tendencias(self):
        """Obtener datos de tendencias"""
        return self.get_data("analisis/tendencias/")
    
    def get_sugerencias(self):
        """Obtener sugerencias de reabastecimiento"""
        return self.get_data("analisis/sugerencias_reabastecimiento/")

# Instancia global para manejo de datos
data_manager = DashboardData()

# Layout principal de la aplicación
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("🤖 Inventario Inteligente", className="text-center mb-4"),
            html.Hr()
        ])
    ]),
    
    # Tarjetas de métricas principales
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("📦 Productos", className="card-title"),
                    html.H2(id="total-productos", className="text-primary"),
                    html.P("Total en inventario", className="card-text")
                ])
            ], className="mb-3")
        ], width=3),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("⚠️ Bajo Stock", className="card-title"),
                    html.H2(id="productos-bajo-stock", className="text-warning"),
                    html.P("Necesitan reabastecimiento", className="card-text")
                ])
            ], className="mb-3")
        ], width=3),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("💰 Ventas del Mes", className="card-title"),
                    html.H2(id="ventas-mes", className="text-success"),
                    html.P("Transacciones realizadas", className="card-text")
                ])
            ], className="mb-3")
        ], width=3),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("📈 Ingresos", className="card-title"),
                    html.H2(id="ingresos-mes", className="text-info"),
                    html.P("Total generado", className="card-text")
                ])
            ], className="mb-3")
        ], width=3)
    ]),
    
    # Gráficos principales
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("📊 Ventas por Día (Últimos 7 días)"),
                dbc.CardBody([
                    dcc.Graph(id="grafico-ventas-dia")
                ])
            ])
        ], width=6),
        
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("🏆 Productos Más Vendidos"),
                dbc.CardBody([
                    dcc.Graph(id="grafico-productos-populares")
                ])
            ])
        ], width=6)
    ], className="mt-4"),
    
    # Análisis de tendencias
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("📈 Análisis de Tendencias"),
                dbc.CardBody([
                    dcc.Graph(id="grafico-tendencias")
                ])
            ])
        ], width=12)
    ], className="mt-4"),
    
    # Sugerencias de reabastecimiento
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("💡 Sugerencias de Reabastecimiento"),
                dbc.CardBody([
                    html.Div(id="tabla-sugerencias")
                ])
            ])
        ], width=12)
    ], className="mt-4"),
    
    # Controles de actualización
    dbc.Row([
        dbc.Col([
            dbc.Button("🔄 Actualizar Datos", id="btn-actualizar", color="primary", className="me-2"),
            dbc.Button("📊 Análisis Completo", id="btn-analisis", color="info"),
            html.Div(id="status-message", className="mt-2")
        ])
    ], className="mt-4"),
    
    # Intervalo de actualización automática
    dcc.Interval(
        id='interval-component',
        interval=30*1000,  # Actualizar cada 30 segundos
        n_intervals=0
    )
], fluid=True)

# Callbacks para actualizar los componentes
@app.callback(
    [Output('total-productos', 'children'),
     Output('productos-bajo-stock', 'children'),
     Output('ventas-mes', 'children'),
     Output('ingresos-mes', 'children')],
    [Input('interval-component', 'n_intervals'),
     Input('btn-actualizar', 'n_clicks')]
)
def update_metrics(n_intervals, n_clicks):
    """Actualizar las métricas principales"""
    data = data_manager.get_dashboard_data()
    
    if data:
        total_productos = len(data.get('productos_bajo_stock', [])) + 50  # Estimación
        productos_bajo_stock = len(data.get('productos_bajo_stock', []))
        ventas_mes = sum(day['ventas'] for day in data.get('ventas_por_dia', []))
        ingresos_mes = f"${ventas_mes * 25:,.0f}"  # Estimación basada en precio promedio
        
        return total_productos, productos_bajo_stock, ventas_mes, ingresos_mes
    else:
        return "N/A", "N/A", "N/A", "N/A"

@app.callback(
    Output('grafico-ventas-dia', 'figure'),
    [Input('interval-component', 'n_intervals'),
     Input('btn-actualizar', 'n_clicks')]
)
def update_sales_chart(n_intervals, n_clicks):
    """Actualizar gráfico de ventas por día"""
    data = data_manager.get_dashboard_data()
    
    if data and 'ventas_por_dia' in data:
        df = pd.DataFrame(data['ventas_por_dia'])
        fig = px.bar(df, x='fecha', y='ventas', 
                    title="Ventas por Día",
                    color='ventas',
                    color_continuous_scale='Blues')
        fig.update_layout(showlegend=False)
        return fig
    else:
        # Gráfico vacío si no hay datos
        fig = go.Figure()
        fig.add_annotation(text="No hay datos disponibles", 
                         xref="paper", yref="paper",
                         x=0.5, y=0.5, showarrow=False)
        return fig

@app.callback(
    Output('grafico-productos-populares', 'figure'),
    [Input('interval-component', 'n_intervals'),
     Input('btn-actualizar', 'n_clicks')]
)
def update_popular_products_chart(n_intervals, n_clicks):
    """Actualizar gráfico de productos populares"""
    data = data_manager.get_dashboard_data()
    
    if data and 'productos_mas_vendidos' in data:
        df = pd.DataFrame(data['productos_mas_vendidos'][:10])
        fig = px.bar(df, x='total_vendido', y='producto__nombre',
                    orientation='h',
                    title="Productos Más Vendidos",
                    color='total_vendido',
                    color_continuous_scale='Greens')
        fig.update_layout(showlegend=False)
        return fig
    else:
        fig = go.Figure()
        fig.add_annotation(text="No hay datos disponibles", 
                         xref="paper", yref="paper",
                         x=0.5, y=0.5, showarrow=False)
        return fig

@app.callback(
    Output('grafico-tendencias', 'figure'),
    [Input('btn-analisis', 'n_clicks')]
)
def update_trends_chart(n_clicks):
    """Actualizar gráfico de tendencias"""
    data = data_manager.get_tendencias()
    
    if data and 'tendencias_diarias' in data:
        df = pd.DataFrame(data['tendencias_diarias'])
        fig = px.line(df, x='dia', y='ventas', 
                     title="Tendencias de Ventas por Día de la Semana",
                     markers=True)
        fig.update_layout(xaxis_title="Día de la Semana", 
                         yaxis_title="Ventas")
        return fig
    else:
        fig = go.Figure()
        fig.add_annotation(text="No hay datos de tendencias disponibles", 
                         xref="paper", yref="paper",
                         x=0.5, y=0.5, showarrow=False)
        return fig

@app.callback(
    Output('tabla-sugerencias', 'children'),
    [Input('interval-component', 'n_intervals'),
     Input('btn-actualizar', 'n_clicks')]
)
def update_suggestions_table(n_intervals, n_clicks):
    """Actualizar tabla de sugerencias"""
    data = data_manager.get_sugerencias()
    
    if data and 'sugerencias' in data and data['sugerencias']:
        df = pd.DataFrame(data['sugerencias'])
        
        # Crear tabla con colores según urgencia
        table = dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[
                {"name": "Producto", "id": "producto"},
                {"name": "Stock Actual", "id": "stock_actual"},
                {"name": "Stock Mínimo", "id": "stock_minimo"},
                {"name": "Demanda Diaria", "id": "demanda_diaria_promedio"},
                {"name": "Días Restantes", "id": "dias_restantes_estimados"},
                {"name": "Cantidad Sugerida", "id": "cantidad_sugerida"},
                {"name": "Urgencia", "id": "urgencia"},
                {"name": "Proveedor", "id": "proveedor"}
            ],
            style_cell={'textAlign': 'left', 'padding': '10px'},
            style_data_conditional=[
                {
                    'if': {'filter_query': '{urgencia} = CRÍTICA'},
                    'backgroundColor': '#ffebee',
                    'color': 'black',
                },
                {
                    'if': {'filter_query': '{urgencia} = ALTA'},
                    'backgroundColor': '#fff3e0',
                    'color': 'black',
                },
                {
                    'if': {'filter_query': '{urgencia} = MEDIA'},
                    'backgroundColor': '#f3e5f5',
                    'color': 'black',
                }
            ],
            page_size=10
        )
        return table
    else:
        return html.Div([
            html.H5("✅ No hay productos que necesiten reabastecimiento inmediato", 
                   className="text-success text-center")
        ])

@app.callback(
    Output('status-message', 'children'),
    [Input('btn-actualizar', 'n_clicks')]
)
def update_status_message(n_clicks):
    """Mostrar mensaje de estado"""
    if n_clicks:
        return dbc.Alert("Datos actualizados correctamente", color="success", dismissable=True)
    return ""

if __name__ == '__main__':
    print("🚀 Iniciando Dashboard de Inventario Inteligente...")
    print("📊 Accede a: http://localhost:8050")
    print("⚠️  Asegúrate de que el servidor Django esté ejecutándose en http://localhost:8000")
    app.run_server(debug=True, host='0.0.0.0', port=8050)
