-- Datos de ejemplo para Rancho 3 Cultivos

INSERT INTO categoria (id, nombre) VALUES
(1, 'Frutas'),
(2, 'Verduras'),
(3, 'Legumbres');

INSERT INTO usuario (id_usuario, tipo_usuario, nombre, apellido_paterno, apellido_materno, numero_telefono, contrasena) VALUES
(1, 'Administrador', 'Ana', 'Lopez', 'Ramirez', '5551112233', 'admin123'),
(2, 'Cajero', 'Luis', 'Hernandez', 'Gomez', '5552223344', 'cajero123');

INSERT INTO cliente (id_cliente, nombre, apellido_paterno, apellido_materno, numero_telefono, correo_electronico, id_usuario) VALUES
(1, 'Maria', 'Perez', 'Santos', '5553334455', 'maria@example.com', 2),
(2, 'Jose', 'Torres', 'Vega', '5554445566', 'jose@example.com', 2);

INSERT INTO producto (id_producto, nombre, precio, stock, id_categoria, id_usuario) VALUES
(1, 'Durazno Toro', 18.50, 120, 1, 1),
(2, 'Durazno Prisco', 22.00, 90, 1, 1),
(3, 'Nopal', 14.00, 150, 2, 1),
(4, 'Haba', 16.00, 80, 3, 2),
(5, 'Maiz', 12.50, 200, 3, 2);

INSERT INTO venta (id_venta, fecha_venta, cantidad_producto, total_venta, id_usuario, id_producto, id_cliente) VALUES
(1, '2026-08-01', 2, 37.00, 2, 1, 1),
(2, '2026-08-01', 3, 66.00, 2, 2, 2);