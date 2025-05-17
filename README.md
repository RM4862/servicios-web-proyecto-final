# Proyecto SOA: Plataforma asincrónica con SOAP, RabbitMQ, SQL/NoSQL y OAuth
Servicio con arquitectura SOA asincrónica basada en mensajes (RabbitMQ), este servicio ofrece el permitir a usuarios que desconozcan de SGBD (Sistema Gestor de Base de Datos ). 
El servicio contiene un flujo de validación básica implementada con la API de google para ser posible probarla desde Postman. 

## Componentes del servicio
- Broker: RabbitMQ
- API Middleware: Python
- Backend SQL: MySQL
- Backend NoSQL: Firebase Firestore (REST API)
- Servicios: Expuestos vía WSDL/SOAP
- Seguridad: OAuth 2.0 con Google

## Estructura del fichero

- /api: Middleware y adaptadores
- /soap: WSDL y XSD de cada servicio
- /pruebas: Scripts y peticiones Postman
- /docs: Diagramas de arquitectura
- firebase-credentials.json: Llave privada de Firebase (no compartir públicamente)

## Instrucciones de uso 

1. Instalar dependencias:
    Ya sea ejecutando 
    pip install -r requirements.txt

    o bien 
    pip install pika mysql-connector-python PyJWT

2. Ejecutar el middleware:

    python api/middleware_api.py

3. Enviar mensajes desde Postman a RabbitMQ usando el plugin de HTTP API (puerto 15672).
    *Nota: se sugiere el uso de Docker para tener el servicio de Rabbit MQ

4. Escuchar las respuestas:

    python pruebas/response_listener.py

## OAuth con Google

Sigue las instrucciones en `auth_google.py` para generar y validar tokens OAuth usando cuentas de Google.
