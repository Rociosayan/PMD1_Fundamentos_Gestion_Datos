PRAGMA foreign_keys = ON;

CREATE TABLE huespedes (
    id_huesped INTEGER PRIMARY KEY,
    nombre TEXT,
    distrito TEXT,
    segmento TEXT,
    fecha_registro TEXT
);

CREATE TABLE habitaciones (
    id_habitacion INTEGER PRIMARY KEY,
    nombre TEXT,
    categoria TEXT,
    tarifa_noche REAL
);

CREATE TABLE hoteles (
    id_hotel INTEGER PRIMARY KEY,
    nombre TEXT,
    distrito TEXT,
    zona TEXT
);

CREATE TABLE reservas (
    id_reserva INTEGER PRIMARY KEY,
    id_huesped INTEGER,
    id_habitacion INTEGER,
    id_hotel INTEGER,
    fecha_operacion TEXT,
    cantidad_habitaciones TEXT,
    noches_estadia TEXT,
    tarifa_noche TEXT,
    descuento_pct TEXT,
    canal TEXT,
    metodo_pago TEXT,
    calificacion TEXT,
    monto_reserva TEXT,
    observacion TEXT,
    FOREIGN KEY (id_huesped) REFERENCES huespedes(id_huesped),
    FOREIGN KEY (id_habitacion) REFERENCES habitaciones(id_habitacion),
    FOREIGN KEY (id_hotel) REFERENCES hoteles(id_hotel)
);
