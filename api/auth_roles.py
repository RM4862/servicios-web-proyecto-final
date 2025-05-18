import json
import os

USERS_FILE = "data/usuarios.json"
ADMIN_EMAIL = "ravelino.fa@gmail.com"

def cargar_usuarios():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE) as f:
        return json.load(f)

def guardar_usuarios(data):
    with open(USERS_FILE, "w") as f:
        json.dump(data, f, indent=2)

def get_user_role(email):
    if email == ADMIN_EMAIL:
        return "admin"
    usuarios = cargar_usuarios()
    if email in usuarios:
        return usuarios[email]
    else:
        usuarios[email] = "user"
        guardar_usuarios(usuarios)
        print(f"Nuevo usuario registrado: {email} como user")
        return "user"

def is_authorized(role, operation):
    permisos = {
        "admin": [
            "createDatabase", "listDatabases", "dropDatabase",
            "createTable", "listTables", "dropTable",
            "insertRecord", "updateRecord", "deleteRecord", "selectRecords",
            "selectJoin", "aggregateQuery", "insertDocument", "listAll"
        ],
        "user": [
            "insertRecord", "updateRecord", "deleteRecord", "selectRecords",
            "selectJoin", "aggregateQuery", "insertDocument", "listAll"
        ],
        "guest": ["listAll"]
    }
    return operation in permisos.get(role, [])
