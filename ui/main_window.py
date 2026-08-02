import flet as ft

# Importaciones de tus vistas/formularios de UI
# (Asegúrate de descomentar o crear estos archivos en tu carpeta ui)
# from ui.categoria_form import categoria_form
# from ui.producto_form import producto_form
# from ui.cliente_form import cliente_form
# from ui.usuario_form import usuario_form
# from ui.venta_form import venta_form

def main_window(page: ft.Page):
    # Configuración de la ventana principal
    page.title = "Rancho Tres Cultivos"
    page.window_width = 1100
    page.window_height = 700
    page.padding = 0
    page.bgcolor = ft.Colors.WHITE

    # Contenedor central dinámico (el área que cambia según la opción del menú)
    contenido = ft.Container(
        padding = 20,
        expand = True
    )

    # Vista de Inicio / Menú Principal (Inspirado en tus pantallas de Figma)
    def inicio():
        return ft.Column(
            controls = [
                ft.Text(
                    "RANCHO 'TRES CULTIVOS'",
                    size = 22,
                    weight = ft.FontWeight.BOLD,
                    text_align = ft.TextAlign.CENTER
                ),
                ft.Container(height = 10),
                # Botones principales del menú del sistema
                ft.ElevatedButton(
                    "CATEGORÍAS",
                    icon = ft.Icons.CATEGORY,
                    width = 250,
                    bgcolor = ft.Colors.BROWN_300,
                    color = ft.Colors.WHITE,
                    on_click = mostrar_categorias
                ),
                ft.ElevatedButton(
                    "CLIENTES",
                    icon = ft.Icons.PEOPLE,
                    width = 250,
                    bgcolor = ft.Colors.BROWN_300,
                    color = ft.Colors.WHITE,
                    on_click = mostrar_clientes
                ),
                ft.ElevatedButton(
                    "VENTAS",
                    icon = ft.Icons.POINT_OF_SALE,
                    width = 250,
                    bgcolor = ft.Colors.BROWN_300,
                    color = ft.Colors.WHITE,
                    on_click = mostrar_ventas
                ),
                ft.ElevatedButton(
                    "USUARIOS",
                    icon = ft.Icons.PERSON,
                    width = 250,
                    bgcolor = ft.Colors.BROWN_300,
                    color = ft.Colors.WHITE,
                    on_click = mostrar_usuarios
                ),
            ],
            spacing = 15,
            horizontal_alignment = ft.CrossAxisAlignment.CENTER,
            alignment = ft.MainAxisAlignment.CENTER
        )
    
    def mostrar_inicio(e=None):
        contenido.content = inicio()
        page.update()

    # Funciones para manejar la navegación entre las vistas de tu sistema
    def mostrar_categorias(e=None):
        # contenido.content = categoria_form(mostrar_inicio)
        contenido.content = ft.Text("Vista de Categorías (En desarrollo)", size=18, weight=ft.FontWeight.BOLD)
        page.update()

    def mostrar_clientes(e=None):
        # contenido.content = cliente_form(mostrar_inicio)
        contenido.content = ft.Text("Vista de Clientes (En desarrollo)", size=18, weight=ft.FontWeight.BOLD)
        page.update()

    def mostrar_ventas(e=None):
        # contenido.content = venta_form(mostrar_inicio)
        contenido.content = ft.Text("Vista de Ventas (En desarrollo)", size=18, weight=ft.FontWeight.BOLD)
        page.update()

    def mostrar_usuarios(e=None):
        # contenido.content = usuario_form(mostrar_inicio)
        contenido.content = ft.Text("Vista de Usuarios (En desarrollo)", size=18, weight=ft.FontWeight.BOLD)
        page.update()

    # Barra superior verde característica de tus wireframes
    barra_superior = ft.Container(
        bgcolor = ft.Colors.GREEN_400,
        padding = 10,
        content = ft.Row(
            controls = [
                ft.IconButton(
                    icon = ft.Icons.HOME,
                    icon_color = ft.Colors.BLACK,
                    on_click = mostrar_inicio
                ),
                ft.IconButton(
                    icon = ft.Icons.MENU,
                    icon_color = ft.Colors.BLACK,
                    on_click = lambda e: print("Menú hamburguesa")
                ),
                ft.Row(
                    controls=[
                        ft.Text("HOLA!", size=14, weight=ft.FontWeight.BOLD),
                        ft.IconButton(
                            icon = ft.Icons.EXIT_TO_APP,
                            icon_color = ft.Colors.BLACK,
                            on_click = lambda e: print("Salir / Cerrar sesión")
                        )
                    ],
                    alignment = ft.MainAxisAlignment.END
                )
            ],
            alignment = ft.MainAxisAlignment.SPACE_BETWEEN
        )
    )

    # Pie de página verde con la etiqueta Copyright de tus pantallas
    pie_pagina = ft.Container(
        bgcolor = ft.Colors.GREEN_300,
        padding = 8,
        alignment = ft.alignment.center,
        content = ft.Text(
            "@Copyright",
            size = 12,
            weight = ft.FontWeight.BOLD,
            color = ft.Colors.BLACK54
        )
    )

    # Estructura general de la ventana (Layout principal)
    layout_principal = ft.Column(
        controls = [
            barra_superior,
            contenido,
            pie_pagina
        ],
        expand = True,
        spacing = 0
    )

    # Agregar el layout a la página y mostrar inicio por defecto
    page.add(layout_principal)
    mostrar_inicio()

if __name__ == "___main___":
    ft.app(target=main_window)