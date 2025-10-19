import os
import psycopg2
import redis
import time

print("--- Iniciando prueba de conexión ---")

try:
    print("Intentando conectar a PostgreSQL...")
    conn = psycopg2.connect(
        dbname=os.environ.get("POSTGRES_DB"),
        user=os.environ.get("POSTGRES_USER"),
        password=os.environ.get("POSTGRES_PASSWORD"),
        host="db_postgres",  
        port=os.environ.get("DB_PORT", "5432")
    )
    print("✅ Conexión a PostgreSQL exitosa.")
    conn.close()
except Exception as e:
    print(f"❌ Error al conectar a PostgreSQL: {e}")

print("-" * 20)

try:
    print("Intentando conectar a Redis...")
    r = redis.Redis(
        host="cache_redis",  # Usamos el nombre del servicio de Docker
        port=int(os.environ.get("REDIS_PORT", 6379)),
        db=0,
        decode_responses=True
    )
    r.ping()
    print("✅ Conexión a Redis exitosa.")
except Exception as e:
    print(f"❌ Error al conectar a Redis: {e}")

print("\n--- Prueba de conexión finalizada ---")
