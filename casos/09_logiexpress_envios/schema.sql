PRAGMA foreign_keys = ON;

CREATE TABLE clientes (
    id_cliente INTEGER PRIMARY KEY,
    nombre TEXT,
    distrito TEXT,
    segmento TEXT,
    fecha_registro TEXT
);

CREATE TABLE tipos_envio (
    id_tipo_envio INTEGER PRIMARY KEY,
    nombre TEXT,
    categoria TEXT,
    tarifa_base REAL
);

CREATE TABLE sedes (
    id_sede INTEGER PRIMARY KEY,
    nombre TEXT,
    distrito TEXT,
    zona TEXT
);

CREATE TABLE envios (
    id_envio INTEGER PRIMARY KEY,
    id_cliente INTEGER,
    id_tipo_envio INTEGER,
    id_sede INTEGER,
    fecha_operacion TEXT,
    cantidad_paquetes TEXT,
    peso_paquete_kg TEXT,
    tarifa_base TEXT,
    descuento_pct TEXT,
    canal TEXT,
    metodo_pago TEXT,
    calificacion TEXT,
    costo_envio TEXT,
    observacion TEXT,
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente),
    FOREIGN KEY (id_tipo_envio) REFERENCES tipos_envio(id_tipo_envio),
    FOREIGN KEY (id_sede) REFERENCES sedes(id_sede)
);
