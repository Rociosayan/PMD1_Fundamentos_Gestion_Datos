PRAGMA foreign_keys = ON;

CREATE TABLE mascotas (
    id_mascota INTEGER PRIMARY KEY,
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

CREATE TABLE atenciones (
    id_atencion INTEGER PRIMARY KEY,
    id_mascota INTEGER,
    id_servicio INTEGER,
    id_sede INTEGER,
    fecha_operacion TEXT,
    cantidad_servicios TEXT,
    peso_mascota_kg TEXT,
    tarifa_base TEXT,
    descuento_pct TEXT,
    canal TEXT,
    metodo_pago TEXT,
    calificacion TEXT,
    costo_servicio TEXT,
    observacion TEXT,
    FOREIGN KEY (id_mascota) REFERENCES mascotas(id_mascota),
    FOREIGN KEY (id_servicio) REFERENCES servicios(id_servicio),
    FOREIGN KEY (id_sede) REFERENCES sedes(id_sede)
);
