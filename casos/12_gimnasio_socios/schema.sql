PRAGMA foreign_keys = ON;

CREATE TABLE socios (
    id_socio INTEGER PRIMARY KEY,
    nombre TEXT,
    distrito TEXT,
    segmento TEXT,
    fecha_registro TEXT
);

CREATE TABLE planes (
    id_plan INTEGER PRIMARY KEY,
    nombre TEXT,
    categoria TEXT,
    tarifa_plan REAL
);

CREATE TABLE sedes (
    id_sede INTEGER PRIMARY KEY,
    nombre TEXT,
    distrito TEXT,
    zona TEXT
);

CREATE TABLE asistencias_pagos (
    id_registro INTEGER PRIMARY KEY,
    id_socio INTEGER,
    id_plan INTEGER,
    id_sede INTEGER,
    fecha_operacion TEXT,
    clases_tomadas TEXT,
    asistencias_mes TEXT,
    tarifa_plan TEXT,
    descuento_pct TEXT,
    canal TEXT,
    metodo_pago TEXT,
    calificacion TEXT,
    pago_mensual TEXT,
    observacion TEXT,
    FOREIGN KEY (id_socio) REFERENCES socios(id_socio),
    FOREIGN KEY (id_plan) REFERENCES planes(id_plan),
    FOREIGN KEY (id_sede) REFERENCES sedes(id_sede)
);
