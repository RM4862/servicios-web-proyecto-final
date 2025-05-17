# middleware_api.py (placeholder)
import pika
import http.client
import urllib.request
import json
import ssl
from api.parser_xml import parse_generic_request
from api.adapters import mysql_adapter, firebase_adapter

RABBIT_HOST = 'localhost'
QUEUE_IN = 'api.request'
QUEUE_OUT = 'api.response'
SOAP_HOST = 'localhost'
SOAP_PORT = 9000
SOAP_PATH = '/soap'

def validar_token_google(token):
    try:
        url = f"https://oauth2.googleapis.com/tokeninfo?id_token={token}"
        context = ssl._create_unverified_context()
        with urllib.request.urlopen(url, context=context) as response:
            data = json.loads(response.read())
            print("Token válido de:", data.get("email"))
            return True
    except:
        return False

def enviar_soap(xml):
    headers = {'Content-Type': 'text/xml', 'Content-Length': str(len(xml))}
    conn = http.client.HTTPConnection(SOAP_HOST, SOAP_PORT)
    conn.request("POST", SOAP_PATH, body=xml.encode(), headers=headers)
    resp = conn.getresponse()
    resultado = resp.read().decode()
    conn.close()
    return resultado

def callback(ch, method, props, body):
    token = props.headers.get('Authorization', '').replace('Bearer ', '')
    if not validar_token_google(token):
        print("Token inválido")
        return

    xml = body.decode()
    parsed = parse_generic_request(xml)
    if not parsed:
        print("XML inválido")
        return

    interface = parsed["interface"]
    operation = parsed["operation"]
    params = parsed["parameters"]

    if interface == "SQL":
        if operation == "createDatabase":
            resultado = mysql_adapter.create_database(params["name"])
        elif operation == "insertRecord":
            resultado = mysql_adapter.insert_record(
                db_name=params["dbName"],
                table_name=params["tableName"],
                values={k: v for k, v in params.items() if k not in ["dbName", "tableName"]}
            )
        else:
            resultado = "Operación SQL no reconocida."

    elif interface == "NoSQL":
        if operation == "insertDocument":
            resultado = firebase_adapter.insert_document(
                collection=params["collection"],
                document={k: v for k, v in params.items() if k != "collection"}
            )
        else:
            resultado = "Operación NoSQL no reconocida."
    else:
        resultado = "Interface desconocida."

    ch.basic_publish(
        exchange='',
        routing_key=props.reply_to or QUEUE_OUT,
        body=resultado.encode(),
        properties=pika.BasicProperties(correlation_id=props.correlation_id)
    )

def iniciar():
    conexion = pika.BlockingConnection(pika.ConnectionParameters(RABBIT_HOST))
    canal = conexion.channel()
    canal.queue_declare(queue=QUEUE_IN)
    canal.queue_declare(queue=QUEUE_OUT)
    canal.basic_consume(queue=QUEUE_IN, on_message_callback=callback, auto_ack=True)
    print(f"Middleware escuchando {QUEUE_IN}...")
    canal.start_consuming()

if __name__ == '__main__':
    iniciar()
