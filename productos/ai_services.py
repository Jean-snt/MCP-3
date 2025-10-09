import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models import Sum, Count, Avg
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from .models import Producto, Venta, MovimientoInventario


class AIService:
    """Servicio de Inteligencia Artificial para análisis de inventario"""

    def __init__(self):
        self.modelo_demanda = LinearRegression()
        self.scaler = StandardScaler()

    def predecir_demanda(self, producto, dias_prediccion=7):
        """
        Predice la demanda futura de un producto usando regresión lineal
        """
        # Obtener datos históricos de ventas
        fecha_limite = timezone.now() - timedelta(days=90)  # Últimos 3 meses
        ventas = Venta.objects.filter(
            producto=producto,
            fecha_venta__gte=fecha_limite
        ).order_by('fecha_venta')

        if len(ventas) < 7:  # Necesitamos al menos una semana de datos
            return {
                'prediccion': 'Insuficientes datos históricos',
                'confianza': 0,
                'recomendacion': 'Recopilar más datos de ventas'
            }

        # Preparar datos para el modelo
        df_ventas = pd.DataFrame([
            {
                'fecha': venta.fecha_venta.date(),
                'cantidad': venta.cantidad_vendida,
                'dia_semana': venta.fecha_venta.weekday(),
                'dia_mes': venta.fecha_venta.day
            }
            for venta in ventas
        ])

        # Agrupar por día y sumar ventas
        df_diario = df_ventas.groupby('fecha').agg({
            'cantidad': 'sum',
            'dia_semana': 'first',
            'dia_mes': 'first'
        }).reset_index()

        # Crear características para el modelo
        X = df_diario[['dia_semana', 'dia_mes']].values
        y = df_diario['cantidad'].values

        # Entrenar el modelo
        self.modelo_demanda.fit(X, y)

        # Generar predicciones para los próximos días
        predicciones = []
        fecha_actual = timezone.now().date()
        
        for i in range(dias_prediccion):
            fecha_prediccion = fecha_actual + timedelta(days=i)
            caracteristicas = np.array([[fecha_prediccion.weekday(), fecha_prediccion.day]])
            demanda_predicha = max(0, self.modelo_demanda.predict(caracteristicas)[0])
            
            predicciones.append({
                'fecha': fecha_prediccion.strftime('%Y-%m-%d'),
                'demanda_predicha': round(demanda_predicha, 2),
                'dia_semana': fecha_prediccion.strftime('%A')
            })

        # Calcular confianza basada en la variabilidad de los datos históricos
        confianza = max(0, min(100, 100 - (np.std(y) / (np.mean(y) + 1)) * 20))

        return {
            'producto': producto.nombre,
            'predicciones': predicciones,
            'confianza': round(confianza, 1),
            'datos_historicos': len(df_diario),
            'demanda_promedio_historica': round(np.mean(y), 2)
        }

    def analizar_tendencias(self):
        """
        Analiza tendencias de ventas y rotación de productos
        """
        # Obtener datos de los últimos 30 días
        fecha_limite = timezone.now() - timedelta(days=30)
        
        # Productos con mayor rotación
        productos_rotacion = Venta.objects.filter(
            fecha_venta__gte=fecha_limite
        ).values('producto__nombre', 'producto__categoria').annotate(
            total_vendido=Sum('cantidad_vendida'),
            num_ventas=Count('id')
        ).order_by('-total_vendido')[:10]

        # Productos con menor rotación
        productos_baja_rotacion = Venta.objects.filter(
            fecha_venta__gte=fecha_limite
        ).values('producto__nombre', 'producto__categoria').annotate(
            total_vendido=Sum('cantidad_vendida'),
            num_ventas=Count('id')
        ).order_by('total_vendido')[:10]

        # Análisis por categoría
        ventas_por_categoria = Venta.objects.filter(
            fecha_venta__gte=fecha_limite
        ).values('producto__categoria').annotate(
            total_vendido=Sum('cantidad_vendida'),
            ingresos=Sum('precio_unitario')
        ).order_by('-total_vendido')

        # Tendencias temporales (ventas por día de la semana)
        tendencias_diarias = []
        for i in range(7):
            ventas_dia = Venta.objects.filter(
                fecha_venta__gte=fecha_limite,
                fecha_venta__week_day=i+1  # Django usa 1-7 para lunes-domingo
            ).aggregate(total=Sum('cantidad_vendida'))['total'] or 0
            
            dias_semana = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
            tendencias_diarias.append({
                'dia': dias_semana[i],
                'ventas': ventas_dia
            })

        return {
            'productos_alta_rotacion': list(productos_rotacion),
            'productos_baja_rotacion': list(productos_baja_rotacion),
            'ventas_por_categoria': list(ventas_por_categoria),
            'tendencias_diarias': tendencias_diarias,
            'periodo_analisis': 'Últimos 30 días'
        }

    def generar_sugerencias_reabastecimiento(self):
        """
        Genera sugerencias inteligentes de reabastecimiento
        """
        sugerencias = []
        
        # Productos que necesitan reabastecimiento inmediato
        productos_bajo_stock = Producto.objects.filter(
            cantidad__lte=models.F('cantidad_minima')
        )

        for producto in productos_bajo_stock:
            # Calcular demanda promedio de los últimos 30 días
            fecha_limite = timezone.now() - timedelta(days=30)
            ventas_recientes = Venta.objects.filter(
                producto=producto,
                fecha_venta__gte=fecha_limite
            ).aggregate(
                total_vendido=Sum('cantidad_vendida'),
                dias_activos=Count('fecha_venta', distinct=True)
            )

            if ventas_recientes['total_vendido'] and ventas_recientes['dias_activos']:
                demanda_diaria = ventas_recientes['total_vendido'] / ventas_recientes['dias_activos']
                dias_restantes = producto.cantidad / demanda_diaria if demanda_diaria > 0 else 0
                
                # Calcular cantidad sugerida para 30 días de stock
                cantidad_sugerida = max(
                    producto.cantidad_minima * 2,
                    int(demanda_diaria * 30)
                )

                urgencia = 'CRÍTICA' if dias_restantes < 3 else 'ALTA' if dias_restantes < 7 else 'MEDIA'

                sugerencias.append({
                    'producto': producto.nombre,
                    'stock_actual': producto.cantidad,
                    'stock_minimo': producto.cantidad_minima,
                    'demanda_diaria_promedio': round(demanda_diaria, 2),
                    'dias_restantes_estimados': round(dias_restantes, 1),
                    'cantidad_sugerida': cantidad_sugerida,
                    'urgencia': urgencia,
                    'proveedor': producto.proveedor.nombre if producto.proveedor else 'Sin proveedor'
                })

        # Ordenar por urgencia
        orden_urgencia = {'CRÍTICA': 1, 'ALTA': 2, 'MEDIA': 3}
        sugerencias.sort(key=lambda x: orden_urgencia.get(x['urgencia'], 4))

        return {
            'sugerencias': sugerencias,
            'total_productos_analizados': len(productos_bajo_stock),
            'fecha_analisis': timezone.now().strftime('%Y-%m-%d %H:%M:%S')
        }

    def predecir_estacionalidad(self, producto, meses_prediccion=3):
        """
        Predice patrones estacionales para un producto
        """
        # Obtener datos de los últimos 12 meses
        fecha_limite = timezone.now() - timedelta(days=365)
        ventas = Venta.objects.filter(
            producto=producto,
            fecha_venta__gte=fecha_limite
        ).order_by('fecha_venta')

        if len(ventas) < 30:
            return {'error': 'Insuficientes datos para análisis estacional'}

        # Preparar datos mensuales
        df_ventas = pd.DataFrame([
            {
                'fecha': venta.fecha_venta,
                'cantidad': venta.cantidad_vendida,
                'mes': venta.fecha_venta.month,
                'trimestre': (venta.fecha_venta.month - 1) // 3 + 1
            }
            for venta in ventas
        ])

        df_mensual = df_ventas.groupby('mes').agg({
            'cantidad': 'sum'
        }).reset_index()

        # Calcular índice estacional
        promedio_general = df_mensual['cantidad'].mean()
        indices_estacionales = {}
        
        for mes in range(1, 13):
            ventas_mes = df_mensual[df_mensual['mes'] == mes]['cantidad'].sum()
            if ventas_mes > 0:
                indices_estacionales[mes] = ventas_mes / promedio_general
            else:
                indices_estacionales[mes] = 0.5  # Valor por defecto

        return {
            'producto': producto.nombre,
            'indices_estacionales': indices_estacionales,
            'promedio_mensual': round(promedio_general, 2),
            'meses_analizados': len(df_mensual)
        }
