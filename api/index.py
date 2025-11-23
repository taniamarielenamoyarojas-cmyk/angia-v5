"""
Entry point para Vercel Serverless Functions
"""

from app.main import app

# Vercel espera que la aplicación ASGI se llame "app"
# y esté en el nivel raíz del módulo
