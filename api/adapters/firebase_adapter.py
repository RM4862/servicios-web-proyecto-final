# firebase_adapter.py (placeholder)
import json
import time
import jwt
import urllib.request
import urllib.error

FIREBASE_CREDENTIALS_PATH = "C:/Users/avfmo/Documents/Servicios_web_proyecto/proyectos-servicios-web-f-firebase-adminsdk-fbsvc-fb8b184b4c.json"
FIREBASE_PROJECT_ID = "proyectos-servicios-web-f"
FIREBASE_DB = f"https://firestore.googleapis.com/v1/projects/{FIREBASE_PROJECT_ID}/databases/(default)/documents"

with open(FIREBASE_CREDENTIALS_PATH) as f:
    creds = json.load(f)

def obtener_token():
    now = int(time.time())
    payload = {
        'iss': creds['client_email'],
        'sub': creds['client_email'],
        'aud': 'https://oauth2.googleapis.com/token',
        'iat': now,
        'exp': now + 3600,
        'scope': 'https://www.googleapis.com/auth/datastore'
    }
    jwt_token = jwt.encode(payload, creds['private_key'], algorithm='RS256')
    data = json.dumps({'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer', 'assertion': jwt_token}).encode()
    req = urllib.request.Request('https://oauth2.googleapis.com/token', data=data, headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req) as res:
        response = json.loads(res.read())
        return response['access_token']

def insert_document(collection, document):
    token = obtener_token()
    url = f"{FIREBASE_DB}/{collection}"
    doc_fields = {k: {"stringValue": str(v)} for k, v in document.items()}
    body = json.dumps({"fields": doc_fields}).encode()
    req = urllib.request.Request(url, data=body)
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req) as res:
            result = res.read().decode()
            return result
    except urllib.error.HTTPError as e:
        return f"Error: {e.read().decode()}"