import os
from getpass import getpass
from pathlib import Path

import psycopg2

from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).resolve().parents[1] / ".env", encoding="latin-1", override=True)


class Conexion:

    @staticmethod
    def obtener_conexion():
        connection_kwargs = dict(
            host = os.getenv("DB_HOST", "localhost"),
            database = os.getenv("DB_NAME", "rancho_3_cultivos"),
            user = os.getenv("DB_USER", "postgres"),
            port = os.getenv("DB_PORT", "5432"),
            client_encoding = "WINDOWS1252"
        )

        # Prompt interactively when DB_PASSWORD is not provided or is empty.
        password_env = os.getenv("DB_PASSWORD", None)
        if password_env is None or password_env.strip() == "":
            password = getpass("Contraseña de PostgreSQL: ")
        else:
            password = password_env.strip()

        # Include password if provided (non-empty)
        if password:
            connection_kwargs["password"] = password

        return psycopg2.connect(**connection_kwargs)