import flet as ft
import psycopg2

# 1. CLASE DE CONEXIÓN A LA BASE DE DATOS

class Conexion:
    @staticmethod
    def obtener_conexion():
        return psycopg2.connect(
            host="localhost",
            database="rancho_tres_cultivos",
            user="postgres",
            password="tu_password"
        )

# 2. MODELO: Categoria
class Categoria:
    def __init__(self, id_categoria=None, nombre=None, productos=None):
        self.id_categoria = id_categoria
        self.nombre = nombre
        self.productos = productos if productos is not None else []

    def mostrar_info(self):
        return f"Categoría {self.id_categoria}: {self.nombre}"

    def __repr__(self):
        return f"Categoria(id_categoria={self.id_categoria}, nombre='{self.nombre}')"


# 3. ACCESO A DATOS (DAO): CategoriaDAO

class CategoriaDAO:

    def obtener_todo(self):
        conexion = None
        try:
            conexion = Conexion.obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute("SELECT id, nombre FROM categoria ORDER BY id ASC;")
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

    def insertar(self, categoria):
        conexion = None
        try:
            conexion = Conexion.obtener_conexion()
            cursor = conexion.cursor()
            sql = "INSERT INTO categoria (nombre) VALUES (%s);"
            cursor.execute(sql, (categoria.nombre,))
            conexion.commit()
        except Exception as e:
            print(f"Error al insertar categoría: {e}")
        finally:
            if conexion:
                cursor.close()
                conexion.close()

    def actualizar(self, categoria):
        conexion = None
        try:
            conexion = Conexion.obtener_conexion()
            cursor = conexion.cursor()
            sql = "UPDATE categoria SET nombre = %s WHERE id = %s;"
            cursor.execute(sql, (categoria.nombre, categoria.id_categoria))
            conexion.commit()
        except Exception as e:
            print(f"Error al actualizar categoría: {e}")
        finally:
            if conexion:
                cursor.close()
                conexion.close()

    def eliminar(self, id_categoria):
        conexion = None
        try:
            conexion = Conexion.obtener_conexion()
            cursor = conexion.cursor()
            sql = "DELETE FROM categoria WHERE id = %s;"
            cursor.execute(sql, (id_categoria,))
            conexion.commit()
        except Exception as e:
            print(f"Error al eliminar categoría: {e}")
        finally:
            if conexion:
                cursor.close()
                conexion.close()

    def obtener_ultimo_id(self):
        conexion = None
        try:
            conexion = Conexion.obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute("SELECT MAX(id) FROM producto;")
            resultado = cursor.fetchone()
            return resultado[0] if resultado and resultado[0] is not None else 0
        except Exception as e:
            print(f"Error al obtener último ID: {e}")
            return 0
        finally:
            if conexion:
                cursor.close()
                conexion.close()

    def obtener_productos_por_categoria(self, id_categoria):
        return self.obtener_cultivos_por_categoria(id_categoria)

    def obtener_cultivos_por_categoria(self, id_categoria):
        conexion = None
        try:
            conexion = Conexion.obtener_conexion()
            cursor = conexion.cursor()
            sql = "SELECT id, nombre, precio, stock FROM producto WHERE id_categoria = %s ORDER BY id ASC;"
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
        return self.insertar_cultivo_en_categoria(nombre, precio, stock, id_categoria)

    def insertar_cultivo_en_categoria(self, nombre, precio, stock, id_categoria):
        conexion = None
        try:
            conexion = Conexion.obtener_conexion()
            cursor = conexion.cursor()
            sql = """
            INSERT INTO producto (nombre, precio, stock, id_categoria)
            VALUES (%s, %s, %s, %s);
            """
            cursor.execute(sql, (nombre, precio, stock, id_categoria))
            conexion.commit()
        except Exception as e:
            print(f"Error al insertar producto en la categoría: {e}")
        finally:
            if conexion:
                cursor.close()
                conexion.close()

# 4. INTERFAZ GRÁFICA (FLET)

def main(page: ft.Page):
    page.title = "Rancho 3 Cultivos"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 20

    categoria_dao = CategoriaDAO()
    PRIMARY = ft.Colors.GREEN_700

    contenido = ft.Container(expand=True)
    snack_bar = ft.SnackBar(ft.Text(""))
    page.snack_bar = snack_bar

    def set_message(texto, color=ft.Colors.GREEN_700):
        snack_bar.content = ft.Text(texto, color=ft.Colors.WHITE)
        snack_bar.bgcolor = color
        snack_bar.open = True
        page.update()

    def safe_float(val, default=0.0):
        try:
            return float(val)
        except (ValueError, TypeError):
            return default

    def safe_int(val, default=0):
        try:
            return int(val)
        except (ValueError, TypeError):
            return default

    def field(label, value="", read_only=False, width=300):
        return ft.TextField(label=label, value=str(value), read_only=read_only, width=width)

    def layout_base(titulo, vista_interior):
        return ft.Column([
            ft.Text(titulo, size=24, weight=ft.FontWeight.BOLD, color=PRIMARY),
            ft.Divider(),
            vista_interior
        ], expand=True)

    def table_view(titulo_tabla, descripcion, texto_boton, columnas, filas, on_click_agregar):
        return ft.Column([
            ft.Row([
                ft.Column([
                    ft.Text(titulo_tabla, size=18, weight=ft.FontWeight.BOLD),
                    ft.Text(descripcion, size=12, color=ft.Colors.GREY_700)
                ]),
                ft.ElevatedButton(texto_boton, icon=ft.Icons.ADD, on_click=on_click_agregar, color=ft.Colors.WHITE, bgcolor=PRIMARY)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.VerticalDivider(height=10),
            ft.Container(
                content=ft.DataTable(
                    columns=columnas,
                    rows=filas,
                    border=ft.border.all(1, ft.Colors.GREY_400),
                    vertical_lines=ft.border.border_side(1, ft.Colors.GREY_300),
                    horizontal_lines=ft.border.border_side(1, ft.Colors.GREY_300),
                ),
                expand=True,
            )
        ], expand=True)

    def show_form_page(titulo_form, campos, on_save, on_cancel):
        contenido.content = ft.Column([
            ft.Text(titulo_form, size=20, weight=ft.FontWeight.BOLD, color=PRIMARY),
            ft.Divider(),
            *campos,
            ft.Row([
                ft.ElevatedButton("Guardar", on_click=on_save, color=ft.Colors.WHITE, bgcolor=PRIMARY),
                ft.OutlinedButton("Cancelar", on_click=on_cancel)
            ], spacing=10)
        ], alignment=ft.MainAxisAlignment.START, spacing=15)
        page.update()

    def mostrar_categorias(e=None):
        try:
            categorias = categoria_dao.obtener_todo()
        except Exception as exc:
            set_message(f"No se pudieron cargar las categorías: {exc}", ft.Colors.RED_700)
            categorias = []

        rows = []
        for cat in categorias:
            productos = categoria_dao.obtener_productos_por_categoria(cat.id_categoria)

            def abrir_agregar_producto(id_cat=cat.id_categoria, nombre_cat=cat.nombre):
                nombre_field = field("Nombre del cultivo (ej. Durazno, Nopal)", width=320)
                precio_field = field("Precio ($)", width=320)
                stock_field = field("Stock (Cantidad)", width=320)

                def guardar(_):
                    if not nombre_field.value.strip():
                        set_message("Ingresa un nombre válido.", ft.Colors.RED_700)
                        return

                    categoria_dao.insertar_producto_en_categoria(
                        nombre_field.value.strip(),
                        safe_float(precio_field.value),
                        safe_int(stock_field.value),
                        id_cat
                    )
                    mostrar_categorias()
                    set_message("Cultivo registrado correctamente.", PRIMARY)

                show_form_page(
                    f"Agregar cultivo a {nombre_cat}", 
                    [nombre_field, precio_field, stock_field], 
                    guardar, 
                    on_cancel=lambda e: mostrar_categorias()
                )

            if productos:
                for prod in productos:
                    rows.append(
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text(str(prod[0]))),
                                ft.DataCell(ft.Text(prod[1])),
                                ft.DataCell(ft.Text(cat.nombre)),
                                ft.DataCell(ft.Text(f"${prod[2]:.2f}")),
                                ft.DataCell(ft.Text(str(prod[3]))),
                                ft.DataCell(
                                    ft.Row(
                                        spacing=0,
                                        controls=[
                                            ft.IconButton(
                                                ft.Icons.ADD, 
                                                tooltip=f"Agregar otro cultivo a {cat.nombre}", 
                                                on_click=lambda e, c_id=cat.id_categoria: abrir_agregar_producto(c_id)
                                            ),
                                        ],
                                    )
                                ),
                            ]
                        )
                    )
            else:
                rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(cat.id_categoria))),
                            ft.DataCell(ft.Text(f"Sin cultivos en {cat.nombre}")),
                            ft.DataCell(ft.Text(cat.nombre)),
                            ft.DataCell(ft.Text("-")),
                            ft.DataCell(ft.Text("-")),
                            ft.DataCell(
                                ft.IconButton(
                                    ft.Icons.ADD, 
                                    tooltip=f"Agregar cultivo a {cat.nombre}", 
                                    on_click=lambda e, c_id=cat.id_categoria: abrir_agregar_producto(c_id)
                                )
                            ),
                        ]
                    )
                )

        columnas = [
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Cultivo / Producto")),
            ft.DataColumn(ft.Text("Categoría")),
            ft.DataColumn(ft.Text("Precio")),
            ft.DataColumn(ft.Text("Stock")),
            ft.DataColumn(ft.Text("Acciones")),
        ]

        id_primera_cat = categorias[0].id_categoria if categorias else None

        contenido.content = layout_base(
            "Cultivos por Categoría", 
            table_view(
                "Cultivos", 
                "Gestión de cultivos y productos registrados.", 
                "Agregar cultivo", 
                columnas, 
                rows, 
                lambda e: abrir_agregar_producto(id_primera_cat) if id_primera_cat else set_message("Primero registra una categoría.", ft.Colors.RED_700)
            )
        )
        page.update()

    page.add(contenido)
    mostrar_categorias()

if __name__ == "__main__":
    ft.app(target=main)
       