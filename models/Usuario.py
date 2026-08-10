class Usuario:
    def __init__(self, id_usuario, tipo_usuario, nombre, apellido_paterno, apellido_materno, telefono, contrasena=""):
        self.id_usuario = id_usuario  # PK
        self.tipo_usuario = tipo_usuario
        self.nombre = nombre
        self.apellido_paterno = apellido_paterno
        self.apellido_materno = apellido_materno
        self.telefono = telefono
        self.contrasena = contrasena

    def mostrar_info(self):
        return f"Usuario {self.id_usuario}: {self.nombre} {self.apellido_paterno} ({self.tipo_usuario})"