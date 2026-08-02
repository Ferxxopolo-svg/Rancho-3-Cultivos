class Categoria:
    def __init__(self, id_categoria, nombre):
        self.id_categoria = id_categoria  # PK
        self.nombre = nombre

    def mostrar_info(self):
        return f"Categoría {self.id_categoria}: {self.nombre}"