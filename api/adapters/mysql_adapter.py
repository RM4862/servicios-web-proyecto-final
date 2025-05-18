import mysql.connector
import decimal

MYSQL_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '12345678a'
}

def create_database(db_name):
    conn = mysql.connector.connect(**MYSQL_CONFIG)
    cursor = conn.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
    conn.close()
    return f"Base de datos '{db_name}' creada."

def list_databases():
    conn = mysql.connector.connect(**MYSQL_CONFIG)
    cursor = conn.cursor()
    cursor.execute("SHOW DATABASES")
    result = [row[0] for row in cursor.fetchall()]
    conn.close()
    return {"databases": result}

def drop_database(db_name):
    conn = mysql.connector.connect(**MYSQL_CONFIG)
    cursor = conn.cursor()
    cursor.execute(f"DROP DATABASE IF EXISTS {db_name}")
    conn.close()
    return f"Base de datos '{db_name}' eliminada."

def create_table(db_name, table_name, columns):
    conn = mysql.connector.connect(database=db_name, **MYSQL_CONFIG)
    cursor = conn.cursor()
    cols = ", ".join([f"{col['name']} {col['type']}" for col in columns])
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({cols})")
    conn.commit()
    conn.close()
    return f"Tabla '{table_name}' creada en '{db_name}'."

def list_tables(db_name):
    conn = mysql.connector.connect(database=db_name, **MYSQL_CONFIG)
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES")
    result = [row[0] for row in cursor.fetchall()]
    conn.close()
    return {"tables": result}

def drop_table(db_name, table_name):
    conn = mysql.connector.connect(database=db_name, **MYSQL_CONFIG)
    cursor = conn.cursor()
    cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
    conn.commit()
    conn.close()
    return f"Tabla '{table_name}' eliminada de '{db_name}'."

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

def update_record(db_name, table_name, values, condition):
    conn = mysql.connector.connect(database=db_name, **MYSQL_CONFIG)
    cursor = conn.cursor()
    set_expr = ', '.join([f"{k} = %s" for k in values.keys()])
    query = f"UPDATE {table_name} SET {set_expr} WHERE {condition}"
    cursor.execute(query, list(values.values()))
    conn.commit()
    conn.close()
    return f"Registro actualizado en '{table_name}'."

def delete_record(db_name, table_name, condition):
    conn = mysql.connector.connect(database=db_name, **MYSQL_CONFIG)
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM {table_name} WHERE {condition}")
    conn.commit()
    conn.close()
    return f"Registro(s) eliminado(s) de '{table_name}'."

def select_records(db_name, table_name):
    conn = mysql.connector.connect(database=db_name, **MYSQL_CONFIG)
    cursor = conn.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM {table_name}")
    result = cursor.fetchall()
    conn.close()
    return result

def select_join(db_name, query):
    conn = mysql.connector.connect(database=db_name, **MYSQL_CONFIG)
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()
    return result

def aggregate_query(db_name, table, column, operation):
    conn = mysql.connector.connect(database=db_name, **MYSQL_CONFIG)
    cursor = conn.cursor()
    query = f"SELECT {operation}({column}) FROM {table}"
    cursor.execute(query)
    result = cursor.fetchone()[0]
    conn.close()
    if isinstance(result, decimal.Decimal):
        result = float(result)
    return {f"{operation}_{column}": result}

def select_distinct(db_name, table_name, column):
    conn = mysql.connector.connect(database=db_name, **MYSQL_CONFIG)
    cursor = conn.cursor()
    cursor.execute(f"SELECT DISTINCT {column} FROM {table_name}")
    result = [row[0] for row in cursor.fetchall()]
    conn.close()
    return {f"distinct_{column}": result}