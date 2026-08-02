from database.conexion import Conexion
from models.Venta import Venta

class VentaDAO:

    # SELECT * FROM venta
    def obtener_todo(self):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        try:
            cursor.execute("SELECT id_venta, fecha_venta, cantidad_producto, total_venta, id_usuario, id_producto, id_cliente FROM venta")
            registros = cursor.fetchall()

            ventas = []
            for registro in registros:
                venta = Venta(
                    id = registro[0],
                    fecha_venta = registro[1],
                    cantidad_producto = registro[2],
                    total_venta = registro[3],
                    id_usuario = registro[4],
                    id_producto = registro[5],
                    id_cliente = registro[6]
                )
                ventas.append(venta)
            return ventas
        finally:
            cursor.close()
            conexion.close()
    
    # INSERT
    def insertar(self, venta):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        try:
            sql = """
            INSERT INTO venta(id_venta, fecha_venta, cantidad_producto, total_venta, id_usuario, id_producto, id_cliente)
            VALUES(%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (
                venta.id,
                venta.fecha_venta, 
                venta.cantidad_producto, 
                venta.total_venta,
                venta.id_usuario,
                venta.id_producto,
                venta.id_cliente
            ))
            conexion.commit()
        finally:
            cursor.close()
            conexion.close()

    # UPDATE
    def actualizar(self, venta):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        try:
            sql = """
            UPDATE venta
            SET fecha_venta = %s, cantidad_producto = %s, total_venta = %s, id_usuario = %s, id_producto = %s, id_cliente = %s
            WHERE id_venta = %s
            """
            cursor.execute(sql, (
                venta.fecha_venta,
                venta.cantidad_producto,
                venta.total_venta,
                venta.id_usuario,
                venta.id_producto,
                venta.id_cliente,
                venta.id
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
            cursor.execute("DELETE FROM venta WHERE id_venta = %s", (id,))
            conexion.commit()
        finally:
            cursor.close()
            conexion.close()

    # OBTENER ULTIMO ID
    def obtener_ultimo_id(self):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        try:
            cursor.execute("SELECT MAX(id_venta) FROM venta")
            resultado = cursor.fetchone()

            if resultado[0] is None:
                return 0
            return resultado[0]
        finally:
            cursor.close()
            conexion.close()