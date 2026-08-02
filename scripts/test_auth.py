import sys
from pathlib import Path

# Asegurar que el directorio raíz del proyecto esté en sys.path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from dao.UsuarioDAO import UsuarioDAO


def main():
    dao = UsuarioDAO()
    usuario = dao.autenticar(1, 'admin123')
    if usuario:
        print('AUTH_OK')
        print(f'id={usuario.id_usuario}, nombre={usuario.nombre}, tipo={usuario.tipo_usuario}')
    else:
        print('AUTH_FAILED')


if __name__ == '__main__':
    main()
