import flet as ft

from ui.main_window import main_window
from dao.UsuarioDAO import UsuarioDAO
from models.Usuario import Usuario
from dao.ClienteDAO import ClienteDAO
from models.Cliente import Cliente
from dao.ProductoDAO import ProductoDAO
from models.Producto import Producto
from dao.VentaDAO import VentaDAO
from models.Venta import Venta
from dao.CategoriaDAO import CategoriaDAO
from models.Categoria import Categoria

# ============================
# USUARIOS
# ============================
def ver_usuarios(usuario_dao):
    usuarios = UsuarioDAO.obtener_usuarios()
    print("Usuarios registrados")
    if len(usuarios) == 0:
        print("No hay usuarios")
    else:
        for u in usuarios:
            print(f"{u.id_usuario} - {u.nombre} {u.apellido_paterno} {u.apellido_materno} - {u.tipo_usuario} - {u.telefono}")

def insertar_usuario(usuario_dao):
    nombre = input("Nombre: ")
    apellido_paterno = input("Apellido paterno: ")
    apellido_materno = input("Apellido materno: ")
    tipo_usuario = input("Tipo de usuario: ")
    telefono = input("Teléfono: ")
    nuevo = Usuario(None, tipo_usuario, nombre, apellido_paterno, apellido_materno, telefono)
    usuario_dao.insertar(nuevo)

def menu_usuarios():
    usuario_dao = UsuarioDAO()
    print("1. Ver usuarios")
    print("2. Insertar usuario")
    opcion = int(input("Opción (1-2): "))
    match opcion:
        case 1: ver_usuarios(UsuarioDAO)
        case 2: insertar_usuario(UsuarioDAO)

# ============================
# CLIENTES
# ============================
def ver_clientes(cliente_dao):
    clientes = cliente_dao.obtener_clientes()
    print("Clientes registrados")
    for c in clientes:
        print(f"{c.id_cliente} - {c.nombre} {c.apellido_paterno} {c.apellido_materno} - {c.correo} - Usuario: {c.id_usuario}")

def insertar_cliente(cliente_dao):
    nombre = input("Nombre: ")
    apellido_paterno = input("Apellido paterno: ")
    apellido_materno = input("Apellido materno: ")
    telefono = input("Teléfono: ")
    correo = input("Correo: ")
    id_usuario = int(input("Id del usuario que gestiona: "))
    nuevo = Cliente(None, nombre, apellido_paterno, apellido_materno, telefono, correo, id_usuario)
    cliente_dao.insertar(nuevo)

def menu_clientes():
    cliente_dao = ClienteDAO()
    print("1. Ver clientes")
    print("2. Insertar cliente")
    opcion = int(input("Opción (1-2): "))
    match opcion:
        case 1: ver_clientes(cliente_dao)
        case 2: insertar_cliente(cliente_dao)

# ============================
# PRODUCTOS
# ============================
def ver_productos(producto_dao):
    productos = producto_dao.obtener_productos()
    print("Productos registrados")
    for p in productos:
        print(f"{p.id_producto} - {p.nombre} - ${p.precio} - Stock: {p.stock} - Categoria: {p.id_categoria} - Usuario: {p.id_usuario}")

def insertar_producto(producto_dao):
    nombre = input("Nombre: ")
    precio = float(input("Precio: "))
    stock = int(input("Stock: "))
    id_categoria = int(input("Id de categoría: "))
    id_usuario = int(input("Id del usuario que gestiona: "))
    nuevo = Producto(None, nombre, precio, stock, id_categoria, id_usuario)
    producto_dao.insertar(nuevo)

def menu_productos():
    producto_dao = ProductoDAO()
    print("1. Ver productos")
    print("2. Insertar producto")
    opcion = int(input("Opción (1-2): "))
    match opcion:
        case 1: ver_productos(producto_dao)
        case 2: insertar_producto(producto_dao)

# ============================
# VENTAS
# ============================
def ver_ventas(venta_dao):
    ventas = venta_dao.obtener_ventas()
    print("Ventas registradas")
    for v in ventas:
        print(f"{v.id_venta} - Fecha: {v.fecha_venta} - Cliente: {v.id_cliente} - Producto: {v.id_producto} - Usuario: {v.id_usuario} - Total: {v.total_venta}")

def insertar_venta(venta_dao):
    fecha = input("Fecha de venta (YYYY-MM-DD): ")
    cantidad = int(input("Cantidad de producto: "))
    total = float(input("Total de la venta: "))
    id_usuario = int(input("Id del usuario: "))
    id_producto = int(input("Id del producto: "))
    id_cliente = int(input("Id del cliente: "))
    nueva = Venta(None, fecha, cantidad, total, id_usuario, id_producto, id_cliente)
    venta_dao.insertar(nueva)

def menu_ventas():
    venta_dao = VentaDAO()
    print("1. Ver ventas")
    print("2. Insertar venta")
    opcion = int(input("Opción (1-2): "))
    match opcion:
        case 1: ver_ventas(venta_dao)
        case 2: insertar_venta(venta_dao)

# ============================
# CATEGORÍAS
# ============================
def ver_categorias(categoria_dao):
    categorias = categoria_dao.obtener_categorias()
    print("Categorías registradas")
    for c in categorias:
        print(f"{c.id_categoria} - {c.nombre}")

def insertar_categoria(categoria_dao):
    nombre = input("Nombre de la categoría: ")
    nueva = Categoria(None, nombre)
    categoria_dao.insertar(nueva)

def menu_categorias():
    categoria_dao = CategoriaDAO()
    print("1. Ver categorías")
    print("2. Insertar categoría")
    opcion = int(input("Opción (1-2): "))
    match opcion:
        case 1: ver_categorias(categoria_dao)
        case 2: insertar_categoria(categoria_dao)

# ============================
# MENÚ PRINCIPAL
# ============================
def main():
    print("=== Rancho 3 Cultivos ===")
    print("1. Gestión de Usuarios")
    print("2. Gestión de Clientes")
    print("3. Gestión de Productos")
    print("4. Gestión de Ventas")
    print("5. Gestión de Categorías")

    opcion = int(input("Escribe tu opción: "))
    match opcion:
        case 1: menu_usuarios()
        case 2: menu_clientes()
        case 3: menu_productos()
        case 4: menu_ventas()
        case 5: menu_categorias()

if __name__ == "__main__":
    main()