"""
Modelos de base de datos para AngIA V5.0
"""

from sqlalchemy import Column, String, Integer, DateTime, Text, Boolean, Enum as SQLEnum, JSON
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
import enum

Base = declarative_base()


class OperatorEnum(str, enum.Enum):
    """Operadores de telecomunicaciones soportados"""
    CLARO = "CLARO"
    WOW = "WOW"
    WIN = "WIN"


class LeadStatusEnum(str, enum.Enum):
    """Estados del lead"""
    PENDING = "PENDING"  # Pendiente de contacto
    CONTACTED = "CONTACTED"  # Contactado
    INTERESTED = "INTERESTED"  # Interesado
    NOT_INTERESTED = "NOT_INTERESTED"  # No interesado
    CONVERTED = "CONVERTED"  # Convertido (venta realizada)
    FAILED = "FAILED"  # Fallido


class Lead(Base):
    """Modelo de Lead (prospecto de venta)"""
    __tablename__ = "leads"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Información del lead
    phone_number = Column(String(20), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=True)
    email = Column(String(255), nullable=True)
    
    # Operador actual y deseado
    current_operator = Column(SQLEnum(OperatorEnum), nullable=True)
    target_operator = Column(SQLEnum(OperatorEnum), nullable=False)
    
    # Estado del lead
    status = Column(SQLEnum(LeadStatusEnum), default=LeadStatusEnum.PENDING, nullable=False)
    
    # Información adicional
    notes = Column(Text, nullable=True)
    extra_data = Column(JSON, nullable=True)  # Datos adicionales flexibles
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    last_contacted_at = Column(DateTime(timezone=True), nullable=True)
    converted_at = Column(DateTime(timezone=True), nullable=True)


class Conversation(Base):
    """Modelo de Conversación (historial de mensajes)"""
    __tablename__ = "conversations"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Relación con el lead
    phone_number = Column(String(20), index=True, nullable=False)
    
    # Contenido del mensaje
    role = Column(String(20), nullable=False)  # 'user' o 'assistant'
    content = Column(Text, nullable=False)
    
    # Metadata
    extra_data = Column(JSON, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class Session(Base):
    """Modelo de Sesión (para rate limiting y control)"""
    __tablename__ = "sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Identificador de sesión
    phone_number = Column(String(20), unique=True, index=True, nullable=False)
    
    # Control de sesión
    is_active = Column(Boolean, default=True, nullable=False)
    message_count = Column(Integer, default=0, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    expires_at = Column(DateTime(timezone=True), nullable=False)
