"""
Schemas de Pydantic para validación de webhooks
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class WhatsAppMessage(BaseModel):
    """Schema para mensaje de WhatsApp entrante"""
    from_number: str = Field(..., description="Número de teléfono del remitente")
    message: str = Field(..., description="Contenido del mensaje")
    timestamp: Optional[datetime] = Field(default=None, description="Timestamp del mensaje")
    message_id: Optional[str] = Field(default=None, description="ID del mensaje")


class WhatsAppWebhook(BaseModel):
    """Schema para webhook de WhatsApp"""
    messages: List[WhatsAppMessage] = Field(..., description="Lista de mensajes")
    
    class Config:
        json_schema_extra = {
            "example": {
                "messages": [
                    {
                        "from_number": "+51987654321",
                        "message": "Hola, quiero información sobre planes",
                        "timestamp": "2025-11-23T10:30:00Z",
                        "message_id": "msg_123456"
                    }
                ]
            }
        }


class AIResponse(BaseModel):
    """Schema para respuesta de la IA"""
    phone_number: str = Field(..., description="Número de teléfono del destinatario")
    message: str = Field(..., description="Mensaje generado por la IA")
    lead_status: Optional[str] = Field(default=None, description="Estado del lead")
    
    class Config:
        json_schema_extra = {
            "example": {
                "phone_number": "+51987654321",
                "message": "¡Hola! Gracias por tu interés en CLARO. Tenemos planes desde S/35 con 20GB...",
                "lead_status": "CONTACTED"
            }
        }


class LeadCreate(BaseModel):
    """Schema para crear un lead"""
    phone_number: str = Field(..., description="Número de teléfono")
    name: Optional[str] = Field(default=None, description="Nombre del lead")
    email: Optional[str] = Field(default=None, description="Email del lead")
    current_operator: Optional[str] = Field(default=None, description="Operador actual")
    target_operator: str = Field(..., description="Operador objetivo (CLARO, WOW, WIN)")
    notes: Optional[str] = Field(default=None, description="Notas adicionales")


class LeadResponse(BaseModel):
    """Schema para respuesta de lead"""
    id: int
    phone_number: str
    name: Optional[str]
    email: Optional[str]
    current_operator: Optional[str]
    target_operator: str
    status: str
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True
