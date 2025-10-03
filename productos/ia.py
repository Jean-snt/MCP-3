import pandas as pd
from sklearn.linear_model import LinearRegression
from ventas.models import Venta
from productos.models import Producto

def predecir_demanda(producto_id):
    ventas = Venta.objects.filter(producto_id=producto_id).order_by('fecha_venta')
    if ventas.count() < 2:
        return "Datos insuficientes para predicción."
    
    df = pd.DataFrame(list(ventas.values('fecha_venta', 'cantidad_vendida')))
    df['timestamp'] = pd.to_datetime(df['fecha_venta']).map(pd.Timestamp.timestamp)
    
    X = df[['timestamp']]
    y = df['cantidad_vendida']
    
    modelo = LinearRegression()
    modelo.fit(X, y)
    
    proximo_timestamp = X['timestamp'].max() + 86400  # próximo día
    prediccion = modelo.predict([[proximo_timestamp]])
    
    return max(0, int(prediccion[0]))
