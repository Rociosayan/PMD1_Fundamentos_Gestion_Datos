PRAGMA foreign_keys = ON;

CREATE TABLE clientes (
    id_cliente INTEGER PRIMARY KEY,
    nombre TEXT,
    distrito TEXT,
    segmento TEXT,
    fecha_registro TEXT
);

CREATE TABLE servicios (
    id_servicio INTEGER PRIMARY KEY,
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

CREATE TABLE ordenes (
    id_orden INTEGER PRIMARY KEY,
    id_cliente INTEGER,
    id_servicio INTEGER,
    id_sede INTEGER,
    fecha_operacion TEXT,
    cantidad_repuestos TEXT,
    horas_trabajo TEXT,
    tarifa_base TEXT,
    descuento_pct TEXT,
    canal TEXT,
    metodo_pago TEXT,
    calificacion TEXT,
    costo_reparacion TEXT,
    observacion TEXT,
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente),
    FOREIGN KEY (id_servicio) REFERENCES servicios(id_servicio),
    FOREIGN KEY (id_sede) REFERENCES sedes(id_sede)
);
