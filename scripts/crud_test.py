import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from dao.CategoriaDAO import CategoriaDAO
from dao.UsuarioDAO import UsuarioDAO
from dao.ClienteDAO import ClienteDAO
from dao.ProductoDAO import ProductoDAO
from dao.VentaDAO import VentaDAO
from models.Categoria import Categoria
from models.Usuario import Usuario
from models.Cliente import Cliente
from models.Producto import Producto
from models.Venta import Venta


def test_categoria():
    dao = CategoriaDAO()
    nid = dao.obtener_ultimo_id() + 1
    c = Categoria(nid, f'TestCat{nid}')
    dao.insertar(c)
    print('Inserted categoria', nid)
    cats = dao.obtener_todo()
    print('Count categorias:', len(cats))
    c.nombre = f'Updated{nid}'
    dao.actualizar(c)
    print('Updated categoria')
    dao.eliminar(nid)
    print('Deleted categoria')


def test_usuario():
    dao = UsuarioDAO()
    nid = dao.obtener_ultimo_id() + 1
    u = Usuario(nid, 'Tester', 'Test', 'Usr', 'One', '000', 'pw123')
    dao.insertar(u)
    print('Inserted usuario', nid)
    users = dao.obtener_todo()
    print('Count usuarios:', len(users))
    u.nombre = 'TestChanged'
    u.contrasena = 'pw456'
    dao.actualizar(u)
    print('Updated usuario')
    dao.eliminar(nid)
    print('Deleted usuario')


def test_cliente():
    dao = ClienteDAO()
    nid = dao.obtener_ultimo_id() + 1
    c = Cliente(nid, 'CName', 'AP', 'AM', '555', 'c@x.com', 1)
    dao.insertar(c)
    print('Inserted cliente', nid)
    cls = dao.obtener_todo()
    print('Count clientes:', len(cls))
    c.nombre = 'CChanged'
    dao.actualizar(c)
    print('Updated cliente')
    dao.eliminar(nid)
    print('Deleted cliente')


def test_producto():
    dao = ProductoDAO()
    nid = dao.obtener_ultimo_id() + 1
    p = Producto(nid, 'PTest', 9.9, 10, 1, 1)
    dao.insertar(p)
    print('Inserted producto', nid)
    pls = dao.obtener_todo()
    print('Count productos:', len(pls))
    p.nombre = 'PChanged'
    dao.actualizar(p)
    print('Updated producto')
    dao.eliminar(nid)
    print('Deleted producto')


def test_venta():
    dao = VentaDAO()
    nid = dao.obtener_ultimo_id() + 1
    v = Venta(nid, '2026-08-02', 1, 9.9, 1, 1, 1)
    dao.insertar(v)
    print('Inserted venta', nid)
    vs = dao.obtener_todo()
    print('Count ventas:', len(vs))
    v.total_venta = 19.8
    dao.actualizar(v)
    print('Updated venta')
    dao.eliminar(nid)
    print('Deleted venta')


def main():
    print('Starting CRUD tests (will require DB access)')
    test_categoria()
    test_usuario()
    test_cliente()
    test_producto()
    test_venta()
    print('CRUD tests completed')


if __name__ == '__main__':
    main()
