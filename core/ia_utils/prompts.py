from enum import Enum

class TipoAnalisis(Enum):
    INVENTARIO = "inventario"
    PREDICCION = "prediccion"
    TENDENCIAS = "tendencias"
    OPTIMIZACION = "optimizacion"

def crear_prompt_avanzado(contexto, tipo_analisis=TipoAnalisis.INVENTARIO, instrucciones_extra=None):
    """
    Crea prompts optimizados para diferentes tipos de análisis
    
    Args:
        contexto (str): Datos contextuales para el análisis
        tipo_analisis (TipoAnalisis): Tipo de análisis a realizar
        instrucciones_extra (str): Instrucciones adicionales específicas
    
    Returns:
        str: Prompt formateado y optimizado
    """
    
    prompts = {
        TipoAnalisis.INVENTARIO: """
        Eres un especialista senior en gestión de inventarios y optimización de cadena de suministro.

        CONTEXTO ACTUAL:
        {contexto}

        INSTRUCCIONES ESPECÍFICAS:
        1. Realiza un análisis exhaustivo del estado del inventario
        2. Identifica patrones, riesgos y oportunidades de optimización
        3. Proporciona recomendaciones cuantificadas y accionables
        4. Prioriza acciones por impacto y urgencia
        5. Incluye métricas específicas y KPIs sugeridos

        FORMATO DE RESPUESTA:
        ## 🎯 Análisis Ejecutivo
        [Resumen ejecutivo de máximo 3 líneas con los hallazgos clave]

        ## ⚠️ Alertas Críticas (Acción Inmediata)
        [Elementos que requieren atención urgente, con justificación]

        ## 📊 Análisis Detallado
        [Análisis profundo de la situación actual]

        ## 💡 Recomendaciones Estratégicas
        [Acciones específicas, ordenadas por prioridad e impacto]

        ## 📈 Métricas y Seguimiento
        [KPIs sugeridos para monitoreo continuo]

        {instrucciones_extra}

        Responde en español profesional, sé conciso pero completo.
        """,
        
        TipoAnalisis.PREDICCION: """
        Eres un científico de datos especializado en forecasting y series de tiempo.

        DATOS HISTÓRICOS:
        {contexto}

        Realiza análisis predictivo considerando:
        - Tendencias históricas y patrones estacionales
        - Factores externos relevantes (si se proporcionan)
        - Nivel de confianza estadística
        - Posibles escenarios disruptivos

        Proporciona:
        - Escenario base (más probable)
        - Escenario optimista (mejor caso)
        - Escenario conservador (peor caso)
        - Recomendaciones basadas en cada escenario

        {instrucciones_extra}

        Incluye rangos de confianza donde sea apropiado.
        """,
        
        TipoAnalisis.TENDENCIAS: """
        Eres un analista de mercado especializado en identificación de tendencias.

        DATOS PARA ANÁLISIS:
        {contexto}

        Analiza:
        - Tendencias emergentes y su sostenibilidad
        - Patrones cíclicos y estacionalidad
        - Cambios en el comportamiento del consumidor
        - Factores macroeconómicos relevantes

        {instrucciones_extra}

        Proporciona insights accionables basados en las tendencias identificadas.
        """,
        
        TipoAnalisis.OPTIMIZACION: """
        Eres un consultor especializado en optimización de procesos y eficiencia operativa.

        SITUACIÓN ACTUAL:
        {contexto}

        Enfoque de análisis:
        - Identificación de cuellos de botella
        - Oportunidades de automatización
        - Optimización de recursos
        - Mejora de procesos
        - Reducción de costos sin afectar calidad

        {instrucciones_extra}

        Proporciona un plan de implementación por fases.
        """
    }
    
    plantilla = prompts.get(tipo_analisis, prompts[TipoAnalisis.INVENTARIO])
    
    # Formatear el prompt
    instrucciones_extra = instrucciones_extra or ""
    prompt_final = plantilla.format(
        contexto=contexto,
        instrucciones_extra=instrucciones_extra
    )
    
    return prompt_final

def crear_prompt_rapido(contexto, objetivo="analizar"):
    """
    Versión simplificada para análisis rápidos
    
    Args:
        contexto (str): Datos a analizar
        objetivo (str): Objetivo del análisis
    
    Returns:
        str: Prompt simplificado
    """
    return f"""
    Objetivo: {objetivo}
    
    Datos:
    {contexto}
    
    Proporciona un análisis conciso y recomendaciones prácticas en español.
    """