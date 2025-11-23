"""
Servicio de IA usando Manus API (OpenAI-compatible)
"""

from openai import OpenAI
from app.core.config import settings
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)


class AIService:
    """Servicio de IA para generar respuestas inteligentes"""
    
    def __init__(self):
        """Inicializar cliente de OpenAI (usando Gemini del sandbox)"""
        # El cliente OpenAI tomará OPENAI_API_KEY y OPENAI_BASE_URL del entorno
        self.client = OpenAI()
        logger.info("✅ AIService inicializado con OpenAI (Gemini 2.5 Flash)")
    
    def generate_response(
        self,
        conversation_history: List[Dict[str, str]],
        lead_info: Dict[str, any],
        system_prompt: str
    ) -> str:
        """
        Generar respuesta inteligente basada en el contexto
        
        Args:
            conversation_history: Historial de conversación [{"role": "user", "content": "..."}]
            lead_info: Información del lead (operador actual, target, etc.)
            system_prompt: Prompt del sistema con instrucciones
        
        Returns:
            Respuesta generada por la IA
        """
        try:
            # Construir mensajes para la API
            messages = [
                {"role": "system", "content": system_prompt}
            ]
            
            # Agregar historial de conversación (últimos N mensajes)
            messages.extend(conversation_history[-settings.MAX_CONVERSATION_HISTORY:])
            
            # Llamar a Manus API (compatible con OpenAI)
            response = self.client.chat.completions.create(
                model=settings.AI_MODEL,
                messages=messages,
                temperature=settings.AI_TEMPERATURE,
                max_tokens=settings.AI_MAX_TOKENS,
            )
            
            # Extraer respuesta
            ai_response = response.choices[0].message.content.strip()
            
            logger.info(f"✅ Respuesta generada para lead: {lead_info.get('phone_number', 'unknown')}")
            return ai_response
            
        except Exception as e:
            logger.error(f"❌ Error al generar respuesta: {str(e)}")
            return "Lo siento, estoy teniendo problemas técnicos. ¿Podrías intentar de nuevo en unos momentos?"
    
    def get_system_prompt(self, target_operator: str, current_operator: str = None) -> str:
        """
        Obtener prompt del sistema personalizado por operador
        
        Args:
            target_operator: Operador objetivo (CLARO, WOW, WIN)
            current_operator: Operador actual del cliente (opcional)
        
        Returns:
            System prompt personalizado
        """
        base_prompt = f"""Eres un agente de ventas experto de {target_operator} en Perú. 
Tu objetivo es convencer al cliente de cambiar su servicio de telecomunicaciones a {target_operator}.

INFORMACIÓN CLAVE:
- Operador objetivo: {target_operator}
- Operador actual del cliente: {current_operator or 'Desconocido'}

INSTRUCCIONES:
1. Sé amable, profesional y persuasivo
2. Destaca los beneficios de {target_operator}
3. Responde preguntas sobre planes, precios y cobertura
4. Si el cliente muestra interés, ofrece agendar una llamada con un asesor
5. Si el cliente no está interesado, agradece su tiempo cortésmente
6. Mantén respuestas cortas (máximo 2-3 oraciones)
7. Usa lenguaje natural y cercano (tú/usted según el tono del cliente)

BENEFICIOS POR OPERADOR:
"""
        
        # Agregar beneficios específicos por operador
        if target_operator == "CLARO":
            base_prompt += """
CLARO:
- Mayor cobertura 4G/5G en Perú
- Planes con más gigas y minutos
- Roaming internacional incluido
- App Mi Claro para gestionar tu línea
- Atención al cliente 24/7
"""
        elif target_operator == "WOW":
            base_prompt += """
WOW:
- Internet de fibra óptica ultra rápido
- Planes con Netflix, HBO Max incluidos
- Sin permanencia mínima
- Instalación gratis
- Precio fijo sin sorpresas
"""
        elif target_operator == "WIN":
            base_prompt += """
WIN:
- Planes económicos y flexibles
- Cobertura en todo Perú
- Recargas desde S/5
- Bonos de internet y llamadas
- Sin contratos ni permanencia
"""
        
        base_prompt += """
IMPORTANTE:
- NO inventes información que no conoces
- Si no sabes algo, di "Déjame verificar eso con un asesor especializado"
- NO prometas descuentos o promociones sin confirmar
- Mantén un tono profesional pero amigable
"""
        
        return base_prompt


# Instancia global del servicio
ai_service = AIService()
