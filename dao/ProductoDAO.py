from database.conexion import Conexion
from models.Producto import Producto

class ProductoDAO:

    # SELECT * FROM producto
    def obtener_todo(self):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        try:
            cursor.execute("SELECT id_producto, nombre, precio, stock, id_categoria, id_usuario FROM producto")
            registros = cursor.fetchall()

            productos = []
            for registro in registros:
                producto = Producto(
                    id = registro[0],
                    nombre = registro[1],
                    precio = registro[2],
                    stock = registro[3],
                    id_categoria = registro[4],
                    id_usuario = registro[5]
                )
                productos.append(producto)
            return productos
        finally:
            cursor.close()
            conexion.close()
    
    # INSERT
    def insertar(self, producto):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        try:
            sql = """
            INSERT INTO producto(id_producto, nombre, precio, stock, id_categoria, id_usuario)
            VALUES(%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (
                producto.id,
                producto.nombre, 
                producto.precio, 
                producto.stock,
                producto.id_categoria,
                producto.id_usuario
            ))
            conexion.commit()
        finally:
            cursor.close()
            conexion.close()

    # UPDATE
    def actualizar(self, producto):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        try:
            sql = """
            UPDATE producto
            SET nombre = %s, precio = %s, stock = %s, id_categoria = %s, id_usuario = %s
            WHERE id_producto = %s
            """
            cursor.execute(sql, (
                producto.nombre,
                producto.precio,
                producto.stock,
                producto.id_categoria,
                producto.id_usuario,
                producto.id
            ))
            conexion.commit()
        finally:
            cursor.close()
            conexion.close()

    # DELETE
    def eliminar(self, id):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        try:
            cursor.execute("DELETE FROM producto WHERE id_producto = %s", (id,))
            conexion.commit()
        finally:
            cursor.close()
            conexion.close()

    # OBTENER ULTIMO ID
    def obtener_ultimo_id(self):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        try:
            cursor.execute("SELECT MAX(id_producto) FROM producto")
            resultado = cursor.fetchone()

            if resultado[0] is None:
                return 0
            return resultado[0]
        finally:
            cursor.close()
            conexion.close()