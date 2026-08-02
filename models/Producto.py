class Producto:
    def __init__(self, id_producto, nombre, precio, stock, id_categoria, id_usuario):
        self.id_producto = id_producto  # PK
        self.nombre = nombre
        self.precio = precio
        self.stock = stock
        self.id_categoria = id_categoria  # FK → Categoria
        self.id_usuario = id_usuario      # FK → Usuario

    def mostrar_info(self):
        return f"Producto {self.id_producto}: {self.nombre} - ${self.precio} - Stock: {self.stock}"