from database.conexion import Conexion
from models.Categoria import Categoria

class CategoriaDAO:

    # SELECT * FROM categoria (o vista)
    def obtener_todo(self):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        try:
            cursor.execute("SELECT * FROM vista_categorias")
            registros = cursor.fetchall()

            categorias = []
            for registro in registros:
                categoria = Categoria(
                    id = registro[0],
                    nombre = registro[1]
                )
                categorias.append(categoria)
            return categorias
        finally:
            cursor.close()
            conexion.close()
    
    # INSERT
    def insertar(self, categoria):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        try:
            sql = """
            INSERT INTO categoria(id, nombre)
            VALUES(%s, %s)
            """
            cursor.execute(sql, (
                categoria.id,
                categoria.nombre
            ))
            conexion.commit()
        finally:
            cursor.close()
            conexion.close()

    # UPDATE
    def actualizar(self, categoria):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        try:
            sql = """
            UPDATE categoria
            SET nombre = %s
            WHERE id = %s
            """
            cursor.execute(sql, (
                categoria.nombre,
                categoria.id
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
            cursor.execute("DELETE FROM categoria WHERE id = %s", (id,))
            conexion.commit()
        finally:
            cursor.close()
            conexion.close()

    # OBTENER ULTIMO ID
    def obtener_ultimo_id(self):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        try:
            cursor.execute("SELECT MAX(id) FROM categoria")
            resultado = cursor.fetchone()

            if resultado[0] is None:
                return 0
            return resultado[0]
        finally:
            cursor.close()
            conexion.close()