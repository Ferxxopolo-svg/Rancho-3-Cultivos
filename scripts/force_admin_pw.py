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
        cur.execute("UPDATE usuario SET contrasena = %s WHERE id_usuario = %s", ('admin123', 1))
        conn.commit()
        print('Contraseña del usuario 1 establecida a: admin123')
        cur.execute("SELECT id_usuario, nombre, contrasena FROM usuario WHERE id_usuario = %s", (1,))
        row = cur.fetchone()
        if row:
            print(f'id={row[0]}, nombre={row[1]}, contrasena={row[2]!r}')
    except Exception as e:
        print('Error al forzar contraseña:', e)
    finally:
        if conn:
            conn.close()


if __name__ == '__main__':
    main()
