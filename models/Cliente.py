class Cliente:
    def __init__(self, id_cliente, nombre, apellido_paterno, apellido_materno, telefono, correo, id_usuario):
        self.id_cliente = id_cliente  # PK
        self.nombre = nombre
        self.apellido_paterno = apellido_paterno
        self.apellido_materno = apellido_materno
        self.telefono = telefono
        self.correo = correo
        self.id_usuario = id_usuario 

    def mostrar_info(self):
        return f"Cliente {self.id_cliente}: {self.nombre} {self.apellido_paterno} ({self.correo})"