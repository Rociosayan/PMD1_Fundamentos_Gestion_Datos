PRAGMA foreign_keys = ON;

CREATE TABLE parcelas (
    id_parcela INTEGER PRIMARY KEY,
    nombre TEXT,
    distrito TEXT,
    segmento TEXT,
    fecha_registro TEXT
);

CREATE TABLE cultivos (
    id_cultivo INTEGER PRIMARY KEY,
    nombre TEXT,
    categoria TEXT,
    costo_insumo REAL
);

CREATE TABLE zonas (
    id_zona INTEGER PRIMARY KEY,
    nombre TEXT,
    distrito TEXT,
    zona TEXT
);

CREATE TABLE produccion (
    id_produccion INTEGER PRIMARY KEY,
    id_parcela INTEGER,
    id_cultivo INTEGER,
    id_zona INTEGER,
    fecha_operacion TEXT,
    cantidad_jornales TEXT,
    hectareas TEXT,
    costo_insumo TEXT,
    descuento_pct TEXT,
    canal TEXT,
    metodo_pago TEXT,
    calificacion TEXT,
    rendimiento_kg TEXT,
    observacion TEXT,
    FOREIGN KEY (id_parcela) REFERENCES parcelas(id_parcela),
    FOREIGN KEY (id_cultivo) REFERENCES cultivos(id_cultivo),
    FOREIGN KEY (id_zona) REFERENCES zonas(id_zona)
);
