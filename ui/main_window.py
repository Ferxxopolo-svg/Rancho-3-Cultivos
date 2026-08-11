from datetime import datetime
import flet as ft

from dao.CategoriaDAO import CategoriaDAO
from dao.ClienteDAO import ClienteDAO
from dao.UsuarioDAO import UsuarioDAO
from dao.VentaDAO import VentaDAO
from models.Categoria import Categoria
from models.Cliente import Cliente
from models.Ticket import crear_pdf_fpdf
from models.Usuario import Usuario
from models.Venta import Venta

PRIMARY = "#A88156"
SECONDARY = "#5E462D"
LIGHT_TONE = "#E5D6C5"
BROWN_DARK = SECONDARY
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
    usuario_dao = UsuarioDAO()
    venta_dao = VentaDAO()

    contenido = ft.Container(expand=True, padding=20)
    mensaje = ft.Text("", size=12, color=ft.Colors.RED_700)
    usuario_actual = {"value": None}

    def set_message(texto: str = "", color=ft.Colors.RED_700):
        mensaje.value = texto
        mensaje.color = color
        if texto:
            page.snack_bar = ft.SnackBar(content=ft.Text(texto, color=TEXT_LIGHT), bgcolor=color)
            page.snack_bar.open = True
        page.update()

    def click_and_call(fn, name: str = None):
        def handler(e=None):
            try:
                set_message("")
                if fn is None:
                    return
                result = fn(e)
                try:
                    page.update()
                except Exception:
                    pass
                return result
            except Exception as exc:
                set_message(f"Error en acción{(' ' + name) if name else ''}: {exc}")
        return handler

    def safe_int(value: str, default: int | None = None):
        if not value or not str(value).strip():
            return default
        return int(str(value).strip())

    def safe_float(value: str, default: float | None = None):
        if not value or not str(value).strip():
            return default
        return float(str(value).strip())

    def field(label, value="", password=False, read_only=False, keyboard_type=None, multiline=False, width=380, on_change=None):
        return ft.TextField(
            label=label,
            value=value,
            password=password,
            read_only=read_only,
            keyboard_type=keyboard_type,
            multiline=multiline,
            width=width,
            on_change=on_change,
        )

    def cerrar_sesion(e=None):
        usuario_actual["value"] = None
        mostrar_login()

    def mostrar_login(e=None):
        login_id = field("ID de usuario", keyboard_type=ft.KeyboardType.NUMBER, width=320)
        login_password = field("Contraseña", password=True, width=320)

        def autenticar(_=None):
            try:
                uid = safe_int(login_id.value)
                if uid is None:
                    set_message("Por favor ingrese un ID válido.", ft.Colors.RED_700)
                    return
                usuario = usuario_dao.autenticar(uid, login_password.value)
                if not usuario:
                    set_message("Credenciales inválidas.", ft.Colors.RED_700)
                    return
                usuario_actual["value"] = usuario
                set_message(f"Bienvenido, {usuario.nombre}.", PRIMARY)
                mostrar_inicio()
            except Exception as exc:
                set_message(f"No se pudo autenticar: {exc}")

        contenido.content = ft.Container(
            expand=True,
            alignment=ft.Alignment.CENTER,
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=18,
                controls=[
                    ft.Container(
                        width=420,
                        padding=24,
                        border_radius=20,
                        bgcolor=ft.Colors.WHITE,
                        content=ft.Column(
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                ft.Text("Rancho Tres Cultivos", size=20, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                                ft.Container(height=10),
                                ft.Image(src=LOGIN_LOGO, width=150, height=150),
                                ft.Container(height=6),
                                ft.Text("Iniciar sesión", size=18, weight=ft.FontWeight.BOLD),
                                ft.Container(height=10),
                                login_id,
                                login_password,
                                ft.ElevatedButton("Entrar", bgcolor=SECONDARY, color=TEXT_LIGHT, width=160, on_click=click_and_call(autenticar, 'autenticar')),
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
                icon=ft.Icons.HOME,
                icon_color=SECONDARY,
                tooltip="Inicio",
                on_click=click_and_call(lambda e: mostrar_inicio(), 'mostrar_inicio')
            ),
            ft.Container(
                width=50,
                height=50,
                padding=4,
                border_radius=25,
                bgcolor=ft.Colors.WHITE,
                alignment=ft.Alignment.CENTER,
                content=ft.Image(
                    src=LOGIN_LOGO,
                    width=46,
                    height=46,
                    fit=ft.BoxFit.CONTAIN,
                    tooltip="Logo Rancho Tres Cultivos",
                ),
            ),
            ft.Column(
                spacing=0,
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.Text(
                        title,
                        weight=ft.FontWeight.BOLD,
                        size=17,
                        color=TEXT_DARK,
                    ),
                    ft.Text(
                        "Rancho Tres Cultivos",
                        size=10,
                        color=SECONDARY,
                    ),
                ],
            ),
            ft.Container(expand=True),
        ]

        if usuario_actual["value"] is not None:
            header_controls.extend([
                ft.Container(
                    padding=8,
                    border_radius=18,
                    bgcolor=LIGHT_TONE,
                    content=ft.Row(
                        spacing=6,
                        controls=[
                            ft.Icon(
                                ft.Icons.ACCOUNT_CIRCLE,
                                size=20,
                                color=SECONDARY,
                            ),
                            ft.Text(
                                f"{usuario_actual['value'].nombre}",
                                size=12,
                                weight=ft.FontWeight.BOLD,
                                color=TEXT_DARK,
                            ),
                        ],
                    ),
                ),
                ft.IconButton(
                    icon=ft.Icons.LOGOUT,
                    icon_color=SECONDARY,
                    tooltip="Cerrar sesión",
                    on_click=click_and_call(cerrar_sesion, 'cerrar_sesion')
                ),
            ])

        return ft.Container(
            height=70,
            bgcolor=PRIMARY,
            padding=8,
            content=ft.Row(
                controls=header_controls,
                spacing=12,
                alignment=ft.MainAxisAlignment.START,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            )
        )

    def footer():
        return ft.Container(
            bgcolor=LIGHT_TONE,
            padding=8,
            alignment=ft.Alignment.CENTER,
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=2,
                controls=[
                    ft.Text("Rancho 3 Cultivos", size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK54),
                    ft.Text("Todos los derechos reservados", size=11, color=ft.Colors.BLACK54),
                    ft.Text("Versión 1.5", size=10, color=ft.Colors.BLACK45),
                ]
            )
        )
    def layout_base(title: str, body):
        return ft.Column(
            controls=[
                top_bar(title),
                ft.Container(expand=True, padding=20, content=body),
                footer()
            ],
            expand=True,
            spacing=0
        )

    def table_view(title: str, subtitle: str, add_label: str, columns, rows, on_add):
        return ft.Column(
            expand=True,
            spacing=16,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Column(
                            spacing=2,
                            controls=[
                                ft.Text(title, size=24, weight=ft.FontWeight.BOLD, color=TEXT_DARK),
                                ft.Text(subtitle, size=12, color=ft.Colors.BLACK54),
                            ],
                        ),
                        ft.ElevatedButton(
                            add_label,
                            icon=ft.Icons.ADD,
                            bgcolor=SECONDARY,
                            color=TEXT_LIGHT,
                            on_click=click_and_call(on_add, f'add_{add_label}'),
                        ),
                    ],
                ),
                mensaje,
                ft.Container(
                    expand=True,
                    border_radius=10,
                    padding=10,
                    content=ft.Column(
                        expand=True,
                        scroll=ft.ScrollMode.AUTO,
                        controls=[
                            ft.DataTable(
                                expand=True,
                                column_spacing=20,
                                heading_row_color=LIGHT_TONE,
                                columns=columns,
                                rows=rows,
                            )
                        ],
                    ),
                ),
            ],
        )

    def show_form_page(title: str, fields, on_save, on_cancel=None):
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
            else:
                mostrar_inicio()

        body = ft.Column(
            controls=[
                ft.Text(title, size=20, weight=ft.FontWeight.BOLD),
                ft.Container(height=12),
            ] + fields + [
                ft.Row(spacing=12, alignment=ft.MainAxisAlignment.END, controls=[
                    ft.TextButton("Cancelar", on_click=wrap_cancel),
                    ft.ElevatedButton("Guardar", bgcolor=SECONDARY, color=TEXT_LIGHT, on_click=wrap_save),
                ])
            ],
            scroll=ft.ScrollMode.AUTO,
        )

        contenido.content = layout_base(title, ft.Container(padding=10, content=body, expand=True))
        page.update()

    def show_confirm_page(message: str, on_accept, on_cancel=None):
        def aceptar(e=None):
            try:
                on_accept(e)
            except Exception as exc:
                set_message(f"Error: {exc}")

        def cancelar(e=None):
            if on_cancel:
                try:
                    on_cancel(e)
                except Exception as exc:
                    set_message(f"Error: {exc}")
            else:
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

    def home_card(texto, icono, callback):
        return ft.Container(
            width=230,
            height=130,
            border_radius=16,
            bgcolor=ft.Colors.WHITE,
            ink=True,
            on_click=callback,
            alignment=ft.Alignment.CENTER,
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=8,
                controls=[
                    ft.Icon(icono, size=38, color=SECONDARY),
                    ft.Text(texto, size=16, weight=ft.FontWeight.BOLD, color=TEXT_DARK),
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
                alignment=ft.Alignment.CENTER,
                expand=True,
                content=ft.Column(
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=24,
                    controls=[
                        ft.Container(
                            width=180,
                            height=180,
                            border_radius=90,
                            alignment=ft.Alignment.CENTER,
                            content=ft.Text(
                                "Rancho\nTres Cultivos",
                                text_align=ft.TextAlign.CENTER,
                                size=20,
                                weight=ft.FontWeight.BOLD,
                                color=BROWN_DARK,
                            ),
                        ),
                        ft.Text("Sistema de gestión", size=18, weight=ft.FontWeight.BOLD, color=TEXT_DARK),
                        ft.Container(
                            width=760,
                            content=ft.Column(
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=20,
                                controls=[
                                    ft.Row(
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        spacing=20,
                                        controls=[
                                            home_card("Usuarios", ft.Icons.PERSON, lambda e: mostrar_usuarios()),
                                            home_card("Clientes", ft.Icons.PEOPLE, lambda e: mostrar_clientes()),
                                        ],
                                    ),
                                    ft.Row(
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        spacing=20,
                                        controls=[
                                            home_card("Categorías", ft.Icons.CATEGORY, lambda e: mostrar_categorias()),
                                            home_card("Ventas", ft.Icons.POINT_OF_SALE, lambda e: mostrar_ventas()),
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

    # --- CATEGORÍAS ---
    def mostrar_categorias(e=None):
        try:
            categorias = categoria_dao.obtener_todo()
        except Exception as exc:
            set_message(f"No se pudieron cargar las categorías: {exc}")
            categorias = []

        def abrir_nuevo(_=None):
            siguiente_id = categoria_dao.obtener_ultimo_id() + 1
            id_field = field("ID Categoría/Cultivo", str(siguiente_id), read_only=True, width=160)
            
            dd_nombre = ft.Dropdown(
                label="Nombre de cultivo / producto",
                width=320,
                options=[
                    ft.dropdown.Option("Durazno"),
                    ft.dropdown.Option("Haba"),
                    ft.dropdown.Option("Nopal"),
                    ft.dropdown.Option("Maíz"),
                    ft.dropdown.Option("Frijol"),
                    ft.dropdown.Option("Otro"),
                ],
                value="Durazno",
            )
            variedad_field = field("Variedad / Detalle", value="Toro", width=320)
            precio_field = field("Precio por unidad/kg ($)", width=320, keyboard_type=ft.KeyboardType.NUMBER)
            stock_field = field("Stock disponible", width=320, keyboard_type=ft.KeyboardType.NUMBER)

            def guardar(_):
                nombre_final = dd_nombre.value.strip() if dd_nombre.value else "Cultivo"
                if variedad_field.value.strip():
                    nombre_completo = f"{nombre_final} ({variedad_field.value.strip()})"
                else:
                    nombre_completo = nombre_final

                cat = Categoria(
                    id_categoria=safe_int(id_field.value),
                    nombre=nombre_completo,
                    precio=safe_float(precio_field.value, 0.0),
                    stock=safe_int(stock_field.value, 0),
                )
                categoria_dao.insertar(cat)
                mostrar_categorias()
                set_message("Categoría / Cultivo guardado correctamente.", PRIMARY)

            show_form_page(
                "Agregar Categoría / Cultivo",
                [id_field, dd_nombre, variedad_field, precio_field, stock_field],
                guardar,
                on_cancel=lambda e: mostrar_categorias()
            )

        def editar_categoria(cat):
            id_field = field("ID Categoría", str(cat.id_categoria), read_only=True, width=160)
            nombre_field = field("Nombre de categoría / producto", getattr(cat, "nombre", ""), width=320)
            precio_field = field("Precio ($)", str(getattr(cat, "precio", 0.0)), width=320, keyboard_type=ft.KeyboardType.NUMBER)
            stock_field = field("Stock", str(getattr(cat, "stock", 0)), width=320, keyboard_type=ft.KeyboardType.NUMBER)

            def guardar(_):
                cat_mod = Categoria(
                    id_categoria=safe_int(id_field.value),
                    nombre=nombre_field.value.strip(),
                    precio=safe_float(precio_field.value, 0.0),
                    stock=safe_int(stock_field.value, 0),
                )
                categoria_dao.actualizar(cat_mod)
                mostrar_categorias()
                set_message("Categoría actualizada correctamente.", PRIMARY)

            show_form_page(
                "Editar Categoría / Cultivo",
                [id_field, nombre_field, precio_field, stock_field],
                guardar,
                on_cancel=lambda e: mostrar_categorias()
            )

        def eliminar_categoria(cat):
            def aceptar(_=None):
                categoria_dao.eliminar(cat.id_categoria)
                mostrar_categorias()
                set_message("Categoría eliminada correctamente.", PRIMARY)

            show_confirm_page(f"¿Eliminar la categoría {cat.nombre}?", aceptar, on_cancel=lambda e: mostrar_categorias())

        rows = []
        for cat in categorias:
            precio_val = f"${getattr(cat, 'precio', 0.0):.2f}" if hasattr(cat, 'precio') else "-"
            stock_val = str(getattr(cat, 'stock', '-')) if hasattr(cat, 'stock') else "-"
            rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(cat.id_categoria))),
                        ft.DataCell(ft.Text(cat.nombre)),
                        ft.DataCell(ft.Text(precio_val)),
                        ft.DataCell(ft.Text(stock_val)),
                        ft.DataCell(
                            ft.Row(
                                spacing=0,
                                controls=[
                                    ft.IconButton(ft.Icons.EDIT, tooltip="Editar", on_click=click_and_call(lambda e, c=cat: editar_categoria(c), 'editar_categoria')),
                                    ft.IconButton(ft.Icons.DELETE, tooltip="Eliminar", icon_color=ft.Colors.RED_600, on_click=click_and_call(lambda e, c=cat: eliminar_categoria(c), 'eliminar_categoria')),
                                ],
                            )
                        ),
                    ]
                )
            )

        columnas = [
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Cultivo / Producto")),
            ft.DataColumn(ft.Text("Precio")),
            ft.DataColumn(ft.Text("Stock")),
            ft.DataColumn(ft.Text("Acciones")),
        ]

        contenido.content = layout_base("Categorías", table_view("Categorías / Cultivos", "Gestión de cultivos y productos (Durazno, Haba, etc.).", "Agregar cultivo/categoría", columnas, rows, abrir_nuevo))
        page.update()

    # --- USUARIOS ---
    def mostrar_usuarios(e=None):
        try:
            usuarios = usuario_dao.obtener_todo()
        except Exception as exc:
            set_message(f"No se pudieron cargar los usuarios: {exc}")
            usuarios = []

        def abrir_nuevo(_=None):
            siguiente_id = usuario_dao.obtener_ultimo_id() + 1
            id_field = field("ID", str(siguiente_id), read_only=True, width=160)
            tipo_field = field("Tipo usuario", width=320)
            nombre_field = field("Nombre", width=320)
            ap_paterno_field = field("Apellido paterno", width=320)
            ap_materno_field = field("Apellido materno", width=320)
            telefono_field = field("Teléfono", width=320)
            contrasena_field = field("Contraseña", password=True, width=320)

            def guardar(_):
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

            show_form_page("Agregar usuario", [id_field, tipo_field, nombre_field, ap_paterno_field, ap_materno_field, telefono_field, contrasena_field], guardar, on_cancel=lambda e: mostrar_usuarios())

        def editar_usuario(usuario):
            id_field = field("ID", str(usuario.id_usuario), read_only=True, width=160)
            tipo_field = field("Tipo usuario", usuario.tipo_usuario, width=320)
            nombre_field = field("Nombre", usuario.nombre, width=320)
            ap_paterno_field = field("Apellido paterno", usuario.apellido_paterno, width=320)
            ap_materno_field = field("Apellido materno", usuario.apellido_materno, width=320)
            telefono_field = field("Teléfono", usuario.telefono, width=320)
            contrasena_field = field("Contraseña", usuario.contrasena, password=True, width=320)

            def guardar(_):
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

            show_form_page("Editar usuario", [id_field, tipo_field, nombre_field, ap_paterno_field, ap_materno_field, telefono_field, contrasena_field], guardar, on_cancel=lambda e: mostrar_usuarios())

        def eliminar_usuario(usuario):
            def aceptar(_=None):
                usuario_dao.eliminar(usuario.id_usuario)
                mostrar_usuarios()
                set_message("Usuario eliminado correctamente.", PRIMARY)

            show_confirm_page(f"¿Eliminar al usuario {usuario.nombre} {usuario.apellido_paterno}?", aceptar, on_cancel=lambda e: mostrar_usuarios())

        rows = []
        for usuario in usuarios:
            rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(usuario.id_usuario))),
                        ft.DataCell(ft.Text(usuario.tipo_usuario)),
                        ft.DataCell(ft.Text(usuario.nombre)),
                        ft.DataCell(ft.Text(usuario.apellido_paterno)),
                        ft.DataCell(ft.Text(usuario.apellido_materno)),
                        ft.DataCell(ft.Text(usuario.telefono)),
                        ft.DataCell(
                            ft.Row(
                                spacing=0,
                                controls=[
                                    ft.IconButton(ft.Icons.EDIT, tooltip="Editar", on_click=click_and_call(lambda e, u=usuario: editar_usuario(u), 'editar_usuario')),
                                    ft.IconButton(ft.Icons.DELETE, tooltip="Eliminar", icon_color=ft.Colors.RED_600, on_click=click_and_call(lambda e, u=usuario: eliminar_usuario(u), 'eliminar_usuario')),
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

        contenido.content = layout_base("Usuarios", table_view("Usuarios", "Gestión de usuarios del sistema.", "Agregar usuario", columnas, rows, abrir_nuevo))
        page.update()

    # --- CLIENTES ---
    def mostrar_clientes(e=None):
        try:
            clientes = cliente_dao.obtener_todo()
            usuarios = usuario_dao.obtener_todo()
        except Exception as exc:
            set_message(f"No se pudieron cargar los clientes: {exc}")
            clientes, usuarios = [], []

        mapa_usuarios = {u.id_usuario: f"{u.nombre} {u.apellido_paterno}" for u in usuarios}

        def abrir_nuevo(_=None):
            siguiente_id = cliente_dao.obtener_ultimo_id() + 1
            id_field = field("ID", str(siguiente_id), read_only=True, width=160)
            nombre_field = field("Nombre", width=320)
            ap_paterno_field = field("Apellido paterno", width=320)
            ap_materno_field = field("Apellido materno", width=320)
            telefono_field = field("Teléfono", width=320)
            correo_field = field("Correo electrónico", width=320)

            def guardar(_):
                cliente = Cliente(
                    safe_int(id_field.value),
                    nombre_field.value.strip(),
                    ap_paterno_field.value.strip(),
                    ap_materno_field.value.strip(),
                    telefono_field.value.strip(),
                    correo_field.value.strip(),
                    usuario_actual["value"].id_usuario,
                )
                cliente_dao.insertar(cliente)
                mostrar_clientes()
                set_message("Cliente guardado correctamente.", PRIMARY)

            show_form_page("Agregar cliente", [id_field, nombre_field, ap_paterno_field, ap_materno_field, telefono_field, correo_field], guardar, on_cancel=lambda e: mostrar_clientes())

        def editar_cliente(cliente):
            id_field = field("ID", str(cliente.id_cliente), read_only=True, width=160)
            nombre_field = field("Nombre", cliente.nombre, width=320)
            ap_paterno_field = field("Apellido paterno", cliente.apellido_paterno, width=320)
            ap_materno_field = field("Apellido materno", cliente.apellido_materno, width=320)
            telefono_field = field("Teléfono", cliente.telefono, width=320)
            correo_field = field("Correo electrónico", cliente.correo, width=320)

            def guardar(_):
                cliente_mod = Cliente(
                    safe_int(id_field.value),
                    nombre_field.value.strip(),
                    ap_paterno_field.value.strip(),
                    ap_materno_field.value.strip(),
                    telefono_field.value.strip(),
                    correo_field.value.strip(),
                    cliente.id_usuario,
                )
                cliente_dao.actualizar(cliente_mod)
                mostrar_clientes()
                set_message("Cliente actualizado correctamente.", PRIMARY)

            show_form_page("Editar cliente", [id_field, nombre_field, ap_paterno_field, ap_materno_field, telefono_field, correo_field], guardar, on_cancel=lambda e: mostrar_clientes())

        def eliminar_cliente(cliente):
            def aceptar(_=None):
                cliente_dao.eliminar(cliente.id_cliente)
                mostrar_clientes()
                set_message("Cliente eliminado correctamente.", PRIMARY)

            show_confirm_page(f"¿Eliminar al cliente {cliente.nombre} {cliente.apellido_paterno}?", aceptar, on_cancel=lambda e: mostrar_clientes())

        rows = []
        for cliente in clientes:
            nombre_user = mapa_usuarios.get(cliente.id_usuario, str(cliente.id_usuario))
            rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(cliente.id_cliente))),
                        ft.DataCell(ft.Text(cliente.nombre)),
                        ft.DataCell(ft.Text(cliente.apellido_paterno)),
                        ft.DataCell(ft.Text(cliente.apellido_materno)),
                        ft.DataCell(ft.Text(cliente.telefono)),
                        ft.DataCell(ft.Text(cliente.correo)),
                        ft.DataCell(ft.Text(nombre_user)),
                        ft.DataCell(
                            ft.Row(
                                spacing=0,
                                controls=[
                                    ft.IconButton(ft.Icons.EDIT, tooltip="Editar", on_click=click_and_call(lambda e, c=cliente: editar_cliente(c), 'editar_cliente')),
                                    ft.IconButton(ft.Icons.DELETE, tooltip="Eliminar", icon_color=ft.Colors.RED_600, on_click=click_and_call(lambda e, c=cliente: eliminar_cliente(c), 'eliminar_cliente')),
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

        contenido.content = layout_base("Clientes", table_view("Clientes", "Gestión de clientes registrados.", "Agregar cliente", columnas, rows, abrir_nuevo))
        page.update()

    # --- VENTAS ---
    def mostrar_ventas(e=None):
        try:
            ventas = venta_dao.obtener_todo()
            categorias = categoria_dao.obtener_todo()
            clientes = cliente_dao.obtener_todo()
        except Exception as exc:
            set_message(f"No se pudieron cargar los datos de ventas: {exc}")
            ventas, categorias, clientes = [], [], []

        def abrir_nuevo(_=None):
            siguiente_id = venta_dao.obtener_ultimo_id() + 1
            id_field = field("ID Venta", str(siguiente_id), read_only=True, width=160)
            fecha_field = field("Fecha", value=datetime.now().strftime("%Y-%m-%d"), read_only=True, width=320)
            cantidad_field = field("Cantidad", value="1", width=320, keyboard_type=ft.KeyboardType.NUMBER)
            total_field = field("Total ($)", value="0.0", read_only=True, width=320)

            dd_categoria = ft.Dropdown(
                label="Seleccionar Cultivo / Producto",
                width=320,
                options=[ft.dropdown.Option(str(c.id_categoria), f"{c.nombre}") for c in categorias]
            )

            dd_cliente = ft.Dropdown(
                label="Seleccionar Cliente",
                width=320,
                options=[ft.dropdown.Option(str(cl.id_cliente), f"{cl.nombre} {cl.apellido_paterno}") for cl in clientes]
            )

            def auto_calcular(e):
                if dd_categoria.value and cantidad_field.value:
                    cat_sel = next((c for c in categorias if str(c.id_categoria) == str(dd_categoria.value)), None)
                    cant = safe_int(cantidad_field.value, 0)
                    precio = getattr(cat_sel, 'precio', 0.0) if cat_sel else 0.0
                    if cat_sel and cant > 0:
                        total_field.value = str(round(precio * cant, 2))
                        page.update()

            dd_categoria.on_change = auto_calcular
            cantidad_field.on_change = auto_calcular

            def guardar(_):
                if not dd_categoria.value or not dd_cliente.value:
                    set_message("Selecciona un cultivo/producto y un cliente.", ft.Colors.RED_700)
                    return

                venta = Venta(
                    safe_int(id_field.value),
                    fecha_field.value.strip(),
                    safe_int(cantidad_field.value),
                    safe_float(total_field.value),
                    usuario_actual["value"].id_usuario,
                    safe_int(dd_categoria.value),
                    safe_int(dd_cliente.value),
                )
                venta_dao.insertar(venta)
                mostrar_ventas()
                set_message("Venta registrada correctamente.", PRIMARY)

            show_form_page(
                "Agregar Venta",
                [id_field, fecha_field, dd_cliente, dd_categoria, cantidad_field, total_field],
                guardar,
                on_cancel=lambda e: mostrar_ventas()
            )

        def editar_venta(venta):
            id_field = field("ID Venta", str(venta.id_venta), read_only=True, width=160)
            fecha_field = field("Fecha", str(venta.fecha_venta), read_only=True, width=320)
            cantidad_field = field("Cantidad", str(venta.cantidad_producto), width=320, keyboard_type=ft.KeyboardType.NUMBER)
            total_field = field("Total ($)", str(venta.total_venta), read_only=True, width=320)

            dd_categoria = ft.Dropdown(
                label="Seleccionar Cultivo / Producto",
                width=320,
                value=str(getattr(venta, 'id_producto', getattr(venta, 'id_categoria', ''))),
                options=[ft.dropdown.Option(str(c.id_categoria), f"{c.nombre}") for c in categorias]
            )

            dd_cliente = ft.Dropdown(
                label="Seleccionar Cliente",
                width=320,
                value=str(venta.id_cliente),
                options=[ft.dropdown.Option(str(cl.id_cliente), f"{cl.nombre} {cl.apellido_paterno}") for cl in clientes]
            )

            def auto_calcular(e):
                if dd_categoria.value and cantidad_field.value:
                    cat_sel = next((c for c in categorias if str(c.id_categoria) == str(dd_categoria.value)), None)
                    cant = safe_int(cantidad_field.value, 0)
                    precio = getattr(cat_sel, 'precio', 0.0) if cat_sel else 0.0
                    if cat_sel and cant > 0:
                        total_field.value = str(round(precio * cant, 2))
                        page.update()

            dd_categoria.on_change = auto_calcular
            cantidad_field.on_change = auto_calcular

            def guardar(_):
                if not dd_categoria.value or not dd_cliente.value:
                    set_message("Selecciona un cultivo y un cliente válidos.", ft.Colors.RED_700)
                    return

                venta_mod = Venta(
                    safe_int(id_field.value),
                    fecha_field.value.strip(),
                    safe_int(cantidad_field.value),
                    safe_float(total_field.value),
                    venta.id_usuario,
                    safe_int(dd_categoria.value),
                    safe_int(dd_cliente.value),
                )
                venta_dao.actualizar(venta_mod)
                mostrar_ventas()
                set_message("Venta actualizada correctamente.", PRIMARY)

            show_form_page(
                "Editar Venta",
                [id_field, fecha_field, dd_cliente, dd_categoria, cantidad_field, total_field],
                guardar,
                on_cancel=lambda e: mostrar_ventas()
            )

        def eliminar_venta(venta):
            def aceptar(_=None):
                venta_dao.eliminar(venta.id_venta)
                mostrar_ventas()
                set_message("Venta eliminada correctamente.", PRIMARY)

            show_confirm_page(f"¿Eliminar la venta con ID {venta.id_venta}?", aceptar, on_cancel=lambda e: mostrar_ventas())

        def generar_ticket(venta):
            cliente = next(
                (cl for cl in clientes if str(cl.id_cliente) == str(venta.id_cliente)),
                None,
            )
            categoria = next(
                (c for c in categorias if str(c.id_categoria) == str(venta.id_producto)),
                None,
            )

            if cliente:
                nombre_cliente = " ".join(
                    parte
                    for parte in (
                        cliente.nombre,
                        cliente.apellido_paterno,
                        cliente.apellido_materno,
                    )
                    if parte
                )
            else:
                nombre_cliente = f"Cliente ID {venta.id_cliente}"

            nombre_producto = categoria.nombre if categoria else f"ID {venta.id_producto}"
            archivo = crear_pdf_fpdf(
                id_venta=venta.id_venta,
                cliente=nombre_cliente,
                total=venta.total_venta,
                fecha=venta.fecha_venta,
                producto=nombre_producto,
                cantidad=venta.cantidad_producto,
            )
            set_message(f"Ticket generado correctamente en: {archivo}", PRIMARY)

        rows = []
        for venta in ventas:
            prod_id_val = getattr(venta, 'id_producto', getattr(venta, 'id_categoria', '-'))
            rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(venta.id_venta))),
                        ft.DataCell(ft.Text(str(venta.fecha_venta))),
                        ft.DataCell(ft.Text(str(venta.cantidad_producto))),
                        ft.DataCell(ft.Text(f"${venta.total_venta:.2f}")),
                        ft.DataCell(ft.Text(str(venta.id_usuario))),
                        ft.DataCell(ft.Text(str(prod_id_val))),
                        ft.DataCell(ft.Text(str(venta.id_cliente))),
                        ft.DataCell(
                            ft.Row(
                                spacing=0,
                                controls=[
                                    ft.IconButton(
                                        ft.Icons.RECEIPT_LONG,
                                        tooltip="Generar ticket PDF",
                                        icon_color=PRIMARY,
                                        on_click=click_and_call(
                                            lambda e, v=venta: generar_ticket(v),
                                            'generar_ticket'
                                        ),
                                    ),
                                    ft.IconButton(ft.Icons.EDIT, tooltip="Editar", on_click=click_and_call(lambda e, v=venta: editar_venta(v), 'editar_venta')),
                                    ft.IconButton(ft.Icons.DELETE, tooltip="Eliminar", icon_color=ft.Colors.RED_600, on_click=click_and_call(lambda e, v=venta: eliminar_venta(v), 'eliminar_venta')),
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
            ft.DataColumn(ft.Text("Categoría/Cultivo")),
            ft.DataColumn(ft.Text("Cliente")),
            ft.DataColumn(ft.Text("Acciones")),
        ]

        contenido.content = layout_base("Ventas", table_view("Ventas", "Registro de ventas realizadas.", "Agregar venta", columnas, rows, abrir_nuevo))
        page.update()

    mostrar_login()
    page.add(contenido)
    page.update()


if __name__ == "__main__":
    ft.app(target=main_window)
    