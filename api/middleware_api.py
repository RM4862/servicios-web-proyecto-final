# middleware_api.py (placeholder)
import pika
import http.client
import urllib.request
import json
import ssl
from api.parser_xml import parse_generic_request
from api.adapters import mysql_adapter, firebase_adapter
from api.auth_roles import get_user_role, is_authorized

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
            print("Token válido. Usuario:", data.get("email"))
            return data
    except Exception as e:
        print("Token inválido:", str(e))
        return None

def callback(ch, method, props, body):
    token = props.headers.get('Authorization', '').replace('Bearer ', '')
    user_info = validar_token_google(token)
    if not user_info:
        return

    email = user_info.get("email")
    xml = body.decode()
    parsed = parse_generic_request(xml)

    if not parsed:
        return

    interface = parsed["interface"]
    operation = parsed["operation"]
    params = parsed["parameters"]
    rol = get_user_role(email)

    if not is_authorized(rol, operation):
        print(f"Usuario '{email}' (rol: {rol}) no tiene permiso para '{operation}'")
        return

    resultado = ""

    if interface == "SQL":
        if operation == "createDatabase":
            resultado = mysql_adapter.create_database(params["name"])
        elif operation == "listDatabases":
            resultado = json.dumps(mysql_adapter.list_databases())
        elif operation == "dropDatabase":
            resultado = mysql_adapter.drop_database(params["name"])
        elif operation == "createTable":
            db_name = params["dbName"]
            table_name = params["tableName"]
            columns = []
            i = 1
            while f"col{i}_name" in params and f"col{i}_type" in params:
                columns.append({
                    "name": params[f"col{i}_name"],
                    "type": params[f"col{i}_type"]
                })
                i += 1
            resultado = mysql_adapter.create_table(db_name, table_name, columns)
        elif operation == "listTables":
            resultado = json.dumps(mysql_adapter.list_tables(params["dbName"]))
        elif operation == "dropTable":
            resultado = mysql_adapter.drop_table(params["dbName"], params["tableName"])
        elif operation == "insertRecord":
            resultado = mysql_adapter.insert_record(
                params["dbName"], params["tableName"],
                {k: v for k, v in params.items() if k not in ["dbName", "tableName"]}
            )
        elif operation == "updateRecord":
            values = {k: v for k, v in params.items() if k not in ["dbName", "tableName", "condition"]}
            resultado = mysql_adapter.update_record(params["dbName"], params["tableName"], values, params["condition"])
        elif operation == "deleteRecord":
            resultado = mysql_adapter.delete_record(params["dbName"], params["tableName"], params["condition"])
        elif operation == "selectRecords":
            resultado = json.dumps(mysql_adapter.select_records(params["dbName"], params["tableName"]))
        elif operation == "selectJoin":
            resultado = json.dumps(mysql_adapter.select_join(params["dbName"], params["query"]))
        elif operation == "aggregateQuery":
            resultado = json.dumps(mysql_adapter.aggregate_query(params["dbName"], params["tableName"], params["column"], params["operation"]))
        else:
            resultado = f"Operación SQL desconocida: {operation}"

    elif interface == "NoSQL":
        if operation == "insertDocument":
            resultado = firebase_adapter.insert_document(
                params["collection"], {k: v for k, v in params.items() if k != "collection"}
            )
        else:
            resultado = f"Operación NoSQL desconocida: {operation}"
    else:
        resultado = "Interface no válida"

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
