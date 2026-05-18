PRAGMA foreign_keys = ON;

CREATE TABLE clientes (
    id_cliente INTEGER PRIMARY KEY,
    nombre TEXT,
    distrito TEXT,
    segmento TEXT,
    fecha_registro TEXT
);

CREATE TABLE medicamentos (
    id_medicamento INTEGER PRIMARY KEY,
    nombre TEXT,
    categoria TEXT,
    precio_unitario REAL
);

CREATE TABLE sucursales (
    id_sucursal INTEGER PRIMARY KEY,
    nombre TEXT,
    distrito TEXT,
    zona TEXT
);

CREATE TABLE ventas (
    id_venta INTEGER PRIMARY KEY,
    id_cliente INTEGER,
    id_medicamento INTEGER,
    id_sucursal INTEGER,
    fecha_operacion TEXT,
    cantidad TEXT,
    cantidad_medicamentos TEXT,
    precio_unitario TEXT,
    descuento_pct TEXT,
    canal TEXT,
    metodo_pago TEXT,
    calificacion TEXT,
    monto_boleta TEXT,
    observacion TEXT,
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente),
    FOREIGN KEY (id_medicamento) REFERENCES medicamentos(id_medicamento),
    FOREIGN KEY (id_sucursal) REFERENCES sucursales(id_sucursal)
);
