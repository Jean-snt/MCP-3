import os
import json
from datetime import datetime
from typing import Dict, Any, Optional
from .vertex_config import inicializar_vertex_ai, obtener_modelo
from .prompts import crear_prompt_avanzado, TipoAnalisis

class GestorIA:
    """
    Clase principal para gestionar todas las interacciones con IA
    de forma consistente y robusta.
    """
    
    _instancia = None
    
    def __init__(self, project_id: Optional[str] = None, location: str = "us-central1"):
        if GestorIA._instancia is not None:
            raise Exception("Esta clase es un Singleton. Usa GestorIA.obtener_instancia()")
        
        self.project_id = project_id or os.getenv('GOOGLE_CLOUD_PROJECT')
        self.location = location
        self.modelo = None
        self.modelo_nombre = None
        self.inicializado = False
        self.historico: list = []
        
        self.inicializar()
    
    @classmethod
    def obtener_instancia(cls, project_id=None, location="us-central1"):
        """Patrón Singleton para una única instancia del gestor"""
        if cls._instancia is None:
            cls._instancia = cls(project_id, location)
        return cls._instancia
    
    def inicializar(self) -> bool:
        """Inicializa la conexión con Vertex AI"""
        try:
            if inicializar_vertex_ai(self.project_id, self.location):
                self.modelo, self.modelo_nombre = obtener_modelo()
                self.inicializado = self.modelo is not None
            return self.inicializado
        except Exception as e:
            print(f"❌ Error en inicialización: {e}")
            return False
    
    def esta_disponible(self) -> bool:
        """Verifica si el servicio de IA está disponible"""
        return self.inicializado and self.modelo is not None
    
    def analizar_inventario(self, datos_inventario: Dict[str, Any], 
                          instrucciones_extra: str = "") -> Dict[str, Any]:
        """
        Analiza datos de inventario usando IA
        
        Args:
            datos_inventario (dict): Diccionario con datos del inventario
            instrucciones_extra (str): Instrucciones adicionales
        
        Returns:
            dict: Resultado del análisis
        """
        if not self.esta_disponible():
            return self._crear_respuesta_error("IA no disponible")
        
        try:
            # Formatear datos para el contexto
            contexto = self._formatear_contexto_inventario(datos_inventario)
            
            # Crear prompt optimizado
            prompt = crear_prompt_avanzado(
                contexto=contexto,
                tipo_analisis=TipoAnalisis.INVENTARIO,
                instrucciones_extra=instrucciones_extra
            )
            
            # Ejecutar análisis
            respuesta = self.modelo.generate_content(prompt)
            
            # Registrar en histórico
            self._registrar_analisis("inventario", datos_inventario, respuesta.text)
            
            return self._crear_respuesta_exitosa(
                analisis=respuesta.text,
                tipo="inventario",
                datos_utilizados=datos_inventario
            )
            
        except Exception as e:
            error_msg = f"Error en análisis de inventario: {str(e)}"
            print(f"❌ {error_msg}")
            return self._crear_respuesta_error(error_msg)
    
    def predecir_demanda(self, datos_ventas: Dict[str, Any],
                        horizonte: str = "30 días") -> Dict[str, Any]:
        """
        Predice demanda futura basada en datos históricos
        
        Args:
            datos_ventas (dict): Datos históricos de ventas
            horizonte (str): Período de predicción
        
        Returns:
            dict: Predicción y análisis
        """
        if not self.esta_disponible():
            return self._crear_respuesta_error("IA no disponible")
        
        try:
            contexto = self._formatear_contexto_ventas(datos_ventas, horizonte)
            
            prompt = crear_prompt_avanzado(
                contexto=contexto,
                tipo_analisis=TipoAnalisis.PREDICCION,
                instrucciones_extra=f"Horizonte de predicción: {horizonte}"
            )
            
            respuesta = self.modelo.generate_content(prompt)
            
            self._registrar_analisis("prediccion", datos_ventas, respuesta.text)
            
            return self._crear_respuesta_exitosa(
                analisis=respuesta.text,
                tipo="prediccion_demanda",
                datos_utilizados=datos_ventas,
                metadata={"horizonte": horizonte}
            )
            
        except Exception as e:
            error_msg = f"Error en predicción: {str(e)}"
            return self._crear_respuesta_error(error_msg)
    
    def analizar_tendencias(self, datos_tendencias: Dict[str, Any]) -> Dict[str, Any]:
        """Analiza tendencias del mercado"""
        if not self.esta_disponible():
            return self._crear_respuesta_error("IA no disponible")
        
        try:
            contexto = json.dumps(datos_tendencias, indent=2, ensure_ascii=False)
            
            prompt = crear_prompt_avanzado(
                contexto=contexto,
                tipo_analisis=TipoAnalisis.TENDENCIAS
            )
            
            respuesta = self.modelo.generate_content(prompt)
            
            return self._crear_respuesta_exitosa(
                analisis=respuesta.text,
                tipo="tendencias",
                datos_utilizados=datos_tendencias
            )
            
        except Exception as e:
            error_msg = f"Error en análisis de tendencias: {str(e)}"
            return self._crear_respuesta_error(error_msg)
    
    def _formatear_contexto_inventario(self, datos: Dict[str, Any]) -> str:
        """Formatea datos de inventario para el contexto"""
        productos = datos.get('productos', [])
        ventas = datos.get('ventas', [])
        metricas = datos.get('metricas', {})
        
        contexto = f"""
        INVENTARIO ACTUAL:
        - Total productos: {len(productos)}
        - Productos con stock bajo: {len([p for p in productos if p.get('stock_actual', 0) <= p.get('stock_minimo', 0)])}
        - Ventas registradas: {len(ventas)}
        
        PRODUCTOS DESTACADOS:
        {chr(10).join([f"• {p.get('nombre')}: Stock {p.get('stock_actual')} (Mín: {p.get('stock_minimo')}) - ${p.get('precio', 0)}" for p in productos[:10]])}
        
        MÉTRICAS PRINCIPALES:
        - Rotación: {metricas.get('rotacion', 'N/A')}
        - Margen promedio: {metricas.get('margen_promedio', 'N/A')}%
        - Días de inventario: {metricas.get('dias_inventario', 'N/A')}
        """
        
        return contexto
    
    def _formatear_contexto_ventas(self, datos: Dict[str, Any], horizonte: str) -> str:
        """Formatea datos de ventas para predicción"""
        return f"""
        DATOS HISTÓRICOS DE VENTAS:
        Período: {datos.get('periodo', 'No especificado')}
        Total de registros: {len(datos.get('ventas', []))}
        
        RESUMEN VENTAS:
        {json.dumps(datos.get('resumen', {}), indent=2, ensure_ascii=False)}
        
        HORIZONTE DE PREDICCIÓN: {horizonte}
        """
    
    def _crear_respuesta_exitosa(self, analisis: str, tipo: str, 
                               datos_utilizados: Dict, metadata: Dict = None) -> Dict[str, Any]:
        """Crea respuesta estandarizada para análisis exitoso"""
        return {
            "exito": True,
            "analisis": analisis,
            "tipo_analisis": tipo,
            "modelo_utilizado": self.modelo_nombre,
            "timestamp": datetime.now().isoformat(),
            "datos_utilizados": datos_utilizados,
            "metadata": metadata or {},
            "error": None
        }
    
    def _crear_respuesta_error(self, mensaje_error: str) -> Dict[str, Any]:
        """Crea respuesta estandarizada para errores"""
        return {
            "exito": False,
            "analisis": None,
            "tipo_analisis": None,
            "modelo_utilizado": None,
            "timestamp": datetime.now().isoformat(),
            "datos_utilizados": None,
            "metadata": {},
            "error": mensaje_error
        }
    
    def _registrar_analisis(self, tipo: str, datos_entrada: Dict, resultado: str):
        """Registra análisis en el histórico"""
        registro = {
            "tipo": tipo,
            "timestamp": datetime.now().isoformat(),
            "modelo": self.modelo_nombre,
            "datos_entrada_keys": list(datos_entrada.keys()),
            "resultado_resumen": resultado[:100] + "..." if len(resultado) > 100 else resultado
        }
        
        self.historico.append(registro)
        
        # Mantener solo los últimos 100 análisis
        if len(self.historico) > 100:
            self.historico.pop(0)
    
    def obtener_estadisticas(self) -> Dict[str, Any]:
        """Obtiene estadísticas de uso del gestor de IA"""
        return {
            "inicializado": self.inicializado,
            "modelo_actual": self.modelo_nombre,
            "total_analisis": len(self.historico),
            "proyecto": self.project_id,
            "ubicacion": self.location,
            "ultimos_analisis": self.historico[-5:] if self.historico else []
        }