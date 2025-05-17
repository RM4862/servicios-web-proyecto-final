# mysql_adapter.py (placeholder)
import mysql.connector

MYSQL_CONFIG = {'host': 'localhost', 'user': 'root', 'password': '12345678a'}

def create_database(db_name):
    conn = mysql.connector.connect(**MYSQL_CONFIG)
    cursor = conn.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
    conn.close()
    return f"Base de datos '{db_name}' creada."

def insert_record(db_name, table_name, values):
    conn = mysql.connector.connect(database=db_name, **MYSQL_CONFIG)
    cursor = conn.cursor()
    keys = ', '.join(values.keys())
    val_placeholder = ', '.join(['%s'] * len(values))
    query = f"INSERT INTO {table_name} ({keys}) VALUES ({val_placeholder})"
    cursor.execute(query, list(values.values()))
    conn.commit()
    conn.close()
    return f"Registro insertado en '{table_name}'."