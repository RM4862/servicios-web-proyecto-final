import urllib.request
import json
import ssl
import google.auth
from google.oauth2 import service_account
from google.auth.transport.requests import Request

FIREBASE_DB = "https://firestore.googleapis.com/v1/projects/proyectos-servicios-web-f/databases/(default)/documents"

#Funcion para obtener el token de google
def obtener_token():
    credentials = service_account.Credentials.from_service_account_file(
        'proyectos-servicios-web-f-firebase-adminsdk-fbsvc-d7cf017db5.json',
        scopes=['https://www.googleapis.com/auth/datastore']
    )
    credentials.refresh(Request())
    return credentials.token

#funcion para validar el token de google
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

#Funcion para crear una coleccion
def insert_document(collection, document):
    token = obtener_token()
    url = f"{FIREBASE_DB}/{collection}"
    data = {"fields": {k: {"stringValue": str(v)} for k, v in document.items()}}
    req = urllib.request.Request(url, data=json.dumps(data).encode(), method="POST")
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req) as res:
            return res.read().decode()
    except Exception as e:
        return f"Error insertando documento: {e}"
    
#Funcion para listar todos los documentos de una coleccion
def list_all(collection):
    token = obtener_token()
    url = f"{FIREBASE_DB}/{collection}"
    req = urllib.request.Request(url)
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req) as res:
            data = json.loads(res.read())
            docs = []
            for doc in data.get("documents", []):
                fields = doc.get("fields", {})
                flat = {}
                for k, v in fields.items():
                    if "integerValue" in v:
                        flat[k] = int(v["integerValue"])
                    elif "doubleValue" in v:
                        flat[k] = float(v["doubleValue"])
                    elif "stringValue" in v:
                        flat[k] = v["stringValue"]
                    else:
                        flat[k] = list(v.values())[0]
                docs.append(flat)
            return json.dumps(docs)
    except Exception as e:
        return json.dumps({"error": f"Error listando documentos: {e}"})

#Funcion para sumar un campo en una coleccion
def sum_field(collection, field):
    docs_json = list_all(collection)
    try:
        docs = json.loads(docs_json)
        if isinstance(docs, dict) and "error" in docs:
            return docs_json
        total = sum(float(doc.get(field, 0)) for doc in docs if field in doc)
        return json.dumps({f"sum_{field}": total})
    except Exception as e:
        return json.dumps({"error": f"Error en sum_field: {e}"})

#Funcion para obtener el promedio de un campo en una coleccion
def avg_field(collection, field):
    docs_json = list_all(collection)
    try:
        docs = json.loads(docs_json)
        if isinstance(docs, dict) and "error" in docs:
            return docs_json
        values = [float(doc.get(field, 0)) for doc in docs if field in doc]
        avg = sum(values) / len(values) if values else 0
        return json.dumps({f"avg_{field}": avg})
    except Exception as e:
        return json.dumps({"error": f"Error en avg_field: {e}"})

#Funcion para obtener los valores distintos de un campo en una coleccion
def distinct_field(collection, field):
    docs_json = list_all(collection)
    try:
        docs = json.loads(docs_json)
        if isinstance(docs, dict) and "error" in docs:
            return docs_json
        distinct = list(set(doc.get(field) for doc in docs if field in doc))
        return json.dumps({f"distinct_{field}": distinct})
    except Exception as e:
        return json.dumps({"error": f"Error en distinct_field: {e}"})
    
#Funcion para realizar un JOIN entre dos colecciones
def join_collections(collection1, collection2, local_field, foreign_field):
    docs1_json = list_all(collection1)
    docs2_json = list_all(collection2)
    try:
        docs1 = json.loads(docs1_json)
        docs2 = json.loads(docs2_json)
        if isinstance(docs1, dict) and "error" in docs1:
            return docs1_json
        if isinstance(docs2, dict) and "error" in docs2:
            return docs2_json
        # Simula un JOIN tipo SQL
        joined = []
        for doc1 in docs1:
            for doc2 in docs2:
                if doc1.get(local_field) == doc2.get(foreign_field):
                    joined.append({**doc1, **doc2})
        return json.dumps(joined)
    except Exception as e:
        return json.dumps({"error": f"Error en join_collections: {e}"})
    
#Funcion para actualizar un documento en una coleccion
def update_document(collection, document_id, updates):
    token = obtener_token()
    url = f"{FIREBASE_DB}/{collection}/{document_id}?updateMask.fieldPaths=" + ",".join(updates.keys())
    data = {"fields": {k: {"stringValue": str(v)} for k, v in updates.items()}}
    req = urllib.request.Request(url, data=json.dumps(data).encode(), method="PATCH")
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req) as res:
            return res.read().decode()
    except Exception as e:
        return f"Error actualizando documento: {e}"

#Funcion para eliminar un documento de una coleccion
def delete_document(collection, document_id):
    token = obtener_token()
    url = f"{FIREBASE_DB}/{collection}/{document_id}"
    req = urllib.request.Request(url, method="DELETE")
    req.add_header("Authorization", f"Bearer {token}")
    try:
        with urllib.request.urlopen(req) as res:
            return f"Documento {document_id} eliminado de {collection}"
    except Exception as e:
        return f"Error eliminando documento: {e}"