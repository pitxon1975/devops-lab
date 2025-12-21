import socket
import os
import time
import psycopg2
from flask import Flask

app = Flask(__name__)

def get_db_connection():
    # Intento de conexión con reintento simple (la DB puede tardar en arrancar)
    retries = 5
    while retries > 0:
        try:
            conn = psycopg2.connect(
                host=os.environ['POSTGRES_HOST'],
                database=os.environ['POSTGRES_DB'],
                user=os.environ['POSTGRES_USER'],
                password=os.environ['POSTGRES_PASSWORD']
            )
            return conn
        except psycopg2.OperationalError:
            retries -= 1
            time.sleep(2)
    return None

def init_db():
    conn = get_db_connection()
    if conn:
        cur = conn.cursor()
        # Crear tabla si no existe (Idempotencia)
        cur.execute('CREATE TABLE IF NOT EXISTS visits (id SERIAL PRIMARY KEY, timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP);')
        conn.commit()
        cur.close()
        conn.close()

# Inicializar DB al arrancar la app
init_db()

@app.route('/')
def system_info():
    hostname = socket.gethostname()
    
    # Lógica de Base de Datos
    conn = get_db_connection()
    if conn:
        cur = conn.cursor()
        # 1. Registrar visita actual
        cur.execute('INSERT INTO visits DEFAULT VALUES;')
        conn.commit()
        # 2. Contar visitas totales
        cur.execute('SELECT COUNT(*) FROM visits;')
        total_visits = cur.fetchone()[0]
        cur.close()
        conn.close()
        db_status = f"Conectado a PostgreSQL. Visitas totales: <strong>{total_visits}</strong>"
    else:
        db_status = "Error crítico: No se puede conectar a la Base de Datos."

    return f"""
    <h1>DevOps Lab - Persistencia</h1>
    <p>Host del Contenedor: {hostname}</p>
    <p>Estado DB: {db_status}</p>
    """

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
