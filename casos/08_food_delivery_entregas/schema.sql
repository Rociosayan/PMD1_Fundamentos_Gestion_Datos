PRAGMA foreign_keys = ON;

CREATE TABLE clientes (
    id_cliente INTEGER PRIMARY KEY,
    nombre TEXT,
    distrito TEXT,
    segmento TEXT,
    fecha_registro TEXT
);

CREATE TABLE restaurantes (
    id_restaurante INTEGER PRIMARY KEY,
    nombre TEXT,
    categoria TEXT,
    costo_pedido REAL
);

CREATE TABLE zonas (
    id_zona INTEGER PRIMARY KEY,
    nombre TEXT,
    distrito TEXT,
    zona TEXT
);

CREATE TABLE entregas (
    id_entrega INTEGER PRIMARY KEY,
    id_cliente INTEGER,
    id_restaurante INTEGER,
    id_zona INTEGER,
    fecha_operacion TEXT,
    cantidad_items TEXT,
    distancia_km TEXT,
    costo_pedido TEXT,
    descuento_pct TEXT,
    canal TEXT,
    metodo_pago TEXT,
    calificacion TEXT,
    tiempo_entrega_min TEXT,
    observacion TEXT,
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente),
    FOREIGN KEY (id_restaurante) REFERENCES restaurantes(id_restaurante),
    FOREIGN KEY (id_zona) REFERENCES zonas(id_zona)
);
