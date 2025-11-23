# 🚀 Guía de Despliegue en Vercel (GRATIS)

Esta guía te mostrará cómo desplegar AngIA V5.0 en Vercel, una plataforma de hosting que ofrece un generoso plan gratuito.

## 1. Requisitos Previos

- **Cuenta de GitHub**: Necesitarás una cuenta de GitHub para alojar tu código.
- **Cuenta de Vercel**: Regístrate en [Vercel](https://vercel.com) usando tu cuenta de GitHub.
- **Node.js y npm**: Asegúrate de tener Node.js y npm instalados en tu máquina local.

## 2. Preparar el Proyecto

### a. Crear archivo `vercel.json`

Crea un archivo llamado `vercel.json` en la raíz de tu proyecto (`/home/ubuntu/angia_v5/`) con el siguiente contenido:

```json
{
  "version": 2,
  "builds": [
    {
      "src": "app/main.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app/main.py"
    }
  ]
}
```

Este archivo le dice a Vercel cómo construir y enrutar tu aplicación FastAPI.

### b. Actualizar `requirements.txt`

Asegúrate de que tu archivo `requirements.txt` esté completo y actualizado.

### c. Subir a GitHub

1. Crea un nuevo repositorio en GitHub (puede ser privado).
2. Sube todo el contenido de la carpeta `/home/ubuntu/angia_v5/` a tu repositorio de GitHub.

## 3. Desplegar en Vercel

### a. Importar Proyecto

1. En tu dashboard de Vercel, haz clic en **"Add New..."** > **"Project"**.
2. Selecciona tu repositorio de GitHub.
3. Vercel detectará automáticamente que es un proyecto de Python.

### b. Configurar Variables de Entorno

Antes de desplegar, necesitas configurar las variables de entorno en Vercel:

1. Ve a la pestaña **"Settings"** > **"Environment Variables"**.
2. Agrega las siguientes variables:

   - **`DATABASE_URL`**: Tu connection string de Neon PostgreSQL.
   - **`WHATCHIM_API_KEY`**: Tu API key de WhatChimp (cuando la tengas).
   - **`WHATCHIM_WEBHOOK_SECRET`**: Tu webhook secret de WhatChimp (cuando lo tengas).
   - **`ENVIRONMENT`**: `production`
   - **`DEBUG`**: `False`
   - **`LOG_LEVEL`**: `INFO`

   **IMPORTANTE**: No necesitas agregar `OPENAI_API_KEY` ni `OPENAI_BASE_URL`, ya que Vercel los tomará del entorno del sandbox si lo ejecutas desde ahí. Si lo ejecutas localmente, sí necesitarás agregarlos.

### c. Desplegar

1. Haz clic en el botón **"Deploy"**.
2. Vercel construirá y desplegará tu aplicación.
3. Una vez completado, obtendrás una URL pública para tu aplicación (ej: `https://angia-v5.vercel.app`).

## 4. Configurar Webhook en WhatChimp

1. En tu cuenta de WhatChimp, ve a la configuración de webhooks.
2. Pega la URL de tu aplicación de Vercel seguida de `/webhook/whatsapp` (ej: `https://angia-v5.vercel.app/webhook/whatsapp`).
3. Guarda los cambios.

## ¡Listo! 🎉

Tu sistema AngIA V5.0 estará en línea y listo para recibir mensajes de WhatsApp.
