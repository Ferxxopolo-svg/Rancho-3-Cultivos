import flet as ft

from dao.CategoriaDAO import CategoriaDAO
from dao.ClienteDAO import ClienteDAO
from dao.ProductoDAO import ProductoDAO
from dao.UsuarioDAO import UsuarioDAO
from dao.VentaDAO import VentaDAO
from models.Categoria import Categoria
from models.Cliente import Cliente
from models.Producto import Producto
from models.Usuario import Usuario
from models.Venta import Venta


PRIMARY = "#A88156"
SECONDARY = "#5E462D"
LIGHT_TONE = "#E5D6C5"
BROWN_DARK = SECONDARY
GRAY = ft.Colors.GREY_300
TEXT_DARK = ft.Colors.BLACK87
TEXT_LIGHT = ft.Colors.WHITE
LOGIN_LOGO = "logo_rancho.png"


def main_window(page: ft.Page):
    page.title = "Rancho Tres Cultivos"
    page.window_width = 1100
    page.window_height = 700
    page.padding = 0
    page.bgcolor = "#F7F2EC"
    page.theme_mode = ft.ThemeMode.LIGHT

    categoria_dao = CategoriaDAO()
    cliente_dao = ClienteDAO()
    producto_dao = ProductoDAO()
    usuario_dao = UsuarioDAO()
    venta_dao = VentaDAO()

    contenido = ft.Container(expand=True, padding=20)
    mensaje = ft.Text("", size=12, color=ft.Colors.RED_700)
    usuario_actual = {"value": None}

    def set_message(texto: str = "", color=ft.Colors.RED_700):
        mensaje.value = texto
        mensaje.color = color
        # also show a SnackBar for better visibility
        if texto:
            sb = ft.SnackBar(ft.Text(texto, color=color))
            page.snack_bar = sb
            sb.open = True
        page.update()

    def click_and_call(fn, name: str = None):
        def handler(e=None):
            try:
                # clear previous message
                set_message("")
                if fn is None:
                    return
                # call the actual handler
                print(f"HANDLER CALL -> {name or fn.__name__}")
                result = fn(e)
                # Ensure UI refresh after handler runs
                try:
                    page.update()
                except Exception:
                    pass
                return result
            except Exception as exc:
                print(f"HANDLER ERROR -> {name or fn.__name__}: {exc}")
                set_message(f"Error en acción{(' ' + name) if name else ''}: {exc}")
        return handler

    def open_dialog(dialog: ft.AlertDialog):
        try:
            print(f"OPEN_DIALOG -> {getattr(dialog, 'title', None)}")
        except Exception:
            pass
        page.dialog = dialog
        dialog.open = True
        # show a small message confirming dialog open
        set_message("Diálogo abierto", PRIMARY)
        page.update()

    def close_dialog(dialog: ft.AlertDialog):
        try:
            print(f"CLOSE_DIALOG -> {getattr(dialog, 'title', None)}")
        except Exception:
            pass
        dialog.open = False
        set_message("")
        page.update()

    def safe_int(value: str, default: int | None = None):
        value = value.strip()
        if value == "":
            return default
        return int(value)

    def safe_float(value: str, default: float | None = None):
        value = value.strip()
        if value == "":
            return default
        return float(value)

    def cerrar_sesion(e=None):
        usuario_actual["value"] = None
        mostrar_login()

    def mostrar_login(e=None):
        login_id = field("ID de usuario", keyboard_type = ft.KeyboardType.NUMBER, width = 320)
        login_password = field("Contraseña", password = True, width = 320)

        def autenticar(_):
            try:
                usuario = usuario_dao.autenticar(safe_int(login_id.value), login_password.value)
                if not usuario:
                    set_message("Credenciales inválidas.", ft.Colors.RED_700)
                    return
                usuario_actual["value"] = usuario
                set_message(f"Bienvenido, {usuario.nombre}.", PRIMARY)
                mostrar_inicio()
            except Exception as exc:
                set_message(f"No se pudo autenticar: {exc}")

        contenido.content = ft.Container(
            expand = True,
            alignment = ft.Alignment.CENTER,
            content = ft.Column(
                alignment = ft.MainAxisAlignment.CENTER,
                horizontal_alignment = ft.CrossAxisAlignment.CENTER,
                spacing = 18,
                controls = [
                    ft.Container(
                        width = 420,
                        padding = 24,
                        border_radius = 20,
                        bgcolor = ft.Colors.WHITE,
                        content = ft.Column(
                            alignment = ft.MainAxisAlignment.CENTER,
                            horizontal_alignment = ft.CrossAxisAlignment.CENTER,
                            controls = [
                                ft.Text("Rancho Tres Cultivos", size = 20, weight = ft.FontWeight.BOLD, text_align = ft.TextAlign.CENTER),
                                ft.Container(height = 10),
                                ft.Image(
                                    src = LOGIN_LOGO,
                                    width = 150,
                                    height = 150,
                                ),
                                ft.Container(height = 6),
                                ft.Text("Iniciar sesión", size = 18, weight = ft.FontWeight.BOLD),
                                ft.Container(height = 10),
                                login_id,
                                login_password,
                                ft.ElevatedButton("Entrar", bgcolor = SECONDARY, color = TEXT_LIGHT, width = 160, on_click = click_and_call(autenticar, 'autenticar')),
                            ],
                        ),
                    ),
                    mensaje,
                ],
            ),
        )
        page.update()

    def top_bar(title: str):
        header_controls = [
            ft.IconButton(
                icon = ft.Icons.HOME,
                icon_color = SECONDARY,
                tooltip = "Inicio",
                on_click = click_and_call(lambda e: mostrar_inicio(), 'mostrar_inicio')
            ),
            ft.Text(title, weight = ft.FontWeight.BOLD, size = 16, color = TEXT_DARK),
            ft.Container(expand = True),
        ]

        if usuario_actual["value"] is not None:
            header_controls.extend([
                ft.Text(f"{usuario_actual['value'].nombre}", size = 12, color = TEXT_DARK),
                ft.IconButton(
                    icon = ft.Icons.LOGOUT,
                    icon_color = SECONDARY,
                    tooltip = "Cerrar sesión",
                    on_click = click_and_call(cerrar_sesion, 'cerrar_sesion')
                ),
            ])

        return ft.Container(
            bgcolor = PRIMARY,
            padding = 10,
            content = ft.Row(
                controls = header_controls,
                alignment = ft.MainAxisAlignment.START
            )
        )

    def footer():
        return ft.Container(
            bgcolor = LIGHT_TONE,
            padding = 8,
            alignment = ft.Alignment.CENTER,
            content = ft.Text("@Copyright", size = 12, weight = ft.FontWeight.BOLD, color = ft.Colors.BLACK54)
        )

    def layout_base(title: str, body):
        return ft.Column(
            controls = [
                top_bar(title),
                ft.Container(expand = True, padding = 20, content = body),
                footer()
            ],
            expand = True,
            spacing = 0
        )

    def table_view(title: str, subtitle: str, add_label: str, columns, rows, on_add):
        return ft.Column(
            expand = True,
            spacing = 16,
            controls = [
                ft.Row(
                    alignment = ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls = [
                        ft.Column(
                            spacing = 2,
                            controls = [
                                ft.Text(title, size = 24, weight = ft.FontWeight.BOLD, color = TEXT_DARK),
                                ft.Text(subtitle, size = 12, color = ft.Colors.BLACK54),
                            ],
                        ),
                                        ft.ElevatedButton(
                            add_label,
                            icon = ft.Icons.ADD,
                            bgcolor = SECONDARY,
                            color = TEXT_LIGHT,
                            on_click = click_and_call(on_add, f'add_{add_label}'),
                        ),
                    ],
                ),
                mensaje,
                ft.Container(
                    expand = True,
                    border_radius = 10,
                    padding = 10,
                    content = ft.Column(
                        expand = True,
                        scroll = ft.ScrollMode.AUTO,
                        controls = [
                            ft.DataTable(
                                expand = True,
                                column_spacing = 20,
                                heading_row_color = LIGHT_TONE,
                                columns = columns,
                                rows = rows,
                            )
                        ],
                    ),
                ),
            ],
        )

    def field(label, value = "", password = False, read_only = False, keyboard_type = None, multiline = False, width = 380):
        return ft.TextField(
            label = label,
            value = value,
            password = password,
            read_only = read_only,
            keyboard_type = keyboard_type,
            multiline = multiline,
            width = width,
        )

    def confirm_delete(title: str, on_accept):
        dlg = ft.AlertDialog(
            modal = True,
            title = ft.Text("Confirmar eliminación"),
            content = ft.Text(title),
            actions = [
                ft.TextButton("Cancelar", on_click = lambda e: close_dialog(dlg)),
                ft.ElevatedButton("Eliminar", bgcolor = ft.Colors.RED_600, color = TEXT_LIGHT, on_click = on_accept),
            ],
        )
        return dlg

    def entity_dialog(title: str, fields, on_save):
        dlg = ft.AlertDialog(
            modal = True,
            title = ft.Text(title),
            content = ft.Container(
                width = 460,
                content = ft.Column(
                    tight = True,
                    scroll = ft.ScrollMode.AUTO,
                    spacing = 12,
                    controls = fields,
                ),
            ),
            actions = [
                ft.TextButton("Cancelar", on_click = lambda e: close_dialog(dlg)),
                ft.ElevatedButton("Guardar", bgcolor = SECONDARY, color = TEXT_LIGHT, on_click = on_save),
            ],
            actions_alignment = ft.MainAxisAlignment.END,
        )
        return dlg

    def show_form_page(title: str, fields, on_save, on_cancel=None):
        # Build inline form view replacing main content so it's always visible
        def wrap_save(e=None):
            try:
                set_message("")
                on_save(e)
            except Exception as exc:
                set_message(f"Error al guardar: {exc}")

        def wrap_cancel(e=None):
            if on_cancel:
                try:
                    on_cancel(e)
                except Exception as exc:
                    set_message(f"Error: {exc}")
            mostrar_inicio()

        body = ft.Column(
            controls = [
                ft.Text(title, size=20, weight=ft.FontWeight.BOLD),
                ft.Container(height=12),
            ] + fields + [
                ft.Row(spacing=12, alignment=ft.MainAxisAlignment.END, controls=[
                    ft.TextButton("Cancelar", on_click=wrap_cancel),
                    ft.ElevatedButton("Guardar", bgcolor=SECONDARY, color=TEXT_LIGHT, on_click=wrap_save),
                ])
            ],
            scroll = ft.ScrollMode.AUTO,
        )

        contenido.content = layout_base(title, ft.Container(padding=10, content=body, expand=True))
        page.update()

    def show_confirm_page(message: str, on_accept, on_cancel=None):
        def aceptar(e=None):
            try:
                on_accept(e)
            except Exception as exc:
                set_message(f"Error: {exc}")
            mostrar_inicio()

        def cancelar(e=None):
            if on_cancel:
                try:
                    on_cancel(e)
                except Exception as exc:
                    set_message(f"Error: {exc}")
            mostrar_inicio()

        body = ft.Column(
            controls=[
                ft.Text("Confirmar", size=18, weight=ft.FontWeight.BOLD),
                ft.Container(height=8),
                ft.Text(message),
                ft.Container(height=12),
                ft.Row(spacing=12, alignment=ft.MainAxisAlignment.END, controls=[
                    ft.TextButton("Cancelar", on_click=cancelar),
                    ft.ElevatedButton("Eliminar", bgcolor=ft.Colors.RED_600, color=TEXT_LIGHT, on_click=aceptar),
                ])
            ]
        )

        contenido.content = layout_base("Confirmar", ft.Container(padding=10, content=body, expand=True))
        page.update()

    def refresh(view_builder):
        contenido.content = view_builder()
        page.update()

    def home_card(texto, icono, callback):
        return ft.Container(
            width = 230,
            height = 130,
            border_radius = 16,
            bgcolor = ft.Colors.WHITE,
            ink = True,
            on_click = callback,
            alignment = ft.Alignment.CENTER,
            content = ft.Column(
                alignment = ft.MainAxisAlignment.CENTER,
                horizontal_alignment = ft.CrossAxisAlignment.CENTER,
                spacing = 8,
                controls = [
                    ft.Icon(icono, size = 38, color = SECONDARY),
                    ft.Text(texto, size = 16, weight = ft.FontWeight.BOLD, color = TEXT_DARK),
                ],
            ),
        )

    def mostrar_inicio(e=None):
        if usuario_actual["value"] is None:
            mostrar_login()
            return

        contenido.content = layout_base(
            "Inicio",
            ft.Container(
                alignment = ft.Alignment.CENTER,
                expand = True,
                content = ft.Column(
                    alignment = ft.MainAxisAlignment.CENTER,
                    horizontal_alignment = ft.CrossAxisAlignment.CENTER,
                    spacing = 24,
                    controls = [
                        ft.Container(
                            width = 180,
                            height = 180,
                            border_radius = 90,
                            alignment = ft.Alignment.CENTER,
                            content = ft.Text(
                                "Rancho\nTres Cultivos",
                                text_align = ft.TextAlign.CENTER,
                                size = 20,
                                weight = ft.FontWeight.BOLD,
                                color = BROWN_DARK,
                            ),
                        ),
                        ft.Text("Sistema de gestión", size = 18, weight = ft.FontWeight.BOLD, color = TEXT_DARK),
                        ft.Container(
                            width = 760,
                            content = ft.Column(
                                horizontal_alignment = ft.CrossAxisAlignment.CENTER,
                                spacing = 20,
                                controls = [
                                    ft.Row(
                                        alignment = ft.MainAxisAlignment.CENTER,
                                        spacing = 20,
                                        controls = [
                                            home_card("Categorías", ft.Icons.CATEGORY, lambda e: mostrar_categorias()),
                                            home_card("Clientes", ft.Icons.PEOPLE, lambda e: mostrar_clientes()),
                                            home_card("Ventas", ft.Icons.POINT_OF_SALE, lambda e: mostrar_ventas()),
                                        ],
                                    ),
                                    ft.Row(
                                        alignment = ft.MainAxisAlignment.CENTER,
                                        spacing = 20,
                                        controls = [
                                            home_card("Usuarios", ft.Icons.PERSON, lambda e: mostrar_usuarios()),
                                            home_card("Productos", ft.Icons.LOCAL_GROCERY_STORE, lambda e: mostrar_productos()),
                                        ],
                                    ),
                                ],
                            ),
                        ),
                    ],
                ),
            ),
        )
        page.update()

    def mostrar_categorias(e=None):
        try:
            categorias = categoria_dao.obtener_todo()
        except Exception as exc:
            set_message(f"No se pudieron cargar las categorías: {exc}")
            categorias = []

        def abrir_nuevo(_=None):
            siguiente_id = categoria_dao.obtener_ultimo_id() + 1
            id_field = field("ID", str(siguiente_id), read_only = True, width = 200)
            nombre_field = field("Nombre", width = 320)

            def guardar(_):
                try:
                    categoria = Categoria(safe_int(id_field.value), nombre_field.value.strip())
                    categoria_dao.insertar(categoria)
                    mostrar_categorias()
                    set_message("Categoría guardada correctamente.", PRIMARY)
                except Exception as exc:
                    set_message(f"Error al guardar categoría: {exc}")
            show_form_page("Agregar categoría", [id_field, nombre_field], guardar, on_cancel=lambda e: mostrar_categorias())

        def editar_categoria(categoria):
            id_field = field("ID", str(categoria.id_categoria), read_only = True, width = 200)
            nombre_field = field("Nombre", categoria.nombre, width = 320)

            def guardar(_):
                try:
                    categoria_mod = Categoria(safe_int(id_field.value), nombre_field.value.strip())
                    categoria_dao.actualizar(categoria_mod)
                    mostrar_categorias()
                    set_message("Categoría actualizada correctamente.", PRIMARY)
                except Exception as exc:
                    set_message(f"Error al actualizar categoría: {exc}")
            show_form_page("Editar categoría", [id_field, nombre_field], guardar, on_cancel=lambda e: mostrar_categorias())

        def eliminar_categoria(categoria):
            def aceptar(_=None):
                try:
                    categoria_dao.eliminar(categoria.id_categoria)
                    mostrar_categorias()
                    set_message("Categoría eliminada correctamente.", PRIMARY)
                except Exception as exc:
                    set_message(f"Error al eliminar categoría: {exc}")

            show_confirm_page(f"¿Eliminar la categoría {categoria.nombre}?", aceptar, on_cancel=lambda e: mostrar_categorias())

        rows = []
        for categoria in categorias:
            rows.append(
                ft.DataRow(
                    cells = [
                        ft.DataCell(ft.Text(str(categoria.id_categoria))),
                        ft.DataCell(ft.Text(categoria.nombre)),
                        ft.DataCell(
                            ft.Row(
                                spacing = 0,
                                controls = [
                                    ft.IconButton(ft.Icons.EDIT, tooltip = "Editar", on_click = click_and_call(lambda e, c=categoria: editar_categoria(c), 'editar_categoria')),
                                    ft.IconButton(ft.Icons.DELETE, tooltip = "Eliminar", icon_color = ft.Colors.RED_600, on_click = click_and_call(lambda e, c=categoria: eliminar_categoria(c), 'eliminar_categoria')),
                                ],
                            )
                        ),
                    ]
                )
            )

        columnas = [
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Nombre")),
            ft.DataColumn(ft.Text("Acciones")),
        ]

        refresh(lambda: layout_base("Categorías", table_view("Categorías", "Administración del catálogo de categorías.", "Agregar categoría", columnas, rows, abrir_nuevo)))

    def mostrar_usuarios(e=None):
        try:
            usuarios = usuario_dao.obtener_todo()
        except Exception as exc:
            set_message(f"No se pudieron cargar los usuarios: {exc}")
            usuarios = []

        def abrir_nuevo(_=None):
            siguiente_id = usuario_dao.obtener_ultimo_id() + 1
            id_field = field("ID", str(siguiente_id), read_only = True, width = 160)
            tipo_field = field("Tipo usuario", width = 320)
            nombre_field = field("Nombre", width = 320)
            ap_paterno_field = field("Apellido paterno", width = 320)
            ap_materno_field = field("Apellido materno", width = 320)
            telefono_field = field("Teléfono", width = 320)
            contrasena_field = field("Contraseña", password = True, width = 320)

            def guardar(_):
                try:
                    usuario = Usuario(
                        safe_int(id_field.value),
                        tipo_field.value.strip(),
                        nombre_field.value.strip(),
                        ap_paterno_field.value.strip(),
                        ap_materno_field.value.strip(),
                        telefono_field.value.strip(),
                        contrasena_field.value,
                    )
                    usuario_dao.insertar(usuario)
                    mostrar_usuarios()
                    set_message("Usuario guardado correctamente.", PRIMARY)
                except Exception as exc:
                    set_message(f"Error al guardar usuario: {exc}")
            show_form_page("Agregar usuario", [id_field, tipo_field, nombre_field, ap_paterno_field, ap_materno_field, telefono_field, contrasena_field], guardar, on_cancel=lambda e: mostrar_usuarios())

        def editar_usuario(usuario):
            id_field = field("ID", str(usuario.id_usuario), read_only = True, width = 160)
            tipo_field = field("Tipo usuario", usuario.tipo_usuario, width = 320)
            nombre_field = field("Nombre", usuario.nombre, width = 320)
            ap_paterno_field = field("Apellido paterno", usuario.apellido_paterno, width = 320)
            ap_materno_field = field("Apellido materno", usuario.apellido_materno, width = 320)
            telefono_field = field("Teléfono", usuario.telefono, width = 320)
            contrasena_field = field("Contraseña", usuario.contrasena, password = True, width = 320)

            def guardar(_):
                try:
                    usuario_mod = Usuario(
                        safe_int(id_field.value),
                        tipo_field.value.strip(),
                        nombre_field.value.strip(),
                        ap_paterno_field.value.strip(),
                        ap_materno_field.value.strip(),
                        telefono_field.value.strip(),
                        contrasena_field.value,
                    )
                    usuario_dao.actualizar(usuario_mod)
                    mostrar_usuarios()
                    set_message("Usuario actualizado correctamente.", PRIMARY)
                except Exception as exc:
                    set_message(f"Error al actualizar usuario: {exc}")
            show_form_page("Editar usuario", [id_field, tipo_field, nombre_field, ap_paterno_field, ap_materno_field, telefono_field, contrasena_field], guardar, on_cancel=lambda e: mostrar_usuarios())

        def eliminar_usuario(usuario):
            def aceptar(_=None):
                try:
                    usuario_dao.eliminar(usuario.id_usuario)
                    mostrar_usuarios()
                    set_message("Usuario eliminado correctamente.", PRIMARY)
                except Exception as exc:
                    set_message(f"Error al eliminar usuario: {exc}")

            show_confirm_page(f"¿Eliminar al usuario {usuario.nombre} {usuario.apellido_paterno}?", aceptar, on_cancel=lambda e: mostrar_usuarios())

        rows = []
        for usuario in usuarios:
            rows.append(
                ft.DataRow(
                    cells = [
                        ft.DataCell(ft.Text(str(usuario.id_usuario))),
                        ft.DataCell(ft.Text(usuario.tipo_usuario)),
                        ft.DataCell(ft.Text(usuario.nombre)),
                        ft.DataCell(ft.Text(usuario.apellido_paterno)),
                        ft.DataCell(ft.Text(usuario.apellido_materno)),
                        ft.DataCell(ft.Text(usuario.telefono)),
                        ft.DataCell(
                            ft.Row(
                                spacing = 0,
                                controls = [
                                    ft.IconButton(ft.Icons.EDIT, tooltip = "Editar", on_click = click_and_call(lambda e, u=usuario: editar_usuario(u), 'editar_usuario')),
                                    ft.IconButton(ft.Icons.DELETE, tooltip = "Eliminar", icon_color = ft.Colors.RED_600, on_click = click_and_call(lambda e, u=usuario: eliminar_usuario(u), 'eliminar_usuario')),
                                ],
                            )
                        ),
                    ]
                )
            )

        columnas = [
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Tipo")),
            ft.DataColumn(ft.Text("Nombre")),
            ft.DataColumn(ft.Text("Apellido paterno")),
            ft.DataColumn(ft.Text("Apellido materno")),
            ft.DataColumn(ft.Text("Teléfono")),
            ft.DataColumn(ft.Text("Acciones")),
        ]

        refresh(lambda: layout_base("Usuarios", table_view("Usuarios", "Gestión de usuarios del sistema.", "Agregar usuario", columnas, rows, abrir_nuevo)))

    def mostrar_clientes(e=None):
        try:
            clientes = cliente_dao.obtener_todo()
        except Exception as exc:
            set_message(f"No se pudieron cargar los clientes: {exc}")
            clientes = []

        def abrir_nuevo(_=None):
            siguiente_id = cliente_dao.obtener_ultimo_id() + 1
            id_field = field("ID", str(siguiente_id), read_only = True, width = 160)
            nombre_field = field("Nombre", width = 320)
            ap_paterno_field = field("Apellido paterno", width = 320)
            ap_materno_field = field("Apellido materno", width = 320)
            telefono_field = field("Teléfono", width = 320)
            correo_field = field("Correo electrónico", width = 320)
            usuario_field = field("ID de usuario", width = 320, keyboard_type = ft.KeyboardType.NUMBER)

            def guardar(_):
                try:
                    cliente = Cliente(
                        safe_int(id_field.value),
                        nombre_field.value.strip(),
                        ap_paterno_field.value.strip(),
                        ap_materno_field.value.strip(),
                        telefono_field.value.strip(),
                        correo_field.value.strip(),
                        safe_int(usuario_field.value),
                    )
                    cliente_dao.insertar(cliente)
                    mostrar_clientes()
                    set_message("Cliente guardado correctamente.", PRIMARY)
                except Exception as exc:
                    set_message(f"Error al guardar cliente: {exc}")
            show_form_page("Agregar cliente", [id_field, nombre_field, ap_paterno_field, ap_materno_field, telefono_field, correo_field, usuario_field], guardar, on_cancel=lambda e: mostrar_clientes())

        def editar_cliente(cliente):
            id_field = field("ID", str(cliente.id_cliente), read_only = True, width = 160)
            nombre_field = field("Nombre", cliente.nombre, width = 320)
            ap_paterno_field = field("Apellido paterno", cliente.apellido_paterno, width = 320)
            ap_materno_field = field("Apellido materno", cliente.apellido_materno, width = 320)
            telefono_field = field("Teléfono", cliente.telefono, width = 320)
            correo_field = field("Correo electrónico", cliente.correo, width = 320)
            usuario_field = field("ID de usuario", str(cliente.id_usuario), width = 320, keyboard_type = ft.KeyboardType.NUMBER)

            def guardar(_):
                try:
                    cliente_mod = Cliente(
                        safe_int(id_field.value),
                        nombre_field.value.strip(),
                        ap_paterno_field.value.strip(),
                        ap_materno_field.value.strip(),
                        telefono_field.value.strip(),
                        correo_field.value.strip(),
                        safe_int(usuario_field.value),
                    )
                    cliente_dao.actualizar(cliente_mod)
                    mostrar_clientes()
                    set_message("Cliente actualizado correctamente.", PRIMARY)
                except Exception as exc:
                    set_message(f"Error al actualizar cliente: {exc}")
            show_form_page("Editar cliente", [id_field, nombre_field, ap_paterno_field, ap_materno_field, telefono_field, correo_field, usuario_field], guardar, on_cancel=lambda e: mostrar_clientes())

        def eliminar_cliente(cliente):
            def aceptar(_=None):
                try:
                    cliente_dao.eliminar(cliente.id_cliente)
                    mostrar_clientes()
                    set_message("Cliente eliminado correctamente.", PRIMARY)
                except Exception as exc:
                    set_message(f"Error al eliminar cliente: {exc}")

            show_confirm_page(f"¿Eliminar al cliente {cliente.nombre} {cliente.apellido_paterno}?", aceptar, on_cancel=lambda e: mostrar_clientes())

        rows = []
        for cliente in clientes:
            rows.append(
                ft.DataRow(
                    cells = [
                        ft.DataCell(ft.Text(str(cliente.id_cliente))),
                        ft.DataCell(ft.Text(cliente.nombre)),
                        ft.DataCell(ft.Text(cliente.apellido_paterno)),
                        ft.DataCell(ft.Text(cliente.apellido_materno)),
                        ft.DataCell(ft.Text(cliente.telefono)),
                        ft.DataCell(ft.Text(cliente.correo)),
                        ft.DataCell(ft.Text(str(cliente.id_usuario))),
                        ft.DataCell(
                            ft.Row(
                                spacing = 0,
                                controls = [
                                    ft.IconButton(ft.Icons.EDIT, tooltip = "Editar", on_click = click_and_call(lambda e, c=cliente: editar_cliente(c), 'editar_cliente')),
                                    ft.IconButton(ft.Icons.DELETE, tooltip = "Eliminar", icon_color = ft.Colors.RED_600, on_click = click_and_call(lambda e, c=cliente: eliminar_cliente(c), 'eliminar_cliente')),
                                ],
                            )
                        ),
                    ]
                )
            )

        columnas = [
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Nombre")),
            ft.DataColumn(ft.Text("Apellido paterno")),
            ft.DataColumn(ft.Text("Apellido materno")),
            ft.DataColumn(ft.Text("Teléfono")),
            ft.DataColumn(ft.Text("Correo")),
            ft.DataColumn(ft.Text("Usuario")),
            ft.DataColumn(ft.Text("Acciones")),
        ]

        refresh(lambda: layout_base("Clientes", table_view("Clientes", "Gestión de clientes registrados.", "Agregar cliente", columnas, rows, abrir_nuevo)))

    def mostrar_productos(e=None):
        try:
            productos = producto_dao.obtener_todo()
        except Exception as exc:
            set_message(f"No se pudieron cargar los productos: {exc}")
            productos = []

        def abrir_nuevo(_=None):
            siguiente_id = producto_dao.obtener_ultimo_id() + 1
            id_field = field("ID", str(siguiente_id), read_only = True, width = 160)
            nombre_field = field("Nombre", width = 320)
            precio_field = field("Precio", width = 320, keyboard_type = ft.KeyboardType.NUMBER)
            stock_field = field("Stock", width = 320, keyboard_type = ft.KeyboardType.NUMBER)
            categoria_field = field("ID de categoría", width = 320, keyboard_type = ft.KeyboardType.NUMBER)
            usuario_field = field("ID de usuario", width = 320, keyboard_type = ft.KeyboardType.NUMBER)

            def guardar(_):
                try:
                    producto = Producto(
                        safe_int(id_field.value),
                        nombre_field.value.strip(),
                        safe_float(precio_field.value),
                        safe_int(stock_field.value),
                        safe_int(categoria_field.value),
                        safe_int(usuario_field.value),
                    )
                    producto_dao.insertar(producto)
                    mostrar_productos()
                    set_message("Producto guardado correctamente.", PRIMARY)
                except Exception as exc:
                    set_message(f"Error al guardar producto: {exc}")
            show_form_page("Agregar producto", [id_field, nombre_field, precio_field, stock_field, categoria_field, usuario_field], guardar, on_cancel=lambda e: mostrar_productos())

        def editar_producto(producto):
            id_field = field("ID", str(producto.id_producto), read_only = True, width = 160)
            nombre_field = field("Nombre", producto.nombre, width = 320)
            precio_field = field("Precio", str(producto.precio), width = 320, keyboard_type = ft.KeyboardType.NUMBER)
            stock_field = field("Stock", str(producto.stock), width = 320, keyboard_type = ft.KeyboardType.NUMBER)
            categoria_field = field("ID de categoría", str(producto.id_categoria), width = 320, keyboard_type = ft.KeyboardType.NUMBER)
            usuario_field = field("ID de usuario", str(producto.id_usuario), width = 320, keyboard_type = ft.KeyboardType.NUMBER)

            def guardar(_):
                try:
                    producto_mod = Producto(
                        safe_int(id_field.value),
                        nombre_field.value.strip(),
                        safe_float(precio_field.value),
                        safe_int(stock_field.value),
                        safe_int(categoria_field.value),
                        safe_int(usuario_field.value),
                    )
                    producto_dao.actualizar(producto_mod)
                    mostrar_productos()
                    set_message("Producto actualizado correctamente.", PRIMARY)
                except Exception as exc:
                    set_message(f"Error al actualizar producto: {exc}")

            show_form_page("Editar producto", [id_field, nombre_field, precio_field, stock_field, categoria_field, usuario_field], guardar, on_cancel=lambda e: mostrar_productos())

        def eliminar_producto(producto):
            def aceptar(_=None):
                try:
                    producto_dao.eliminar(producto.id_producto)
                    mostrar_productos()
                    set_message("Producto eliminado correctamente.", PRIMARY)
                except Exception as exc:
                    set_message(f"Error al eliminar producto: {exc}")

            show_confirm_page(f"¿Eliminar el producto {producto.nombre}?", aceptar, on_cancel=lambda e: mostrar_productos())

        rows = []
        for producto in productos:
            rows.append(
                ft.DataRow(
                    cells = [
                        ft.DataCell(ft.Text(str(producto.id_producto))),
                        ft.DataCell(ft.Text(producto.nombre)),
                        ft.DataCell(ft.Text(str(producto.precio))),
                        ft.DataCell(ft.Text(str(producto.stock))),
                        ft.DataCell(ft.Text(str(producto.id_categoria))),
                        ft.DataCell(ft.Text(str(producto.id_usuario))),
                        ft.DataCell(
                            ft.Row(
                                spacing = 0,
                                controls = [
                                    ft.IconButton(ft.Icons.EDIT, tooltip = "Editar", on_click = click_and_call(lambda e, p=producto: editar_producto(p), 'editar_producto')),
                                    ft.IconButton(ft.Icons.DELETE, tooltip = "Eliminar", icon_color = ft.Colors.RED_600, on_click = click_and_call(lambda e, p=producto: eliminar_producto(p), 'eliminar_producto')),
                                ],
                            )
                        ),
                    ]
                )
            )

        columnas = [
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Nombre")),
            ft.DataColumn(ft.Text("Precio")),
            ft.DataColumn(ft.Text("Stock")),
            ft.DataColumn(ft.Text("Categoría")),
            ft.DataColumn(ft.Text("Usuario")),
            ft.DataColumn(ft.Text("Acciones")),
        ]

        refresh(lambda: layout_base("Productos", table_view("Productos", "Gestión del inventario de productos.", "Agregar producto", columnas, rows, abrir_nuevo)))

    def mostrar_ventas(e=None):
        try:
            ventas = venta_dao.obtener_todo()
        except Exception as exc:
            set_message(f"No se pudieron cargar las ventas: {exc}")
            ventas = []

        def abrir_nuevo(_=None):
            siguiente_id = venta_dao.obtener_ultimo_id() + 1
            id_field = field("ID", str(siguiente_id), read_only = True, width = 160)
            fecha_field = field("Fecha (YYYY-MM-DD)", width = 320)
            cantidad_field = field("Cantidad", width = 320, keyboard_type = ft.KeyboardType.NUMBER)
            total_field = field("Total", width = 320, keyboard_type = ft.KeyboardType.NUMBER)
            usuario_field = field("ID de usuario", width = 320, keyboard_type = ft.KeyboardType.NUMBER)
            producto_field = field("ID de producto", width = 320, keyboard_type = ft.KeyboardType.NUMBER)
            cliente_field = field("ID de cliente", width = 320, keyboard_type = ft.KeyboardType.NUMBER)

            def guardar(_):
                try:
                    venta = Venta(
                        safe_int(id_field.value),
                        fecha_field.value.strip(),
                        safe_int(cantidad_field.value),
                        safe_float(total_field.value),
                        safe_int(usuario_field.value),
                        safe_int(producto_field.value),
                        safe_int(cliente_field.value),
                    )
                    venta_dao.insertar(venta)
                    mostrar_ventas()
                    set_message("Venta guardada correctamente.", PRIMARY)
                except Exception as exc:
                    set_message(f"Error al guardar venta: {exc}")
            show_form_page("Agregar venta", [id_field, fecha_field, cantidad_field, total_field, usuario_field, producto_field, cliente_field], guardar, on_cancel=lambda e: mostrar_ventas())

        def editar_venta(venta):
            id_field = field("ID", str(venta.id_venta), read_only = True, width = 160)
            fecha_field = field("Fecha (YYYY-MM-DD)", str(venta.fecha_venta), width = 320)
            cantidad_field = field("Cantidad", str(venta.cantidad_producto), width = 320, keyboard_type = ft.KeyboardType.NUMBER)
            total_field = field("Total", str(venta.total_venta), width = 320, keyboard_type = ft.KeyboardType.NUMBER)
            usuario_field = field("ID de usuario", str(venta.id_usuario), width = 320, keyboard_type = ft.KeyboardType.NUMBER)
            producto_field = field("ID de producto", str(venta.id_producto), width = 320, keyboard_type = ft.KeyboardType.NUMBER)
            cliente_field = field("ID de cliente", str(venta.id_cliente), width = 320, keyboard_type = ft.KeyboardType.NUMBER)

            def guardar(_):
                try:
                    venta_mod = Venta(
                        safe_int(id_field.value),
                        fecha_field.value.strip(),
                        safe_int(cantidad_field.value),
                        safe_float(total_field.value),
                        safe_int(usuario_field.value),
                        safe_int(producto_field.value),
                        safe_int(cliente_field.value),
                    )
                    venta_dao.actualizar(venta_mod)
                    mostrar_ventas()
                    set_message("Venta actualizada correctamente.", PRIMARY)
                except Exception as exc:
                    set_message(f"Error al actualizar venta: {exc}")

            show_form_page("Editar venta", [id_field, fecha_field, cantidad_field, total_field, usuario_field, producto_field, cliente_field], guardar, on_cancel=lambda e: mostrar_ventas())

        def eliminar_venta(venta):
            def aceptar(_=None):
                try:
                    venta_dao.eliminar(venta.id_venta)
                    mostrar_ventas()
                    set_message("Venta eliminada correctamente.", PRIMARY)
                except Exception as exc:
                    set_message(f"Error al eliminar venta: {exc}")

            show_confirm_page(f"¿Eliminar la venta {venta.id_venta}?", aceptar, on_cancel=lambda e: mostrar_ventas())

        rows = []
        for venta in ventas:
            rows.append(
                ft.DataRow(
                    cells = [
                        ft.DataCell(ft.Text(str(venta.id_venta))),
                        ft.DataCell(ft.Text(str(venta.fecha_venta))),
                        ft.DataCell(ft.Text(str(venta.cantidad_producto))),
                        ft.DataCell(ft.Text(str(venta.total_venta))),
                        ft.DataCell(ft.Text(str(venta.id_usuario))),
                        ft.DataCell(ft.Text(str(venta.id_producto))),
                        ft.DataCell(ft.Text(str(venta.id_cliente))),
                        ft.DataCell(
                            ft.Row(
                                spacing = 0,
                                controls = [
                                    ft.IconButton(ft.Icons.EDIT, tooltip = "Editar", on_click = click_and_call(lambda e, v=venta: editar_venta(v), 'editar_venta')),
                                    ft.IconButton(ft.Icons.DELETE, tooltip = "Eliminar", icon_color = ft.Colors.RED_600, on_click = click_and_call(lambda e, v=venta: eliminar_venta(v), 'eliminar_venta')),
                                ],
                            )
                        ),
                    ]
                )
            )

        columnas = [
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Fecha")),
            ft.DataColumn(ft.Text("Cantidad")),
            ft.DataColumn(ft.Text("Total")),
            ft.DataColumn(ft.Text("Usuario")),
            ft.DataColumn(ft.Text("Producto")),
            ft.DataColumn(ft.Text("Cliente")),
            ft.DataColumn(ft.Text("Acciones")),
        ]

        refresh(lambda: layout_base("Ventas", table_view("Ventas", "Registro de ventas realizadas.", "Agregar venta", columnas, rows, abrir_nuevo)))

    def dashboard():
        return ft.Column(
            expand = True,
            alignment = ft.MainAxisAlignment.CENTER,
            horizontal_alignment = ft.CrossAxisAlignment.CENTER,
            controls = [
                ft.Text("RANCHO 'TRES CULTIVOS'", size = 22, weight = ft.FontWeight.BOLD, text_align = ft.TextAlign.CENTER),
                ft.Container(height = 12),
                ft.Text("Sistema administrativo", size = 16, color = ft.Colors.BLACK54),
                ft.Container(height = 30),
                ft.Column(
                    horizontal_alignment = ft.CrossAxisAlignment.CENTER,
                    spacing = 18,
                    controls = [
                        ft.Row(
                            alignment = ft.MainAxisAlignment.CENTER,
                            spacing = 18,
                            controls = [
                                home_card("CATEGORÍAS", ft.Icons.CATEGORY, lambda e: mostrar_categorias()),
                                home_card("CLIENTES", ft.Icons.PEOPLE, lambda e: mostrar_clientes()),
                                home_card("VENTAS", ft.Icons.POINT_OF_SALE, lambda e: mostrar_ventas()),
                            ],
                        ),
                        ft.Row(
                            alignment = ft.MainAxisAlignment.CENTER,
                            spacing = 18,
                            controls = [
                                home_card("USUARIOS", ft.Icons.PERSON, lambda e: mostrar_usuarios()),
                                home_card("PRODUCTOS", ft.Icons.LOCAL_GROCERY_STORE, lambda e: mostrar_productos()),
                            ],
                        ),
                    ],
                ),
            ],
        )

    mostrar_login()

    page.add(contenido)
    page.update()


if __name__ == "__main__":
    ft.run(main_window)
