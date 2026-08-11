import os
from pathlib import Path
import psycopg2
from dotenv import load_dotenv

# Carga variables de entorno si existe archivo .env
load_dotenv(dotenv_path=Path(__file__).resolve().parents[1] / ".env")

class Conexion:
    @staticmethod
    def obtener_conexion():
        try:
            connection_kwargs = {
                "host": os.getenv("DB_HOST", "localhost"),
                "database": os.getenv("DB_NAME", "rancho_3_cultivos"),
                "user": os.getenv("DB_USER", "postgres"),
                "password": os.getenv("DB_PASSWORD", "tu_contraseña_aqui"),  # Cambia por tu contraseña de PostgreSQL
                "port": os.getenv("DB_PORT", "5432"),
                "client_encoding": "UTF8"
            }
            return psycopg2.connect(**connection_kwargs)
        except Exception as e:
            print(f"Error al conectar a PostgreSQL: {e}")
            return None
                