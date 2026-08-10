-- Migración para agregar autenticación a una BD existente

ALTER TABLE usuario
ADD COLUMN IF NOT EXISTS contrasena VARCHAR(100) NOT NULL DEFAULT '';

UPDATE usuario
SET contrasena = 'admin123'
WHERE id_usuario = 1 AND contrasena = '';
