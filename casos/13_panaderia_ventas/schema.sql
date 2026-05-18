PRAGMA foreign_keys = ON;

CREATE TABLE clientes (
    id_cliente INTEGER PRIMARY KEY,
    nombre TEXT,
    distrito TEXT,
    segmento TEXT,
    fecha_registro TEXT
);

CREATE TABLE productos (
    id_producto INTEGER PRIMARY KEY,
    nombre TEXT,
    categoria TEXT,
    precio_unitario REAL
);

CREATE TABLE locales (
    id_local INTEGER PRIMARY KEY,
    nombre TEXT,
    distrito TEXT,
    zona TEXT
);

CREATE TABLE ventas (
    id_venta INTEGER PRIMARY KEY,
    id_cliente INTEGER,
    id_producto INTEGER,
    id_local INTEGER,
    fecha_operacion TEXT,
    cantidad TEXT,
    cantidad_unidades TEXT,
    precio_unitario TEXT,
    descuento_pct TEXT,
    canal TEXT,
    metodo_pago TEXT,
    calificacion TEXT,
    ingreso_venta TEXT,
    observacion TEXT,
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente),
    FOREIGN KEY (id_producto) REFERENCES productos(id_producto),
    FOREIGN KEY (id_local) REFERENCES locales(id_local)
);
