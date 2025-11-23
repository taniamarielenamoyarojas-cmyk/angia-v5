# AngIA V5.0 🤖📱

**Sistema de Automatización de Ventas con IA para Telecomunicaciones**

Desarrollado por: **Tania Marielena Moya Rojas**  
Fecha: **23 Noviembre 2025**

---

## 📋 Descripción

AngIA V5.0 es un sistema inteligente de automatización de ventas que utiliza IA (powered by Manus API) para gestionar conversaciones con leads vía WhatsApp. El sistema está diseñado para promover servicios de telecomunicaciones (CLARO, WOW, WIN) en Perú, procesando hasta 18,000+ leads con un objetivo de conversión del 80%.

## 🏗️ Arquitectura

```
WhatsApp (WhatChimp) → FastAPI → Agente IA (Manus) → PostgreSQL (Neon)
                          ↓
                   Respuestas automáticas
```

### Componentes:

- **FastAPI**: API REST para recibir webhooks de WhatsApp
- **Manus API**: IA generativa (OpenAI-compatible) con créditos UNLIMITED
- **PostgreSQL**: Base de datos (Neon - FREE tier, 0.5GB)
- **WhatChimp**: Proveedor de WhatsApp Business API

## 🚀 Características

✅ **Conversaciones inteligentes** con IA personalizada por operador  
✅ **Gestión de leads** con estados y seguimiento  
✅ **Historial de conversaciones** completo  
✅ **Rate limiting** y control de sesiones  
✅ **API REST** completa para integración  
✅ **Importación masiva** de leads desde CSV  
✅ **Estadísticas** en tiempo real  
✅ **100% gratuito** (infraestructura)

## 📦 Instalación

### 1. Clonar repositorio

```bash
cd /home/ubuntu/angia_v5
```

### 2. Instalar dependencias

```bash
pip3 install -r requirements.txt
```

### 3. Configurar variables de entorno

```bash
cp .env.example .env
# Editar .env con tus credenciales
```

### 4. Inicializar base de datos

```bash
python3 -c "from app.db.database import init_db; init_db()"
```

### 5. Ejecutar servidor

```bash
python3 app/main.py
```

El servidor estará disponible en: `http://localhost:8000`

## 📚 Documentación de API

Una vez iniciado el servidor, accede a:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### Endpoints principales:

#### Webhook de WhatsApp

```http
POST /webhook/whatsapp
Content-Type: application/json
X-Webhook-Secret: your-secret

{
  "messages": [
    {
      "from_number": "+51987654321",
      "message": "Hola, quiero información sobre planes",
      "timestamp": "2025-11-23T10:30:00Z",
      "message_id": "msg_123456"
    }
  ]
}
```

#### Crear Lead

```http
POST /leads/
Content-Type: application/json

{
  "phone_number": "+51987654321",
  "name": "Juan Pérez",
  "email": "juan@example.com",
  "current_operator": "WOW",
  "target_operator": "CLARO",
  "notes": "Cliente interesado en fibra óptica"
}
```

#### Listar Leads

```http
GET /leads/?skip=0&limit=100&status=CONTACTED&target_operator=CLARO
```

#### Estadísticas

```http
GET /leads/stats/summary
```

## 📊 Importar Leads desde CSV

### Formato del CSV:

```csv
phone_number,name,email,current_operator,notes
+51987654321,Juan Pérez,juan@example.com,WOW,Cliente interesado
+51987654322,María García,maria@example.com,WIN,Quiere fibra óptica
+51987654323,Carlos López,,CLARO,Llamar en la tarde
```

### Ejecutar importación:

```bash
python3 scripts/import_leads.py leads.csv --operator CLARO
```

## 🔧 Configuración

### Variables de entorno (.env):

```bash
# Manus API (IA)
MANUS_API_KEY=sk-your-key-here

# PostgreSQL (Neon)
DATABASE_URL=postgresql://user:pass@host:5432/db

# WhatChimp (WhatsApp)
WHATCHIM_API_KEY=your-key-here
WHATCHIM_WEBHOOK_SECRET=your-secret-here

# App Settings
ENVIRONMENT=development
DEBUG=True
LOG_LEVEL=INFO
```

## 📈 Estados de Leads

- **PENDING**: Pendiente de contacto
- **CONTACTED**: Contactado
- **INTERESTED**: Interesado
- **NOT_INTERESTED**: No interesado
- **CONVERTED**: Convertido (venta realizada)
- **FAILED**: Fallido

## 🎯 Operadores Soportados

- **CLARO**: Mayor cobertura 4G/5G en Perú
- **WOW**: Internet de fibra óptica ultra rápido
- **WIN**: Planes económicos y flexibles

## 🧪 Testing

### Probar webhook localmente:

```bash
curl -X POST http://localhost:8000/webhook/whatsapp \
  -H "Content-Type: application/json" \
  -H "X-Webhook-Secret: pending" \
  -d '{
    "messages": [
      {
        "from_number": "+51987654321",
        "message": "Hola, quiero información sobre planes de CLARO"
      }
    ]
  }'
```

### Verificar health check:

```bash
curl http://localhost:8000/health
```

## 🚀 Despliegue

### Opción 1: Vercel (Recomendado - GRATIS)

```bash
# Instalar Vercel CLI
npm install -g vercel

# Desplegar
vercel
```

### Opción 2: Railway.app

1. Conectar repositorio GitHub
2. Configurar variables de entorno
3. Desplegar automáticamente

### Opción 3: Fly.io

```bash
# Instalar Fly CLI
curl -L https://fly.io/install.sh | sh

# Desplegar
fly deploy
```

## 📝 Estructura del Proyecto

```
angia_v5/
├── app/
│   ├── __init__.py
│   ├── main.py              # Aplicación FastAPI principal
│   ├── api/
│   │   ├── webhook.py       # Endpoints de webhook
│   │   └── leads.py         # Endpoints de leads
│   ├── core/
│   │   └── config.py        # Configuración
│   ├── db/
│   │   └── database.py      # Configuración de DB
│   ├── models/
│   │   └── lead.py          # Modelos SQLAlchemy
│   ├── schemas/
│   │   └── webhook.py       # Schemas Pydantic
│   └── services/
│       ├── ai_service.py    # Servicio de IA (Manus)
│       └── lead_service.py  # Servicio de leads
├── scripts/
│   └── import_leads.py      # Script de importación
├── .env                     # Variables de entorno
├── .env.example             # Ejemplo de .env
├── requirements.txt         # Dependencias Python
└── README.md               # Este archivo
```

## 💰 Costos

### Infraestructura (FREE):
- ✅ **PostgreSQL** (Neon): $0/mes (0.5GB)
- ✅ **Manus API**: $0/mes (UNLIMITED hasta agosto 2026)
- ✅ **Vercel**: $0/mes (hosting)

### Servicios pagos:
- ⏳ **WhatChimp**: $36/mes (3 números WhatsApp)

**Total inicial**: $36/mes (solo WhatsApp)

## 🎓 Créditos

- **Desarrolladora**: Tania Marielena Moya Rojas
- **Email**: taniamarielenamoyarojas@gmail.com
- **IA**: Powered by Manus API
- **Database**: Neon PostgreSQL
- **WhatsApp**: WhatChimp Business API

## 📄 Licencia

Propiedad de Tania Marielena Moya Rojas. Todos los derechos reservados.

---

**¿Preguntas?** Contacta a taniamarielenamoyarojas@gmail.com
