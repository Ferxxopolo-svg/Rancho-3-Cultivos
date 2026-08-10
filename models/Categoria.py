class Categoria:
    def __init__(self, id_categoria=None, nombre="", productos=None):
        self.id_categoria = id_categoria  # PK
        self.nombre = nombre
        self.productos = productos if productos is not None else []  # Lista de productos asociados

    def mostrar_info(self):
        return f"Categoría {self.id_categoria}: {self.nombre} (Productos: {len(self.productos)})"