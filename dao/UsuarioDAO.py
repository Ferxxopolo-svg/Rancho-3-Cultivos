from database.conexion import Conexion
from models.Usuario import Usuario

class UsuarioDAO:

    # SELECT * FROM usuario
    def obtener_todo(self):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        try:
            cursor.execute("SELECT id_usuario, tipo_usuario, nombre, apellido_paterno, apellido_materno, numero_telefono FROM usuario")
            registros = cursor.fetchall()

            usuarios = []
            for registro in registros:
                usuario = Usuario(
                    id = registro[0],
                    tipo_usuario = registro[1],
                    nombre = registro[2],
                    apellido_paterno = registro[3],
                    apellido_materno = registro[4],
                    numero_telefono = registro[5]
                )
                usuarios.append(usuario)
            return usuarios
        finally:
            cursor.close()
            conexion.close()
    
    # INSERT
    def insertar(self, usuario):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        try:
            sql = """
            INSERT INTO usuario(id_usuario, tipo_usuario, nombre, apellido_paterno, apellido_materno, numero_telefono)
            VALUES(%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (
                usuario.id,
                usuario.tipo_usuario, 
                usuario.nombre, 
                usuario.apellido_paterno,
                usuario.apellido_materno,
                usuario.numero_telefono
            ))
            conexion.commit()
        finally:
            cursor.close()
            conexion.close()

    # UPDATE
    def actualizar(self, usuario):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        try:
            sql = """
            UPDATE usuario
            SET tipo_usuario = %s, nombre = %s, apellido_paterno = %s, apellido_materno = %s, numero_telefono = %s
            WHERE id_usuario = %s
            """
            cursor.execute(sql, (
                usuario.tipo_usuario,
                usuario.nombre,
                usuario.apellido_paterno,
                usuario.apellido_materno,
                usuario.numero_telefono,
                usuario.id
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
            cursor.execute("DELETE FROM usuario WHERE id_usuario = %s", (id,))
            conexion.commit()
        finally:
            cursor.close()
            conexion.close()

    # OBTENER ULTIMO ID
    def obtener_ultimo_id(self):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        try:
            cursor.execute("SELECT MAX(id_usuario) FROM usuario")
            resultado = cursor.fetchone()

            if resultado[0] is None:
                return 0
            return resultado[0]
        finally:
            cursor.close()
            conexion.close()