from database.conexion import Conexion
from models.Usuario import Usuario

class UsuarioDAO:

    # SELECT * FROM usuario
    def obtener_todo(self):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        try:
            cursor.execute("SELECT id_usuario, tipo_usuario, nombre, apellido_paterno, apellido_materno, numero_telefono, contrasena FROM usuario")
            registros = cursor.fetchall()

            usuarios = []
            for registro in registros:
                usuario = Usuario(registro[0], registro[1], registro[2], registro[3], registro[4], registro[5], registro[6])
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
            INSERT INTO usuario(id_usuario, tipo_usuario, nombre, apellido_paterno, apellido_materno, numero_telefono, contrasena)
            VALUES(%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (
                usuario.id_usuario,
                usuario.tipo_usuario, 
                usuario.nombre, 
                usuario.apellido_paterno,
                usuario.apellido_materno,
                usuario.telefono,
                usuario.contrasena
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
            SET tipo_usuario = %s, nombre = %s, apellido_paterno = %s, apellido_materno = %s, numero_telefono = %s, contrasena = %s
            WHERE id_usuario = %s
            """
            cursor.execute(sql, (
                usuario.tipo_usuario,
                usuario.nombre,
                usuario.apellido_paterno,
                usuario.apellido_materno,
                usuario.telefono,
                usuario.contrasena,
                usuario.id_usuario
            ))
            conexion.commit()
        finally:
            cursor.close()
            conexion.close()

    def autenticar(self, id_usuario, contrasena):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        try:
            # Intento directo (coincidencia exacta)
            cursor.execute(
                "SELECT id_usuario, tipo_usuario, nombre, apellido_paterno, apellido_materno, numero_telefono, contrasena FROM usuario WHERE id_usuario = %s AND contrasena = %s",
                (id_usuario, contrasena)
            )
            registro = cursor.fetchone()
            if registro:
                return Usuario(registro[0], registro[1], registro[2], registro[3], registro[4], registro[5], registro[6])

            # Si falla la coincidencia exacta, intentar leer la contraseña almacenada y comparar quitando espacios
            cursor.execute("SELECT contrasena FROM usuario WHERE id_usuario = %s", (id_usuario,))
            row = cursor.fetchone()
            if not row:
                return None
            almacenada = row[0] or ""
            if almacenada.strip() == (contrasena or "").strip():
                # Obtener registro completo y devolver Usuario
                cursor.execute(
                    "SELECT id_usuario, tipo_usuario, nombre, apellido_paterno, apellido_materno, numero_telefono, contrasena FROM usuario WHERE id_usuario = %s",
                    (id_usuario,)
                )
                registro = cursor.fetchone()
                if registro:
                    return Usuario(registro[0], registro[1], registro[2], registro[3], registro[4], registro[5], registro[6])

            return None
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