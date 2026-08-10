class Categoria:
    def __init__(self, id_categoria=None, nombre=None, productos=None):
        self.id_categoria = id_categoria
        self.nombre = nombre
        self.productos = productos if productos is not None else []

    def mostrar_info(self):
        return f"Categoría {self.id_categoria}: {self.nombre}"

    def __repr__(self):
        return f"Categoria(id_categoria={self.id_categoria}, nombre='{self.nombre}')"
    