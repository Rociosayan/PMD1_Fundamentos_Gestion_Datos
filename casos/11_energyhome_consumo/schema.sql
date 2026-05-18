PRAGMA foreign_keys = ON;

CREATE TABLE hogares (
    id_hogar INTEGER PRIMARY KEY,
    nombre TEXT,
    distrito TEXT,
    segmento TEXT,
    fecha_registro TEXT
);

CREATE TABLE tarifas (
    id_tarifa INTEGER PRIMARY KEY,
    nombre TEXT,
    categoria TEXT,
    tarifa_base REAL
);

CREATE TABLE distritos (
    id_distrito INTEGER PRIMARY KEY,
    nombre TEXT,
    distrito TEXT,
    zona TEXT
);

CREATE TABLE consumos (
    id_consumo INTEGER PRIMARY KEY,
    id_hogar INTEGER,
    id_tarifa INTEGER,
    id_distrito INTEGER,
    fecha_operacion TEXT,
    electrodomesticos TEXT,
    numero_habitantes TEXT,
    tarifa_base TEXT,
    descuento_pct TEXT,
    canal TEXT,
    metodo_pago TEXT,
    calificacion TEXT,
    consumo_kwh TEXT,
    observacion TEXT,
    FOREIGN KEY (id_hogar) REFERENCES hogares(id_hogar),
    FOREIGN KEY (id_tarifa) REFERENCES tarifas(id_tarifa),
    FOREIGN KEY (id_distrito) REFERENCES distritos(id_distrito)
);
