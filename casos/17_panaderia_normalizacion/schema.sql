PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS ventas_original;
DROP TABLE IF EXISTS ventas;
DROP TABLE IF EXISTS productos;
DROP TABLE IF EXISTS categorias;
DROP TABLE IF EXISTS clientes;
DROP TABLE IF EXISTS locales;

CREATE TABLE ventas_original (
    id_venta INTEGER PRIMARY KEY,
    fecha TEXT NOT NULL,
    cliente_nombre TEXT NOT NULL,
    cliente_distrito TEXT NOT NULL,
    producto_nombre TEXT NOT NULL,
    categoria_nombre TEXT NOT NULL,
    local_nombre TEXT NOT NULL,
    local_distrito TEXT NOT NULL,
    cantidad INTEGER NOT NULL,
    precio_unitario REAL NOT NULL,
    metodo_pago TEXT NOT NULL,
    total_venta REAL NOT NULL
);

CREATE TABLE categorias (
    id_categoria INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL UNIQUE
);

CREATE TABLE productos (
    id_producto INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL,
    id_categoria INTEGER NOT NULL,
    precio_unitario REAL NOT NULL,
    FOREIGN KEY (id_categoria) REFERENCES categorias(id_categoria)
);

CREATE TABLE clientes (
    id_cliente INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL,
    distrito TEXT NOT NULL
);

CREATE TABLE locales (
    id_local INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL,
    distrito TEXT NOT NULL
);

CREATE TABLE ventas (
    id_venta INTEGER PRIMARY KEY,
    fecha TEXT NOT NULL,
    id_cliente INTEGER NOT NULL,
    id_producto INTEGER NOT NULL,
    id_local INTEGER NOT NULL,
    cantidad INTEGER NOT NULL,
    metodo_pago TEXT NOT NULL,
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente),
    FOREIGN KEY (id_producto) REFERENCES productos(id_producto),
    FOREIGN KEY (id_local) REFERENCES locales(id_local)
);
