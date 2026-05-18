PRAGMA foreign_keys = ON;

CREATE TABLE clientes (
    id_cliente INTEGER PRIMARY KEY,
    nombre TEXT,
    distrito TEXT,
    segmento TEXT,
    fecha_registro TEXT
);

CREATE TABLE articulos (
    id_articulo INTEGER PRIMARY KEY,
    nombre TEXT,
    categoria TEXT,
    precio_unitario REAL
);

CREATE TABLE tiendas (
    id_tienda INTEGER PRIMARY KEY,
    nombre TEXT,
    distrito TEXT,
    zona TEXT
);

CREATE TABLE ventas (
    id_venta INTEGER PRIMARY KEY,
    id_cliente INTEGER,
    id_articulo INTEGER,
    id_tienda INTEGER,
    fecha_operacion TEXT,
    cantidad TEXT,
    cantidad_articulos TEXT,
    precio_unitario TEXT,
    descuento_pct TEXT,
    canal TEXT,
    metodo_pago TEXT,
    calificacion TEXT,
    monto_compra TEXT,
    observacion TEXT,
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente),
    FOREIGN KEY (id_articulo) REFERENCES articulos(id_articulo),
    FOREIGN KEY (id_tienda) REFERENCES tiendas(id_tienda)
);
