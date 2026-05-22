PRAGMA foreign_keys = ON;

CREATE TABLE maquinas (
    id_maquina INTEGER PRIMARY KEY,
    nombre TEXT,
    linea TEXT,
    tipo_maquina TEXT,
    antiguedad_anios REAL
);

CREATE TABLE procesos (
    id_proceso INTEGER PRIMARY KEY,
    nombre TEXT,
    familia TEXT,
    temperatura_objetivo_c REAL,
    velocidad_objetivo_u_h REAL
);

CREATE TABLE turnos (
    id_turno INTEGER PRIMARY KEY,
    nombre TEXT,
    supervisor TEXT,
    hora_inicio TEXT,
    hora_fin TEXT
);

CREATE TABLE paradas (
    id_parada INTEGER PRIMARY KEY,
    id_maquina INTEGER,
    id_proceso INTEGER,
    id_turno INTEGER,
    fecha_operacion TEXT,
    tiempo_operacion_h TEXT,
    unidades_producidas TEXT,
    defectos_unidades TEXT,
    temperatura_promedio_c TEXT,
    velocidad_real_u_h TEXT,
    causa_parada TEXT,
    criticidad TEXT,
    duracion_parada_min TEXT,
    costo_parada_soles TEXT,
    observacion TEXT,
    FOREIGN KEY (id_maquina) REFERENCES maquinas(id_maquina),
    FOREIGN KEY (id_proceso) REFERENCES procesos(id_proceso),
    FOREIGN KEY (id_turno) REFERENCES turnos(id_turno)
);
