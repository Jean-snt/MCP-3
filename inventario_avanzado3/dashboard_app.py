from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd

app = Dash(__name__)
server = app.server

# ======== LAYOUT (todos los IDs aquí) =========
app.layout = html.Div([
    html.H2("🔧 Dashboard Prueba — Verificación de IDs", style={'textAlign': 'center'}),
    dcc.Interval(id='interval-component', interval=5000, n_intervals=0),
    dcc.Dropdown(id='sku-dropdown', options=[], value=None),
    dcc.Graph(id='grafico-stock'),
    dcc.Graph(id='grafico-precios'),
    dcc.Graph(id='grafico-prediccion'),
    dcc.Graph(id='grafico-ventas'),
])

# ======== CALLBACK PRINCIPAL =========
@app.callback(
    [
        Output('grafico-stock', 'figure'),
        Output('grafico-precios', 'figure'),
        Output('grafico-prediccion', 'figure'),
        Output('grafico-ventas', 'figure'),
        Output('sku-dropdown', 'options'),
        Output('sku-dropdown', 'value'),
    ],
    Input('interval-component', 'n_intervals')
)
def actualizar(n):
    df = pd.DataFrame({'nombre': ['A', 'B', 'C'], 'valor': [10, 15, 8]})
    fig1 = px.bar(df, x='nombre', y='valor', title='Stock')
    fig2 = px.bar(df, x='nombre', y='valor', title='Precios', color='valor')
    fig3 = px.line(df, x='nombre', y='valor', title='Predicción')
    fig4 = px.scatter(df, x='nombre', y='valor', title='Ventas')
    opts = [{'label': i, 'value': i} for i in df['nombre']]
    return fig1, fig2, fig3, fig4, opts, 'A'

if __name__ == "__main__":
    app.run_server(debug=True, port=8050)
