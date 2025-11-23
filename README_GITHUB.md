# 🤖 AngIA V5.0 - Sistema de Automatización de Ventas con IA

Sistema inteligente de automatización de ventas para telecomunicaciones en Perú, procesando leads masivos vía WhatsApp con IA conversacional.

## 🚀 Características

- **Agente IA Conversacional**: Respuestas naturales y contextuales en español
- **Gestión de Leads**: Base de datos PostgreSQL con estados de conversión
- **WhatsApp Integration**: Webhook para recibir y enviar mensajes
- **Multi-Operador**: Personalización para CLARO, WOW y WIN
- **Importación Masiva**: Carga de leads desde CSV
- **API REST Completa**: Endpoints para gestión y estadísticas

## 🛠️ Stack Tecnológico

- **Backend**: FastAPI (Python 3.11+)
- **Base de Datos**: PostgreSQL (Neon)
- **IA**: OpenAI-compatible API (Gemini 2.5 Flash)
- **Hosting**: Vercel
- **WhatsApp**: WhatChimp API

## 📦 Instalación Local

```bash
# Clonar repositorio
git clone https://github.com/tu-usuario/angia-v5.git
cd angia-v5

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus credenciales

# Inicializar base de datos
python3 -c "from app.db.database import init_db; init_db()"

# Ejecutar servidor
python3 app/main.py
```

## 🌐 Despliegue en Vercel

1. Haz fork de este repositorio
2. Conecta tu cuenta de Vercel con GitHub
3. Importa el proyecto en Vercel
4. Configura las variables de entorno (ver `.env.example`)
5. Despliega

## 📊 Uso

### Importar Leads

```bash
python3 scripts/import_leads.py leads.csv --operator CLARO
```

### API Endpoints

- `GET /health` - Health check
- `POST /webhook/whatsapp` - Webhook de WhatsApp
- `GET /leads/stats/summary` - Estadísticas generales
- `GET /leads/stats/by-operator` - Estadísticas por operador

## 📄 Licencia

Propietario - Tania Marielena Moya Rojas

## 🤝 Soporte

Para soporte, contacta a: [tu-email]
