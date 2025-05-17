# Proyecto SOA: Plataforma asincrónica con SOAP, RabbitMQ, SQL/NoSQL y OAuth

Este proyecto implementa una arquitectura SOA asincrónica basada en mensajes (RabbitMQ), con autenticación mediante OAuth (Google) y backends intercambiables en MySQL y Firebase. La comunicación se realiza con mensajes SOAP, enviados desde Postman o una app externa.

## 📦 Componentes

- Broker: RabbitMQ
- API Middleware: Python
- Backend SQL: MySQL
- Backend NoSQL: Firebase Firestore (REST API)
- Servicios: Expuestos vía WSDL/SOAP
- Seguridad: OAuth 2.0 con Google

## 📁 Estructura

- /api: Middleware y adaptadores
- /soap: WSDL y XSD de cada servicio
- /pruebas: Scripts y peticiones Postman
- /docs: Diagramas de arquitectura
- firebase-credentials.json: Llave privada de Firebase (no compartir públicamente)

## 🚀 Instrucciones

1. Instalar dependencias:

    pip install pika mysql-connector-python PyJWT

2. Ejecutar el middleware:

    python api/middleware_api.py

3. Enviar mensajes desde Postman a RabbitMQ usando el plugin de HTTP API (puerto 15672).

4. Escuchar las respuestas:

    python pruebas/response_listener.py

## 🔐 OAuth con Google

Sigue las instrucciones en `auth_google.py` para generar y validar tokens OAuth usando cuentas de Google.
