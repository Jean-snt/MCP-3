import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from django.utils import timezone
from django.db import models
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, r2_score
import joblib
import os
from django.conf import settings
from .models import Product, Sale

class DemandPredictionService:
    """Servicio para predicción de demanda usando Machine Learning"""
    
    def __init__(self):
        self.model_path = os.path.join(settings.BASE_DIR, 'modelos_ia')
        self.scaler_path = os.path.join(self.model_path, 'scaler.pkl')
        self.models = {}
        self.scalers = {}
        
        # Crear directorio de modelos si no existe
        os.makedirs(self.model_path, exist_ok=True)
    
    def prepare_sales_data(self, product_id, days_back=90):
        """Preparar datos de ventas para entrenamiento del modelo"""
        end_date = timezone.now()
        start_date = end_date - timedelta(days=days_back)
        
        # Obtener ventas del producto
        sales = Sale.objects.filter(
            product_id=product_id,
            sale_date__range=[start_date, end_date]
        ).order_by('sale_date')
        
        if not sales.exists():
            return None
        
        # Crear DataFrame con datos de ventas
        sales_data = []
        for sale in sales:
            sales_data.append({
                'date': sale.sale_date.date(),
                'quantity': sale.quantity_sold,
                'day_of_week': sale.sale_date.weekday(),
                'month': sale.sale_date.month,
                'day_of_month': sale.sale_date.day,
            })
        
        df = pd.DataFrame(sales_data)
        
        # Agrupar por fecha y sumar cantidades
        daily_sales = df.groupby('date').agg({
            'quantity': 'sum',
            'day_of_week': 'first',
            'month': 'first',
            'day_of_month': 'first'
        }).reset_index()
        
        # Rellenar fechas faltantes con 0
        date_range = pd.date_range(start=start_date.date(), end=end_date.date(), freq='D')
        full_df = pd.DataFrame({'date': date_range})
        full_df['date'] = pd.to_datetime(full_df['date'])
        daily_sales['date'] = pd.to_datetime(daily_sales['date'])
        
        merged_df = full_df.merge(daily_sales, on='date', how='left')
        merged_df['quantity'] = merged_df['quantity'].fillna(0)
        merged_df['day_of_week'] = merged_df['date'].dt.dayofweek
        merged_df['month'] = merged_df['date'].dt.month
        merged_df['day_of_month'] = merged_df['date'].dt.day
        
        return merged_df
    
    def create_features(self, df):
        """Crear características para el modelo de ML"""
        df = df.copy()
        
        # Características temporales
        df['is_weekend'] = (df['day_of_week'] >= 5).astype(int)
        df['is_month_start'] = (df['day_of_month'] <= 7).astype(int)
        df['is_month_end'] = (df['day_of_month'] >= 25).astype(int)
        
        # Promedio móvil de 7 días
        df['ma_7d'] = df['quantity'].rolling(window=7, min_periods=1).mean()
        
        # Promedio móvil de 30 días
        df['ma_30d'] = df['quantity'].rolling(window=30, min_periods=1).mean()
        
        # Tendencia (diferencia entre promedios móviles)
        df['trend'] = df['ma_7d'] - df['ma_30d']
        
        # Características cíclicas (sin/cos para capturar estacionalidad)
        df['day_sin'] = np.sin(2 * np.pi * df['day_of_week'] / 7)
        df['day_cos'] = np.cos(2 * np.pi * df['day_of_week'] / 7)
        df['month_sin'] = np.sin(2 * np.pi * df['month'] / 12)
        df['month_cos'] = np.cos(2 * np.pi * df['month'] / 12)
        
        return df
    
    def train_model(self, product_id):
        """Entrenar modelo para un producto específico"""
        df = self.prepare_sales_data(product_id)
        if df is None or len(df) < 14:  # Necesitamos al menos 2 semanas de datos
            return False
        
        # Crear características
        df = self.create_features(df)
        
        # Preparar datos de entrenamiento
        feature_columns = [
            'day_of_week', 'month', 'day_of_month', 'is_weekend',
            'is_month_start', 'is_month_end', 'ma_7d', 'ma_30d', 'trend',
            'day_sin', 'day_cos', 'month_sin', 'month_cos'
        ]
        
        # Usar datos desde el día 30 para tener promedios móviles
        train_data = df.iloc[30:].copy()
        
        if len(train_data) < 7:
            return False
        
        X = train_data[feature_columns].values
        y = train_data['quantity'].values
        
        # Escalar características
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # Entrenar modelo
        model = LinearRegression()
        model.fit(X_scaled, y)
        
        # Evaluar modelo
        y_pred = model.predict(X_scaled)
        mae = mean_absolute_error(y, y_pred)
        r2 = r2_score(y, y_pred)
        
        # Guardar modelo y escalador
        model_path = os.path.join(self.model_path, f'model_{product_id}.pkl')
        scaler_path = os.path.join(self.model_path, f'scaler_{product_id}.pkl')
        
        joblib.dump(model, model_path)
        joblib.dump(scaler, scaler_path)
        
        self.models[product_id] = model
        self.scalers[product_id] = scaler
        
        return {
            'success': True,
            'mae': mae,
            'r2_score': r2,
            'training_samples': len(train_data)
        }
    
    def load_model(self, product_id):
        """Cargar modelo entrenado para un producto"""
        model_path = os.path.join(self.model_path, f'model_{product_id}.pkl')
        scaler_path = os.path.join(self.model_path, f'scaler_{product_id}.pkl')
        
        if os.path.exists(model_path) and os.path.exists(scaler_path):
            self.models[product_id] = joblib.load(model_path)
            self.scalers[product_id] = joblib.load(scaler_path)
            return True
        return False
    
    def predict_demand(self, product_id, days_ahead=7):
        """Predecir demanda futura para un producto"""
        if product_id not in self.models:
            if not self.load_model(product_id):
                # Si no hay modelo, usar promedio histórico simple
                return self._simple_prediction(product_id, days_ahead)
        
        # Obtener datos recientes para características
        df = self.prepare_sales_data(product_id, days_back=60)
        if df is None:
            return self._simple_prediction(product_id, days_ahead)
        
        df = self.create_features(df)
        
        # Obtener la última fila como base para predicción
        last_row = df.iloc[-1].copy()
        
        predictions = []
        current_date = timezone.now().date()
        
        for i in range(days_ahead):
            # Crear características para el día futuro
            future_date = current_date + timedelta(days=i+1)
            future_features = last_row.copy()
            
            # Actualizar características temporales
            future_features['day_of_week'] = future_date.weekday()
            future_features['month'] = future_date.month
            future_features['day_of_month'] = future_date.day
            future_features['is_weekend'] = 1 if future_date.weekday() >= 5 else 0
            future_features['is_month_start'] = 1 if future_date.day <= 7 else 0
            future_features['is_month_end'] = 1 if future_date.day >= 25 else 0
            
            # Actualizar características cíclicas
            future_features['day_sin'] = np.sin(2 * np.pi * future_date.weekday() / 7)
            future_features['day_cos'] = np.cos(2 * np.pi * future_date.weekday() / 7)
            future_features['month_sin'] = np.sin(2 * np.pi * future_date.month / 12)
            future_features['month_cos'] = np.cos(2 * np.pi * future_date.month / 12)
            
            # Preparar características para predicción
            feature_columns = [
                'day_of_week', 'month', 'day_of_month', 'is_weekend',
                'is_month_start', 'is_month_end', 'ma_7d', 'ma_30d', 'trend',
                'day_sin', 'day_cos', 'month_sin', 'month_cos'
            ]
            
            X = future_features[feature_columns].values.reshape(1, -1)
            X_scaled = self.scalers[product_id].transform(X)
            
            # Hacer predicción
            prediction = self.models[product_id].predict(X_scaled)[0]
            predictions.append(max(0, prediction))  # No permitir predicciones negativas
        
        return {
            'predictions': predictions,
            'total_demand': sum(predictions),
            'average_daily': np.mean(predictions),
            'confidence': 'medium'  # Podríamos calcular esto basado en R²
        }
    
    def _simple_prediction(self, product_id, days_ahead):
        """Predicción simple basada en promedio histórico"""
        try:
            product = Product.objects.get(id=product_id)
            # 1) Usar promedio diario si existe
            avg_daily = float(product.average_daily_sales or 0)
            
            # 2) Si no hay promedio, intentar con total_sold distribuido
            if avg_daily <= 0 and (product.total_sold or 0) > 0:
                days_existing = max( (timezone.now() - (product.created_at or timezone.now())).days, 30)
                avg_daily = max(0.1, product.total_sold / days_existing)
            
            # 3) Heurística sin ventas: usar niveles de stock para estimar demanda
            if avg_daily <= 0:
                # Asume que el stock mínimo cubre ~7 días de ventas
                if (product.min_stock_level or 0) > 0:
                    avg_daily = max(0.2, product.min_stock_level / 7.0)
                else:
                    # Fallback: consumir ~5% del stock actual por día, acotado
                    avg_daily = max(0.2, min(5.0, (product.quantity or 0) * 0.05))
            
            predictions = [avg_daily] * days_ahead
            
            return {
                'predictions': predictions,
                'total_demand': avg_daily * days_ahead,
                'average_daily': avg_daily,
                'confidence': 'low'
            }
        except Product.DoesNotExist:
            return {
                'predictions': [0] * days_ahead,
                'total_demand': 0,
                'average_daily': 0,
                'confidence': 'none'
            }

class ReorderSuggestionService:
    """Servicio para sugerencias de reabastecimiento"""
    
    def __init__(self, prediction_service):
        self.prediction_service = prediction_service
    
    def calculate_reorder_suggestion(self, product_id):
        """Calcular sugerencia de reabastecimiento para un producto"""
        try:
            product = Product.objects.get(id=product_id)
            
            # Obtener predicción de demanda
            prediction_7d = self.prediction_service.predict_demand(product_id, 7)
            prediction_30d = self.prediction_service.predict_demand(product_id, 30)
            
            # Calcular días de suministro actual
            current_days_supply = product.days_of_supply
            
            # Ajustar promedio por estacionalidad si está definido
            seasonality = getattr(product, 'seasonality_index', 1.0) or 1.0
            # Ajuste por promoción: si hay promo, multiplicar por (1 + descuento%)
            promo_factor = 1.0
            try:
                if getattr(product, 'promotion_active', False):
                    discount = float(getattr(product, 'current_discount', 0) or 0) / 100.0
                    promo_factor = max(1.0, 1.0 + discount)
            except Exception:
                promo_factor = 1.0

            adj_avg7 = prediction_7d['average_daily'] * seasonality * promo_factor

            # Determinar si necesita reabastecimiento
            needs_reorder = (
                product.quantity <= product.min_stock_level or
                current_days_supply < 7 or
                adj_avg7 * 7 > product.quantity
            )
            
            # Calcular cantidad sugerida
            if needs_reorder:
                # Demanda durante el lead time y stock de seguridad
                lead_time = getattr(product, 'lead_time_days', 7) or 7
                safety_stock = getattr(product, 'safety_stock', 0) or int(product.min_stock_level * 1.0)
                demand_lead_time = adj_avg7 * lead_time
                predicted_demand_30d = prediction_30d['total_demand'] * seasonality * promo_factor
                suggested_quantity = max(
                    product.max_stock_level - product.quantity,
                    int(demand_lead_time + safety_stock - product.quantity)
                )
                suggested_quantity = max(0, suggested_quantity)
            else:
                suggested_quantity = 0
            
            # Actualizar producto con predicciones
            product.predicted_demand_7d = prediction_7d['average_daily']
            product.predicted_demand_30d = prediction_30d['average_daily']
            product.reorder_suggestion = needs_reorder
            product.reorder_quantity = suggested_quantity
            product.save()
            
            return {
                'product_id': product_id,
                'product_name': product.name,
                'current_stock': product.quantity,
                'min_stock_level': product.min_stock_level,
                'days_of_supply': current_days_supply,
                'needs_reorder': needs_reorder,
                'predicted_demand_7d': prediction_7d['average_daily'],
                'predicted_demand_30d': prediction_30d['average_daily'],
                'suggested_quantity': suggested_quantity,
                'confidence': prediction_7d['confidence'],
                'reason': self._get_reorder_reason(product, current_days_supply, prediction_7d)
            }
            
        except Product.DoesNotExist:
            return None
    
    def _get_reorder_reason(self, product, days_supply, prediction_7d):
        """Obtener razón para la sugerencia de reabastecimiento"""
        if product.quantity <= product.min_stock_level:
            return "Stock por debajo del nivel mínimo"
        elif days_supply < 7:
            return "Días de suministro insuficientes"
        elif prediction_7d['total_demand'] > product.quantity:
            return "Demanda predicha excede stock actual"
        else:
            return "No requiere reabastecimiento inmediato"

class TrendAnalysisService:
    """Servicio para análisis de tendencias"""
    
    def analyze_trends(self, days_back=30):
        """Analizar tendencias generales del inventario"""
        end_date = timezone.now()
        start_date = end_date - timedelta(days=days_back)
        
        # Análisis de ventas
        sales = Sale.objects.filter(sale_date__range=[start_date, end_date])
        
        # Top productos vendidos
        top_selling = sales.values('product__name', 'product__id').annotate(
            total_sold=models.Sum('quantity_sold'),
            total_revenue=models.Sum('total_amount')
        ).order_by('-total_sold')[:10]
        
        # Productos con stock bajo
        low_stock_products = Product.objects.filter(
            quantity__lte=models.F('min_stock_level') * 1.2
        )
        
        # Estadísticas generales
        total_revenue = sales.aggregate(total=models.Sum('total_amount'))['total'] or 0
        total_products = Product.objects.count()
        products_needing_reorder = Product.objects.filter(reorder_suggestion=True).count()
        
        return {
            'period_days': days_back,
            'top_selling_products': list(top_selling),
            'low_stock_products': list(low_stock_products.values('id', 'name', 'quantity', 'min_stock_level')),
            'total_revenue': total_revenue,
            'total_products': total_products,
            'products_needing_reorder': products_needing_reorder,
            'analysis_date': timezone.now()
        }