class Venta:
    def __init__(self, id_venta, fecha_venta, cantidad_producto, total_venta, id_usuario, id_producto, id_cliente):
        self.id_venta = id_venta  # PK
        self.fecha_venta = fecha_venta
        self.cantidad_producto = cantidad_producto
        self.total_venta = total_venta
        self.id_usuario = id_usuario   # FK → Usuario
        self.id_producto = id_producto # FK → Producto
        self.id_cliente = id_cliente   # FK → Cliente

    def mostrar_info(self):
        return f"Venta {self.id_venta}: {self.cantidad_producto} unidades - Total: ${self.total_venta} - Fecha: {self.fecha_venta}"