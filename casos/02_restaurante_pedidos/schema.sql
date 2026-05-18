PRAGMA foreign_keys = ON;

CREATE TABLE clientes (
    id_cliente INTEGER PRIMARY KEY,
    nombre TEXT,
    distrito TEXT,
    segmento TEXT,
    fecha_registro TEXT
);

CREATE TABLE platos (
    id_plato INTEGER PRIMARY KEY,
    nombre TEXT,
    categoria TEXT,
    precio_plato REAL
);

CREATE TABLE locales (
    id_local INTEGER PRIMARY KEY,
    nombre TEXT,
    distrito TEXT,
    zona TEXT
);

CREATE TABLE pedidos (
    id_pedido INTEGER PRIMARY KEY,
    id_cliente INTEGER,
    id_plato INTEGER,
    id_local INTEGER,
    fecha_operacion TEXT,
    cantidad_platos TEXT,
    tiempo_preparacion_min TEXT,
    precio_plato TEXT,
    descuento_pct TEXT,
    canal TEXT,
    metodo_pago TEXT,
    calificacion TEXT,
    total_pedido TEXT,
    observacion TEXT,
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente),
    FOREIGN KEY (id_plato) REFERENCES platos(id_plato),
    FOREIGN KEY (id_local) REFERENCES locales(id_local)
);
