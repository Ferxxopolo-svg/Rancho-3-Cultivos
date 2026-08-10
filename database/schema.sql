-- Esquema real para Rancho 3 Cultivos
-- Base de datos sugerida: rancho_3_cultivos

DROP VIEW IF EXISTS vista_categorias;
DROP TABLE IF EXISTS venta CASCADE;
DROP TABLE IF EXISTS producto CASCADE;
DROP TABLE IF EXISTS cliente CASCADE;
DROP TABLE IF EXISTS categoria CASCADE;
DROP TABLE IF EXISTS usuario CASCADE;

DROP FUNCTION IF EXISTS usuario_set_id();
DROP FUNCTION IF EXISTS categoria_set_id();
DROP FUNCTION IF EXISTS cliente_set_id();
DROP FUNCTION IF EXISTS producto_set_id();
DROP FUNCTION IF EXISTS venta_set_id();

DROP SEQUENCE IF EXISTS usuario_id_usuario_seq;
DROP SEQUENCE IF EXISTS categoria_id_seq;
DROP SEQUENCE IF EXISTS cliente_id_cliente_seq;
DROP SEQUENCE IF EXISTS producto_id_producto_seq;
DROP SEQUENCE IF EXISTS venta_id_venta_seq;

CREATE TABLE usuario (
    id_usuario INTEGER PRIMARY KEY,
    tipo_usuario VARCHAR(50) NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    apellido_paterno VARCHAR(100) NOT NULL,
    apellido_materno VARCHAR(100) NOT NULL,
    numero_telefono VARCHAR(20) NOT NULL,
    contrasena VARCHAR(100) NOT NULL
);

CREATE TABLE categoria (
    id INTEGER PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL
);

CREATE TABLE cliente (
    id_cliente INTEGER PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido_paterno VARCHAR(100) NOT NULL,
    apellido_materno VARCHAR(100) NOT NULL,
    numero_telefono VARCHAR(20) NOT NULL,
    correo_electronico VARCHAR(150) NOT NULL,
    id_usuario INTEGER NOT NULL,
    CONSTRAINT fk_cliente_usuario
        FOREIGN KEY (id_usuario)
        REFERENCES usuario (id_usuario)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

CREATE TABLE producto (
    id_producto INTEGER PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    precio NUMERIC(10,2) NOT NULL CHECK (precio >= 0),
    stock INTEGER NOT NULL CHECK (stock >= 0),
    id_categoria INTEGER NOT NULL,
    id_usuario INTEGER NOT NULL,
    CONSTRAINT fk_producto_categoria
        FOREIGN KEY (id_categoria)
        REFERENCES categoria (id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,
    CONSTRAINT fk_producto_usuario
        FOREIGN KEY (id_usuario)
        REFERENCES usuario (id_usuario)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

CREATE TABLE venta (
    id_venta INTEGER PRIMARY KEY,
    fecha_venta DATE NOT NULL,
    cantidad_producto INTEGER NOT NULL CHECK (cantidad_producto > 0),
    total_venta NUMERIC(10,2) NOT NULL CHECK (total_venta >= 0),
    id_usuario INTEGER NOT NULL,
    id_producto INTEGER NOT NULL,
    id_cliente INTEGER NOT NULL,
    CONSTRAINT fk_venta_usuario
        FOREIGN KEY (id_usuario)
        REFERENCES usuario (id_usuario)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,
    CONSTRAINT fk_venta_producto
        FOREIGN KEY (id_producto)
        REFERENCES producto (id_producto)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,
    CONSTRAINT fk_venta_cliente
        FOREIGN KEY (id_cliente)
        REFERENCES cliente (id_cliente)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

CREATE SEQUENCE usuario_id_usuario_seq START WITH 1 INCREMENT BY 1 OWNED BY usuario.id_usuario;
CREATE SEQUENCE categoria_id_seq START WITH 1 INCREMENT BY 1 OWNED BY categoria.id;
CREATE SEQUENCE cliente_id_cliente_seq START WITH 1 INCREMENT BY 1 OWNED BY cliente.id_cliente;
CREATE SEQUENCE producto_id_producto_seq START WITH 1 INCREMENT BY 1 OWNED BY producto.id_producto;
CREATE SEQUENCE venta_id_venta_seq START WITH 1 INCREMENT BY 1 OWNED BY venta.id_venta;

ALTER TABLE usuario ALTER COLUMN id_usuario SET DEFAULT nextval('usuario_id_usuario_seq');
ALTER TABLE categoria ALTER COLUMN id SET DEFAULT nextval('categoria_id_seq');
ALTER TABLE cliente ALTER COLUMN id_cliente SET DEFAULT nextval('cliente_id_cliente_seq');
ALTER TABLE producto ALTER COLUMN id_producto SET DEFAULT nextval('producto_id_producto_seq');
ALTER TABLE venta ALTER COLUMN id_venta SET DEFAULT nextval('venta_id_venta_seq');

CREATE OR REPLACE FUNCTION usuario_set_id()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.id_usuario IS NULL THEN
        NEW.id_usuario := nextval('usuario_id_usuario_seq');
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION categoria_set_id()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.id IS NULL THEN
        NEW.id := nextval('categoria_id_seq');
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION cliente_set_id()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.id_cliente IS NULL THEN
        NEW.id_cliente := nextval('cliente_id_cliente_seq');
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION producto_set_id()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.id_producto IS NULL THEN
        NEW.id_producto := nextval('producto_id_producto_seq');
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION venta_set_id()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.id_venta IS NULL THEN
        NEW.id_venta := nextval('venta_id_venta_seq');
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_usuario_set_id
BEFORE INSERT ON usuario
FOR EACH ROW
EXECUTE FUNCTION usuario_set_id();

CREATE TRIGGER trg_categoria_set_id
BEFORE INSERT ON categoria
FOR EACH ROW
EXECUTE FUNCTION categoria_set_id();

CREATE TRIGGER trg_cliente_set_id
BEFORE INSERT ON cliente
FOR EACH ROW
EXECUTE FUNCTION cliente_set_id();

CREATE TRIGGER trg_producto_set_id
BEFORE INSERT ON producto
FOR EACH ROW
EXECUTE FUNCTION producto_set_id();

CREATE TRIGGER trg_venta_set_id
BEFORE INSERT ON venta
FOR EACH ROW
EXECUTE FUNCTION venta_set_id();

CREATE OR REPLACE VIEW vista_categorias AS
SELECT id, nombre
FROM categoria;

CREATE INDEX idx_cliente_id_usuario ON cliente (id_usuario);
CREATE INDEX idx_producto_id_categoria ON producto (id_categoria);
CREATE INDEX idx_producto_id_usuario ON producto (id_usuario);
CREATE INDEX idx_venta_id_usuario ON venta (id_usuario);
CREATE INDEX idx_venta_id_producto ON venta (id_producto);
CREATE INDEX idx_venta_id_cliente ON venta (id_cliente);