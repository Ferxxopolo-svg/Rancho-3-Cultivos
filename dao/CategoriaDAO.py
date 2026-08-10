from models.Categoria import Categoria
from database.conexion import Conexion

class CategoriaDAO:

    # READ / OBTENER TODAS LAS CATEGORÍAS
    def obtener_todo(self):
        conexion = None
        try:
            conexion = Conexion.obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM vista_categorias")
            registros = cursor.fetchall()

            categorias = []
            for registro in registros:
                categoria = Categoria(registro[0], registro[1])
                categorias.append(categoria)
            return categorias
        except Exception as e:
            print(f"Error al obtener categorías: {e}")
            return []
        finally:
            if conexion:
                cursor.close()
                conexion.close()

    # CREATE / INSERTAR CATEGORÍA
    def insertar(self, categoria):
        conexion = None
        try:
            conexion = Conexion.obtener_conexion()
            cursor = conexion.cursor()
            sql = """
            INSERT INTO categoria (nombre)
            VALUES (%s)
            """
            cursor.execute(sql, (categoria.nombre,))
            conexion.commit()
        except Exception as e:
            print(f"Error al insertar categoría: {e}")
        finally:
            if conexion:
                cursor.close()
                conexion.close()

    # UPDATE / ACTUALIZAR CATEGORÍA
    def actualizar(self, categoria):
        conexion = None
        try:
            conexion = Conexion.obtener_conexion()
            cursor = conexion.cursor()
            sql = """
            UPDATE categoria
            SET nombre = %s
            WHERE id = %s
            """
            cursor.execute(sql, (categoria.nombre, categoria.id))
            conexion.commit()
        except Exception as e:
            print(f"Error al actualizar categoría: {e}")
        finally:
            if conexion:
                cursor.close()
                conexion.close()

    # DELETE / ELIMINAR CATEGORÍA
    def eliminar(self, id_categoria):
        conexion = None
        try:
            conexion = Conexion.obtener_conexion()
            cursor = conexion.cursor()
            sql = "DELETE FROM categoria WHERE id = %s"
            cursor.execute(sql, (id_categoria,))
            conexion.commit()
        except Exception as e:
            print(f"Error al eliminar categoría: {e}")
        finally:
            if conexion:
                cursor.close()
                conexion.close()



    def obtener_productos_por_categoria(self, id_categoria):
        conexion = None
        try:
            conexion = Conexion.obtener_conexion()
            cursor = conexion.cursor()
            sql = "SELECT id, nombre, precio, stock FROM producto WHERE id_categoria = %s"
            cursor.execute(sql, (id_categoria,))
            return cursor.fetchall()
        except Exception as e:
            print(f"Error al obtener productos de la categoría: {e}")
            return []
        finally:
            if conexion:
                cursor.close()
                conexion.close()

    def insertar_producto_en_categoria(self, nombre, precio, stock, id_categoria):
        conexion = None
        try:
            conexion = Conexion.obtener_conexion()
            cursor = conexion.cursor()
            sql = """
            INSERT INTO producto (nombre, precio, stock, id_categoria)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(sql, (nombre, precio, stock, id_categoria))
            conexion.commit()
        except Exception as e:
            print(f"Error al insertar producto en la categoría: {e}")
        finally:
            if conexion:
                cursor.close()
                conexion.close()