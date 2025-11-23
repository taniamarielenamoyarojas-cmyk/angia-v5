"""
API endpoints para webhooks de WhatsApp
"""

from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.webhook import WhatsAppWebhook, AIResponse, WhatsAppMessage
from app.services.ai_service import ai_service
from app.services.lead_service import lead_service
from app.models.lead import LeadStatusEnum
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/webhook", tags=["Webhook"])


@router.post("/whatsapp", response_model=list[AIResponse])
async def whatsapp_webhook(
    webhook: WhatsAppWebhook,
    db: Session = Depends(get_db),
    x_webhook_secret: str = Header(None)
):
    """
    Endpoint para recibir mensajes de WhatsApp
    
    Args:
        webhook: Datos del webhook
        db: Sesión de base de datos
        x_webhook_secret: Secret del webhook para autenticación
    
    Returns:
        Lista de respuestas generadas
    """
    # Validar webhook secret (si está configurado)
    if settings.WHATCHIM_WEBHOOK_SECRET != "pending":
        if x_webhook_secret != settings.WHATCHIM_WEBHOOK_SECRET:
            raise HTTPException(status_code=401, detail="Webhook secret inválido")
    
    responses = []
    
    for msg in webhook.messages:
        try:
            # Procesar mensaje
            response = await process_whatsapp_message(msg, db)
            responses.append(response)
            
        except Exception as e:
            logger.error(f"❌ Error procesando mensaje de {msg.from_number}: {str(e)}")
            # Continuar con los demás mensajes
            continue
    
    return responses


async def process_whatsapp_message(msg: WhatsAppMessage, db: Session) -> AIResponse:
    """
    Procesar un mensaje de WhatsApp individual
    
    Args:
        msg: Mensaje de WhatsApp
        db: Sesión de base de datos
    
    Returns:
        Respuesta generada por la IA
    """
    phone_number = msg.from_number
    user_message = msg.message
    
    logger.info(f"📱 Mensaje recibido de {phone_number}: {user_message[:50]}...")
    
    # 1. Obtener o crear sesión
    session = lead_service.get_or_create_session(db, phone_number)
    
    # 2. Obtener o crear lead (por defecto target_operator = CLARO)
    # TODO: Detectar operador objetivo del mensaje o base de datos de leads
    lead = lead_service.get_or_create_lead(db, phone_number, "CLARO")
    
    # 3. Guardar mensaje del usuario en historial
    lead_service.add_conversation_message(
        db,
        phone_number=phone_number,
        role="user",
        content=user_message,
        extra_data={"message_id": msg.message_id}
    )
    
    # 4. Obtener historial de conversación
    conversation_history = lead_service.get_conversation_history(db, phone_number)
    
    # 5. Generar respuesta con IA
    system_prompt = ai_service.get_system_prompt(
        target_operator=lead.target_operator.value,
        current_operator=lead.current_operator.value if lead.current_operator else None
    )
    
    ai_response_text = ai_service.generate_response(
        conversation_history=conversation_history,
        lead_info={
            "phone_number": phone_number,
            "target_operator": lead.target_operator.value,
            "current_operator": lead.current_operator.value if lead.current_operator else None,
        },
        system_prompt=system_prompt
    )
    
    # 6. Guardar respuesta de la IA en historial
    lead_service.add_conversation_message(
        db,
        phone_number=phone_number,
        role="assistant",
        content=ai_response_text
    )
    
    # 7. Actualizar estado del lead
    if lead.status == LeadStatusEnum.PENDING:
        lead_service.update_lead_status(db, phone_number, LeadStatusEnum.CONTACTED)
    
    # 8. Detectar intención (interesado, no interesado, etc.)
    # TODO: Implementar detección de intención con IA
    
    logger.info(f"✅ Respuesta generada para {phone_number}")
    
    return AIResponse(
        phone_number=phone_number,
        message=ai_response_text,
        lead_status=lead.status.value
    )


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION
    }
