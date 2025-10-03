import dash
from dash import html, dcc
import plotly.express as px
import pandas as pd
import os, django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smart_inventory_project.settings')
django.setup()

from productos.models import Producto
from ventas.models import Venta

app = dash.Dash(__name__)

ventas = Venta.objects.all()
df = pd.DataFrame(list(ventas.values('producto__nombre', 'cantidad_vendida')))

fig = px.bar(df, x='producto__nombre', y='cantidad_vendida', title='Ventas por Producto')

app.layout = html.Div([
    html.H1("Dashboard de Inventario"),
    dcc.Graph(figure=fig)
])

if __name__ == '__main__':
    app.run(debug=True)
