import os
import psycopg2
import redis
from dotenv import load_dotenv
import time

load_dotenv()

IN_DOCKER = os.environ.get('IN_DOCKER', False)

db_host = "db" if IN_DOCKER else "localhost"
db_port = os.getenv("POSTGRES_PORT", "5432") 
db_name = os.getenv("POSTGRES_DB")
db_user = os.getenv("POSTGRES_USER")
db_password = os.getenv("POSTGRES_PASSWORD")

redis_host = "redis" if IN_DOCKER else "localhost"
redis_port = os.getenv("REDIS_PORT", "6379")


def test_postgres_connection():
    """Intenta conectar a la base de datos PostgreSQL."""
    print("Intentando conectar a PostgreSQL...")
    retries = 5
    delay = 3 
    conn = None
    for i in range(retries):
        try:
            conn = psycopg2.connect(
                dbname=db_name,
                user=db_user,
                password=db_password,
                host=db_host,
                port=db_port
            )
            print(f"Conexión a PostgreSQL exitosa en el puerto: {db_port}")
            conn.close()
            return True
        except psycopg2.OperationalError as e:
            print(f"Intento {i+1}/{retries} fallido: {e}")
            if "database system is starting up" in str(e) or "Connection refused" in str(e):
                 print(f"   Esperando {delay} segundos antes de reintentar...")
                 time.sleep(delay)
            else:
                 print("Error inesperado de PostgreSQL.")
                 return False 
        except Exception as e:
            print(f"Error inesperado al conectar a PostgreSQL: {e}")
            return False
    print("No se pudo conectar a PostgreSQL después de varios intentos.")
    return False

def test_redis_connection():
    """Intenta conectar y hacer ping al servidor Redis."""
    print("\nIntentando conectar a Redis...")
    try:
        r = redis.Redis(
            host=redis_host,
            port=int(redis_port),
            decode_responses=True 
        )
        r.ping()
        print("¡Conexión a Redis exitosa (Ping OK)!")
        return True
    except redis.exceptions.ConnectionError as e:
        print(f"Error al conectar a Redis: {e}")
        return False
    except Exception as e:
        print(f"Error inesperado al conectar a Redis: {e}")
        return False

if __name__ == "__main__":
    if not os.path.exists('.env'):
        try:
            with open('.env.example', 'r') as f_example, open('.env', 'w') as f_env:
                f_env.write(f_example.read())
            print("Archivo .env creado a partir de .env.example.")
            load_dotenv(override=True) 
            db_name = os.getenv("POSTGRES_DB")
            db_user = os.getenv("POSTGRES_USER")
            db_password = os.getenv("POSTGRES_PASSWORD")
            redis_port = os.getenv("REDIS_PORT", "6379")
        except FileNotFoundError:
             print("No se encontró .env.example. Asegúrate de tener un archivo .env con las variables necesarias.")
             exit()


    if not all([db_name, db_user, db_password, redis_port]):
        print("Faltan variables de entorno esenciales en el archivo .env.")
        print("Asegúrate de que POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD y REDIS_PORT estén definidos.")
    else:
        pg_success = test_postgres_connection()
        redis_success = test_redis_connection()

        print("\n--- Resumen de pruebas ---")
        print(f"PostgreSQL: {'EXITOSO' if pg_success else 'FALLIDO'}")
        print(f"Redis:      {'EXITOSO' if redis_success else 'FALLIDO'}")
        print("--------------------------")