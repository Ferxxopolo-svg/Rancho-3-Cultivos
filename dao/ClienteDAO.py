from database.conexion import Conexion
from models.Cliente import Cliente

class ClienteDAO:

    # SELECT * FROM cliente
    def obtener_todo(self):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        try:
            cursor.execute("SELECT id_cliente, nombre, apellido_paterno, apellido_materno, numero_telefono, correo_electronico, id_usuario FROM cliente")
            registros = cursor.fetchall()

            clientes = []
            for registro in registros:
                cliente = Cliente(registro[0], registro[1], registro[2], registro[3], registro[4], registro[5], registro[6])
                clientes.append(cliente)
            return clientes
        finally:
            cursor.close()
            conexion.close()
    
    # INSERT
    def insertar(self, cliente):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        try:
            sql = """
            INSERT INTO cliente(id_cliente, nombre, apellido_paterno, apellido_materno, numero_telefono, correo_electronico, id_usuario)
            VALUES(%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (
                cliente.id_cliente,
                cliente.nombre, 
                cliente.apellido_paterno, 
                cliente.apellido_materno,
                cliente.telefono,
                cliente.correo,
                cliente.id_usuario
            ))
            conexion.commit()
        finally:
            cursor.close()
            conexion.close()

    # UPDATE
    def actualizar(self, cliente):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        try:
            sql = """
            UPDATE cliente
            SET nombre = %s, apellido_paterno = %s, apellido_materno = %s, numero_telefono = %s, correo_electronico = %s, id_usuario = %s
            WHERE id_cliente = %s
            """
            cursor.execute(sql, (
                cliente.nombre,
                cliente.apellido_paterno,
                cliente.apellido_materno,
                cliente.telefono,
                cliente.correo,
                cliente.id_usuario,
                cliente.id_cliente
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
            cursor.execute("DELETE FROM cliente WHERE id_cliente = %s", (id,))
            conexion.commit()
        finally:
            cursor.close()
            conexion.close()

    # OBTENER ULTIMO ID
    def obtener_ultimo_id(self):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        try:
            cursor.execute("SELECT MAX(id_cliente) FROM cliente")
            resultado = cursor.fetchone()

            if resultado[0] is None:
                return 0
            return resultado[0]
        finally:
            cursor.close()
            conexion.close()