import sys
from pathlib import Path

# Asegurar que el directorio raíz del proyecto esté en sys.path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from database.conexion import Conexion


def main():
    conn = None
    try:
        conn = Conexion.obtener_conexion()
        cur = conn.cursor()
        cur.execute("SELECT id_usuario, nombre, contrasena FROM usuario ORDER BY id_usuario")
        for row in cur.fetchall():
            print(f'id={row[0]}, nombre={row[1]}, contrasena={row[2]!r}')
    except Exception as e:
        print('Error:', e)
    finally:
        if conn:
            conn.close()


if __name__ == '__main__':
    main()
