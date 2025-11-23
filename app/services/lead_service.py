"""
Servicio de gestión de leads
"""

from sqlalchemy.orm import Session
from app.models.lead import Lead, Conversation, Session as SessionModel, LeadStatusEnum, OperatorEnum
from datetime import datetime, timedelta, timezone
from typing import Optional, List
import logging

logger = logging.getLogger(__name__)


class LeadService:
    """Servicio para gestionar leads"""
    
    @staticmethod
    def get_or_create_lead(db: Session, phone_number: str, target_operator: str) -> Lead:
        """
        Obtener o crear un lead
        
        Args:
            db: Sesión de base de datos
            phone_number: Número de teléfono del lead
            target_operator: Operador objetivo (CLARO, WOW, WIN)
        
        Returns:
            Lead existente o recién creado
        """
        # Buscar lead existente
        lead = db.query(Lead).filter(Lead.phone_number == phone_number).first()
        
        if lead:
            logger.info(f"✅ Lead existente encontrado: {phone_number}")
            return lead
        
        # Crear nuevo lead
        lead = Lead(
            phone_number=phone_number,
            target_operator=OperatorEnum(target_operator),
            status=LeadStatusEnum.PENDING,
        )
        db.add(lead)
        db.commit()
        db.refresh(lead)
        
        logger.info(f"✅ Nuevo lead creado: {phone_number} -> {target_operator}")
        return lead
    
    @staticmethod
    def update_lead_status(db: Session, phone_number: str, status: LeadStatusEnum) -> Lead:
        """
        Actualizar estado del lead
        
        Args:
            db: Sesión de base de datos
            phone_number: Número de teléfono del lead
            status: Nuevo estado
        
        Returns:
            Lead actualizado
        """
        lead = db.query(Lead).filter(Lead.phone_number == phone_number).first()
        
        if not lead:
            raise ValueError(f"Lead no encontrado: {phone_number}")
        
        lead.status = status
        lead.updated_at = datetime.now(timezone.utc)
        
        if status == LeadStatusEnum.CONVERTED:
            lead.converted_at = datetime.now(timezone.utc)
        
        db.commit()
        db.refresh(lead)
        
        logger.info(f"✅ Lead actualizado: {phone_number} -> {status}")
        return lead
    
    @staticmethod
    def add_conversation_message(
        db: Session,
        phone_number: str,
        role: str,
        content: str,
        extra_data: dict = None
    ) -> Conversation:
        """
        Agregar mensaje al historial de conversación
        
        Args:
            db: Sesión de base de datos
            phone_number: Número de teléfono
            role: 'user' o 'assistant'
            content: Contenido del mensaje
            extra_data: Datos adicionales (opcional)
        
        Returns:
            Conversation creada
        """
        conversation = Conversation(
            phone_number=phone_number,
            role=role,
            content=content,
            extra_data=extra_data or {}
        )
        db.add(conversation)
        db.commit()
        db.refresh(conversation)
        
        logger.info(f"✅ Mensaje agregado: {phone_number} ({role})")
        return conversation
    
    @staticmethod
    def get_conversation_history(db: Session, phone_number: str, limit: int = 10) -> List[dict]:
        """
        Obtener historial de conversación
        
        Args:
            db: Sesión de base de datos
            phone_number: Número de teléfono
            limit: Número máximo de mensajes a retornar
        
        Returns:
            Lista de mensajes en formato [{"role": "user", "content": "..."}]
        """
        conversations = (
            db.query(Conversation)
            .filter(Conversation.phone_number == phone_number)
            .order_by(Conversation.created_at.desc())
            .limit(limit)
            .all()
        )
        
        # Invertir orden (más antiguo primero)
        conversations.reverse()
        
        # Convertir a formato de mensajes
        messages = [
            {"role": conv.role, "content": conv.content}
            for conv in conversations
        ]
        
        return messages
    
    @staticmethod
    def get_or_create_session(db: Session, phone_number: str) -> SessionModel:
        """
        Obtener o crear sesión activa
        
        Args:
            db: Sesión de base de datos
            phone_number: Número de teléfono
        
        Returns:
            Session activa
        """
        # Buscar sesión existente
        session = db.query(SessionModel).filter(SessionModel.phone_number == phone_number).first()
        
        now = datetime.now(timezone.utc)
        
        # Si existe y no ha expirado, retornar
        if session and session.expires_at > now:
            session.message_count += 1
            session.updated_at = now
            db.commit()
            db.refresh(session)
            return session
        
        # Si existe pero expiró, eliminar
        if session:
            db.delete(session)
            db.commit()
        
        # Crear nueva sesión
        session = SessionModel(
            phone_number=phone_number,
            is_active=True,
            message_count=1,
            expires_at=now + timedelta(minutes=30)  # 30 minutos de duración
        )
        db.add(session)
        db.commit()
        db.refresh(session)
        
        logger.info(f"✅ Nueva sesión creada: {phone_number}")
        return session


# Instancia global del servicio
lead_service = LeadService()
