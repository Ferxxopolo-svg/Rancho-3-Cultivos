import sys
from pathlib import Path

# Asegurar que el directorio raíz del proyecto esté en sys.path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from database.conexion import Conexion


def main():
    sql_path = Path(__file__).resolve().parents[1] / 'database' / 'migrate_auth.sql'
    sql_text = sql_path.read_text(encoding='utf-8')

    conn = None
    try:
        conn = Conexion.obtener_conexion()
        cur = conn.cursor()
        cur.execute(sql_text)
        conn.commit()
        print('Migration applied successfully')
    except Exception as e:
        print('Migration failed:', e)
    finally:
        if conn:
            conn.close()


if __name__ == '__main__':
    main()
