"""
Configuración de la aplicación AngIA V5.0
"""

from pydantic_settings import BaseSettings
from typing import Literal


class Settings(BaseSettings):
    """Configuración de la aplicación"""
    
    # Información de la aplicación
    APP_NAME: str = "AngIA V5.0"
    APP_VERSION: str = "5.0.0"
    APP_DESCRIPTION: str = "Sistema de Automatización de Ventas con IA para Telecomunicaciones"
    
    # Configuración del entorno
    ENVIRONMENT: Literal["development", "production"] = "development"
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"
    
    # OpenAI API (IA)
    OPENAI_API_KEY: str = ""  # Se tomará del entorno
    
    # PostgreSQL Database
    DATABASE_URL: str
    
    # WhatChimp API (WhatsApp)
    WHATCHIM_API_KEY: str = "pending"
    WHATCHIM_WEBHOOK_SECRET: str = "pending"
    WHATCHIM_BASE_URL: str = "https://api.whatchim.com/v1"
    
    # Configuración de la IA
    AI_MODEL: str = "gpt-4o-mini"  # Modelo de OpenAI (económico y rápido)
    AI_TEMPERATURE: float = 0.7
    AI_MAX_TOKENS: int = 500
    
    # Configuración de conversación
    MAX_CONVERSATION_HISTORY: int = 10  # Últimos 10 mensajes
    SESSION_TIMEOUT_MINUTES: int = 30
    
    # Operadores soportados
    SUPPORTED_OPERATORS: list[str] = ["CLARO", "WOW", "WIN"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Instancia global de configuración
settings = Settings()
