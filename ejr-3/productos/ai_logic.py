"""
AI Logic Module - Lógica de Inteligencia Artificial para el Sistema de Inventario
Este módulo contiene toda la lógica de IA para predicciones, análisis y sugerencias.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models import Sum, Count, Avg, F
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.cluster import KMeans
import warnings
warnings.filterwarnings('ignore')

from productos.models import Producto, Venta, MovimientoInventario, Proveedor


class AIInventoryLogic:
    """
    Clase principal que contiene toda la lógica de IA para el sistema de inventario
    """
    
    def __init__(self):
        self.demand_model = LinearRegression()
        self.seasonality_model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.scaler = StandardScaler()
        self.clustering_model = KMeans(n_clusters=3, random_state=42)
        
    def predict_demand(self, producto_id, days_ahead=7):
        """
        Predice la demanda futura de un producto específico
        
        Args:
            producto_id (int): ID del producto
            days_ahead (int): Días hacia adelante para predecir
            
        Returns:
            dict: Predicciones con fechas y cantidades estimadas
        """
        try:
            producto = Producto.objects.get(id=producto_id)
        except Producto.DoesNotExist:
            return {"error": "Producto no encontrado"}
        
        # Obtener datos históricos de ventas (últimos 90 días)
        fecha_limite = timezone.now() - timedelta(days=90)
        ventas = Venta.objects.filter(
            producto=producto,
            fecha_venta__gte=fecha_limite
        ).order_by('fecha_venta')
        
        if len(ventas) < 7:
            return {
                "error": "Datos insuficientes",
                "message": "Se necesitan al menos 7 días de datos históricos",
                "data_points": len(ventas)
            }
        
        # Preparar datos para el modelo
        df_ventas = pd.DataFrame([
            {
                'fecha': venta.fecha_venta.date(),
                'cantidad': venta.cantidad_vendida,
                'dia_semana': venta.fecha_venta.weekday(),
                'dia_mes': venta.fecha_venta.day,
                'mes': venta.fecha_venta.month,
                'precio': float(venta.precio_unitario)
            }
            for venta in ventas
        ])
        
        # Agrupar por día
        df_diario = df_ventas.groupby('fecha').agg({
            'cantidad': 'sum',
            'dia_semana': 'first',
            'dia_mes': 'first',
            'mes': 'first',
            'precio': 'mean'
        }).reset_index()
        
        # Crear características
        X = df_diario[['dia_semana', 'dia_mes', 'mes', 'precio']].values
        y = df_diario['cantidad'].values
        
        # Normalizar características
        X_scaled = self.scaler.fit_transform(X)
        
        # Entrenar modelo
        self.demand_model.fit(X_scaled, y)
        
        # Generar predicciones
        predicciones = []
        fecha_actual = timezone.now().date()
        
        for i in range(days_ahead):
            fecha_prediccion = fecha_actual + timedelta(days=i)
            
            # Usar precio promedio histórico
            precio_promedio = df_diario['precio'].mean()
            
            caracteristicas = np.array([[
                fecha_prediccion.weekday(),
                fecha_prediccion.day,
                fecha_prediccion.month,
                precio_promedio
            ]])
            
            caracteristicas_scaled = self.scaler.transform(caracteristicas)
            demanda_predicha = max(0, self.demand_model.predict(caracteristicas_scaled)[0])
            
            predicciones.append({
                'fecha': fecha_prediccion.strftime('%Y-%m-%d'),
                'demanda_estimada': round(demanda_predicha, 2),
                'dia_semana': fecha_prediccion.strftime('%A'),
                'confianza': self._calculate_confidence(y, demanda_predicha)
            })
        
        # Calcular métricas de confianza
        confianza_general = self._calculate_overall_confidence(y)
        
        return {
            'producto': {
                'id': producto.id,
                'nombre': producto.nombre,
                'categoria': producto.categoria
            },
            'predicciones': predicciones,
            'confianza_general': confianza_general,
            'datos_historicos': len(df_diario),
            'demanda_promedio': round(np.mean(y), 2),
            'tendencia': self._calculate_trend(y),
            'fecha_analisis': timezone.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def analyze_trends(self, days_back=30):
        """
        Analiza tendencias generales del inventario
        
        Args:
            days_back (int): Días hacia atrás para el análisis
            
        Returns:
            dict: Análisis completo de tendencias
        """
        fecha_limite = timezone.now() - timedelta(days=days_back)
        
        # Productos con mayor rotación
        productos_alta_rotacion = Venta.objects.filter(
            fecha_venta__gte=fecha_limite
        ).values(
            'producto__id',
            'producto__nombre', 
            'producto__categoria'
        ).annotate(
            total_vendido=Sum('cantidad_vendida'),
            num_ventas=Count('id'),
            ingresos_totales=Sum('precio_unitario')
        ).order_by('-total_vendido')[:10]
        
        # Productos con menor rotación
        productos_baja_rotacion = Venta.objects.filter(
            fecha_venta__gte=fecha_limite
        ).values(
            'producto__id',
            'producto__nombre',
            'producto__categoria'
        ).annotate(
            total_vendido=Sum('cantidad_vendida'),
            num_ventas=Count('id'),
            ingresos_totales=Sum('precio_unitario')
        ).order_by('total_vendido')[:10]
        
        # Análisis por categoría
        ventas_por_categoria = Venta.objects.filter(
            fecha_venta__gte=fecha_limite
        ).values('producto__categoria').annotate(
            total_vendido=Sum('cantidad_vendida'),
            ingresos_totales=Sum('precio_unitario'),
            num_ventas=Count('id')
        ).order_by('-total_vendido')
        
        # Tendencias temporales
        tendencias_diarias = []
        dias_semana = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
        
        for i in range(7):
            ventas_dia = Venta.objects.filter(
                fecha_venta__gte=fecha_limite,
                fecha_venta__week_day=i+1
            ).aggregate(
                total_vendido=Sum('cantidad_vendida'),
                ingresos=Sum('precio_unitario')
            )
            
            tendencias_diarias.append({
                'dia': dias_semana[i],
                'ventas': ventas_dia['total_vendido'] or 0,
                'ingresos': float(ventas_dia['ingresos'] or 0)
            })
        
        # Análisis de estacionalidad mensual
        tendencias_mensuales = []
        meses = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 
                'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
        
        for i in range(1, 13):
            ventas_mes = Venta.objects.filter(
                fecha_venta__gte=fecha_limite,
                fecha_venta__month=i
            ).aggregate(
                total_vendido=Sum('cantidad_vendida'),
                ingresos=Sum('precio_unitario')
            )
            
            tendencias_mensuales.append({
                'mes': meses[i-1],
                'ventas': ventas_mes['total_vendido'] or 0,
                'ingresos': float(ventas_mes['ingresos'] or 0)
            })
        
        return {
            'periodo_analisis': f'Últimos {days_back} días',
            'productos_alta_rotacion': list(productos_alta_rotacion),
            'productos_baja_rotacion': list(productos_baja_rotacion),
            'ventas_por_categoria': list(ventas_por_categoria),
            'tendencias_diarias': tendencias_diarias,
            'tendencias_mensuales': tendencias_mensuales,
            'metricas_generales': self._calculate_general_metrics(fecha_limite)
        }
    
    def generate_replenishment_suggestions(self):
        """
        Genera sugerencias inteligentes de reabastecimiento
        
        Returns:
            dict: Sugerencias categorizadas por urgencia
        """
        sugerencias = []
        
        # Productos que necesitan reabastecimiento
        productos_bajo_stock = Producto.objects.filter(
            cantidad__lte=F('cantidad_minima')
        )
        
        for producto in productos_bajo_stock:
            # Calcular demanda promedio de los últimos 30 días
            fecha_limite = timezone.now() - timedelta(days=30)
            ventas_recientes = Venta.objects.filter(
                producto=producto,
                fecha_venta__gte=fecha_limite
            ).aggregate(
                total_vendido=Sum('cantidad_vendida'),
                dias_activos=Count('fecha_venta', distinct=True),
                precio_promedio=Avg('precio_unitario')
            )
            
            if ventas_recientes['total_vendido'] and ventas_recientes['dias_activos']:
                demanda_diaria = ventas_recientes['total_vendido'] / ventas_recientes['dias_activos']
                dias_restantes = producto.cantidad / demanda_diaria if demanda_diaria > 0 else 0
                
                # Calcular cantidad sugerida usando IA
                cantidad_sugerida = self._calculate_optimal_quantity(
                    producto, demanda_diaria, ventas_recientes['precio_promedio']
                )
                
                # Determinar urgencia
                urgencia = self._determine_urgency(dias_restantes, producto.cantidad_minima)
                
                # Calcular costo estimado
                costo_estimado = cantidad_sugerida * float(producto.precio_compra or 0)
                
                sugerencias.append({
                    'producto': {
                        'id': producto.id,
                        'nombre': producto.nombre,
                        'categoria': producto.categoria
                    },
                    'stock_actual': producto.cantidad,
                    'stock_minimo': producto.cantidad_minima,
                    'demanda_diaria_promedio': round(demanda_diaria, 2),
                    'dias_restantes_estimados': round(dias_restantes, 1),
                    'cantidad_sugerida': cantidad_sugerida,
                    'urgencia': urgencia,
                    'costo_estimado': round(costo_estimado, 2),
                    'proveedor': producto.proveedor.nombre if producto.proveedor else 'Sin proveedor',
                    'ubicacion': producto.ubicacion or 'No especificada'
                })
        
        # Ordenar por urgencia
        orden_urgencia = {'CRÍTICA': 1, 'ALTA': 2, 'MEDIA': 3, 'BAJA': 4}
        sugerencias.sort(key=lambda x: orden_urgencia.get(x['urgencia'], 5))
        
        # Calcular métricas de resumen
        total_costo = sum(s['costo_estimado'] for s in sugerencias)
        productos_criticos = len([s for s in sugerencias if s['urgencia'] == 'CRÍTICA'])
        
        return {
            'sugerencias': sugerencias,
            'resumen': {
                'total_productos_analizados': len(productos_bajo_stock),
                'productos_criticos': productos_criticos,
                'costo_total_estimado': round(total_costo, 2),
                'fecha_analisis': timezone.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        }
    
    def predict_seasonality(self, producto_id, months_ahead=6):
        """
        Predice patrones estacionales para un producto
        
        Args:
            producto_id (int): ID del producto
            months_ahead (int): Meses hacia adelante para predecir
            
        Returns:
            dict: Predicciones estacionales
        """
        try:
            producto = Producto.objects.get(id=producto_id)
        except Producto.DoesNotExist:
            return {"error": "Producto no encontrado"}
        
        # Obtener datos de los últimos 24 meses
        fecha_limite = timezone.now() - timedelta(days=730)
        ventas = Venta.objects.filter(
            producto=producto,
            fecha_venta__gte=fecha_limite
        ).order_by('fecha_venta')
        
        if len(ventas) < 30:
            return {"error": "Datos insuficientes para análisis estacional"}
        
        # Preparar datos mensuales
        df_ventas = pd.DataFrame([
            {
                'fecha': venta.fecha_venta,
                'cantidad': venta.cantidad_vendida,
                'mes': venta.fecha_venta.month,
                'trimestre': (venta.fecha_venta.month - 1) // 3 + 1,
                'precio': float(venta.precio_unitario)
            }
            for venta in ventas
        ])
        
        df_mensual = df_ventas.groupby('mes').agg({
            'cantidad': 'sum',
            'precio': 'mean'
        }).reset_index()
        
        # Calcular índices estacionales
        promedio_general = df_mensual['cantidad'].mean()
        indices_estacionales = {}
        
        for mes in range(1, 13):
            ventas_mes = df_mensual[df_mensual['mes'] == mes]['cantidad'].sum()
            if ventas_mes > 0:
                indices_estacionales[mes] = ventas_mes / promedio_general
            else:
                indices_estacionales[mes] = 0.5
        
        # Generar predicciones estacionales
        predicciones_estacionales = []
        fecha_actual = timezone.now()
        
        for i in range(months_ahead):
            fecha_prediccion = fecha_actual + timedelta(days=30*i)
            mes_prediccion = fecha_prediccion.month
            
            demanda_base = promedio_general
            factor_estacional = indices_estacionales.get(mes_prediccion, 1.0)
            demanda_predicha = demanda_base * factor_estacional
            
            predicciones_estacionales.append({
                'mes': fecha_prediccion.strftime('%Y-%m'),
                'mes_nombre': fecha_prediccion.strftime('%B'),
                'demanda_predicha': round(demanda_predicha, 2),
                'factor_estacional': round(factor_estacional, 2),
                'confianza': self._calculate_seasonal_confidence(df_mensual, mes_prediccion)
            })
        
        return {
            'producto': {
                'id': producto.id,
                'nombre': producto.nombre,
                'categoria': producto.categoria
            },
            'indices_estacionales': indices_estacionales,
            'promedio_mensual': round(promedio_general, 2),
            'predicciones_estacionales': predicciones_estacionales,
            'meses_analizados': len(df_mensual),
            'fecha_analisis': timezone.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def cluster_products(self, n_clusters=3):
        """
        Agrupa productos usando clustering para análisis de comportamiento
        
        Args:
            n_clusters (int): Número de clusters a crear
            
        Returns:
            dict: Resultados del clustering
        """
        # Obtener datos de todos los productos
        productos = Producto.objects.all()
        
        if len(productos) < n_clusters:
            return {"error": "No hay suficientes productos para clustering"}
        
        # Preparar características para clustering
        features = []
        productos_data = []
        
        for producto in productos:
            # Calcular métricas del producto
            ventas_totales = Venta.objects.filter(producto=producto).aggregate(
                total=Sum('cantidad_vendida')
            )['total'] or 0
            
            precio_promedio = float(producto.precio_venta or 0)
            rotacion = ventas_totales / max(producto.cantidad, 1)
            
            features.append([
                ventas_totales,
                precio_promedio,
                rotacion,
                producto.cantidad,
                producto.cantidad_minima
            ])
            
            productos_data.append({
                'id': producto.id,
                'nombre': producto.nombre,
                'categoria': producto.categoria
            })
        
        # Normalizar características
        features_scaled = self.scaler.fit_transform(features)
        
        # Aplicar clustering
        clusters = self.clustering_model.fit_predict(features_scaled)
        
        # Organizar resultados por cluster
        clusters_result = {}
        for i in range(n_clusters):
            clusters_result[f'cluster_{i}'] = {
                'productos': [],
                'caracteristicas_promedio': {}
            }
        
        for i, (producto_data, cluster) in enumerate(zip(productos_data, clusters)):
            clusters_result[f'cluster_{cluster}']['productos'].append(producto_data)
        
        # Calcular características promedio por cluster
        for cluster_id, cluster_data in clusters_result.items():
            cluster_idx = int(cluster_id.split('_')[1])
            cluster_features = [features[i] for i, c in enumerate(clusters) if c == cluster_idx]
            
            if cluster_features:
                avg_features = np.mean(cluster_features, axis=0)
                clusters_result[cluster_id]['caracteristicas_promedio'] = {
                    'ventas_promedio': round(avg_features[0], 2),
                    'precio_promedio': round(avg_features[1], 2),
                    'rotacion_promedio': round(avg_features[2], 2),
                    'stock_promedio': round(avg_features[3], 2),
                    'stock_minimo_promedio': round(avg_features[4], 2)
                }
        
        return {
            'clusters': clusters_result,
            'total_productos': len(productos),
            'fecha_analisis': timezone.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    
    # Métodos auxiliares privados
    
    def _calculate_confidence(self, historical_data, prediction):
        """Calcula la confianza de una predicción basada en datos históricos"""
        if len(historical_data) < 2:
            return 0
        
        std_dev = np.std(historical_data)
        mean_val = np.mean(historical_data)
        
        if mean_val == 0:
            return 0
        
        cv = std_dev / mean_val  # Coeficiente de variación
        confidence = max(0, min(100, 100 - (cv * 50)))
        
        return round(confidence, 1)
    
    def _calculate_overall_confidence(self, data):
        """Calcula la confianza general del modelo"""
        if len(data) < 5:
            return 0
        
        # Usar R² como medida de confianza
        mean_val = np.mean(data)
        ss_tot = np.sum((data - mean_val) ** 2)
        
        if ss_tot == 0:
            return 100
        
        # Simular R² basado en la variabilidad
        cv = np.std(data) / mean_val if mean_val > 0 else 1
        r_squared = max(0, min(1, 1 - cv))
        
        return round(r_squared * 100, 1)
    
    def _calculate_trend(self, data):
        """Calcula la tendencia de los datos"""
        if len(data) < 2:
            return "Sin datos suficientes"
        
        # Regresión lineal simple para determinar tendencia
        x = np.arange(len(data))
        slope = np.polyfit(x, data, 1)[0]
        
        if slope > 0.1:
            return "Creciente"
        elif slope < -0.1:
            return "Decreciente"
        else:
            return "Estable"
    
    def _calculate_optimal_quantity(self, producto, demanda_diaria, precio_promedio):
        """Calcula la cantidad óptima de reabastecimiento"""
        # Factor de seguridad basado en variabilidad histórica
        factor_seguridad = 1.5
        
        # Cantidad para 30 días de stock
        cantidad_base = int(demanda_diaria * 30 * factor_seguridad)
        
        # Asegurar que sea al menos el stock mínimo * 2
        cantidad_minima = producto.cantidad_minima * 2
        
        # Considerar el precio para ajustar la cantidad
        if precio_promedio and precio_promedio > 100:  # Productos caros
            factor_precio = 0.8
        else:
            factor_precio = 1.0
        
        cantidad_optima = max(cantidad_minima, int(cantidad_base * factor_precio))
        
        return cantidad_optima
    
    def _determine_urgency(self, dias_restantes, stock_minimo):
        """Determina la urgencia del reabastecimiento"""
        if dias_restantes < 1:
            return "CRÍTICA"
        elif dias_restantes < 3:
            return "ALTA"
        elif dias_restantes < 7:
            return "MEDIA"
        else:
            return "BAJA"
    
    def _calculate_seasonal_confidence(self, df_mensual, mes):
        """Calcula la confianza de predicciones estacionales"""
        mes_data = df_mensual[df_mensual['mes'] == mes]['cantidad']
        
        if len(mes_data) == 0:
            return 0
        
        # Confianza basada en la cantidad de datos históricos para ese mes
        confidence = min(100, len(mes_data) * 20)
        
        return round(confidence, 1)
    
    def _calculate_general_metrics(self, fecha_limite):
        """Calcula métricas generales del sistema"""
        total_ventas = Venta.objects.filter(fecha_venta__gte=fecha_limite).aggregate(
            total=Sum('cantidad_vendida')
        )['total'] or 0
        
        total_ingresos = Venta.objects.filter(fecha_venta__gte=fecha_limite).aggregate(
            total=Sum('precio_unitario')
        )['total'] or 0
        
        productos_activos = Venta.objects.filter(fecha_venta__gte=fecha_limite).values(
            'producto'
        ).distinct().count()
        
        return {
            'total_ventas': total_ventas,
            'total_ingresos': round(float(total_ingresos), 2),
            'productos_activos': productos_activos,
            'promedio_ventas_diarias': round(total_ventas / 30, 2)
        }


# Instancia global para uso en toda la aplicación
ai_logic = AIInventoryLogic()

