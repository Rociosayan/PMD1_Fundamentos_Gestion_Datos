import csv
import random
import shutil
import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
CSV_DIR = BASE_DIR / "csv"
DB_PATH = BASE_DIR / "industria_paradas_procesos.db"
SCHEMA_PATH = BASE_DIR / "schema.sql"
N_ROWS = 500
SEED = 202615


MAQUINAS = [
    ("Mezcladora 01", "Linea A", "Mezclado", 4.5),
    ("Prensa 02", "Linea A", "Prensado", 7.0),
    ("Cortadora 03", "Linea B", "Corte", 5.2),
    ("Empacadora 04", "Linea B", "Empaque", 3.8),
    ("Horno 05", "Linea C", "Termico", 9.5),
    ("Etiquetadora 06", "Linea C", "Etiquetado", 2.4),
    ("Llenadora 07", "Linea D", "Llenado", 6.1),
    ("Selladora 08", "Linea D", "Sellado", 8.3),
]

PROCESOS = [
    ("Preparacion de insumo", "Preparacion", 45.0, 520.0),
    ("Moldeado inicial", "Transformacion", 70.0, 410.0),
    ("Corte de piezas", "Transformacion", 38.0, 620.0),
    ("Tratamiento termico", "Termico", 155.0, 260.0),
    ("Enfriamiento controlado", "Termico", 30.0, 300.0),
    ("Empaque primario", "Empaque", 24.0, 720.0),
    ("Etiquetado final", "Empaque", 24.0, 880.0),
    ("Control de calidad", "Calidad", 23.0, 350.0),
]

TURNOS = [
    ("Manana", "Ana Torres", "06:00", "14:00"),
    ("Tarde", "Luis Ramos", "14:00", "22:00"),
    ("Noche", "Diana Flores", "22:00", "06:00"),
]

CAUSAS = [
    "Falla mecanica",
    "Cambio de formato",
    "Falta de insumo",
    "Mantenimiento correctivo",
    "Ajuste de calidad",
    "Falla electrica",
    "Limpieza no programada",
    "Espera de operador",
]

CRITICIDADES = ["Baja", "Media", "Alta", "Critica"]


def dirty_text(value, rng, p=0.16):
    if rng.random() < 0.03:
        return None
    if rng.random() >= p:
        return value
    option = rng.choice(["upper", "lower", "spaces", "mixed", "double_space"])
    if option == "upper":
        return value.upper()
    if option == "lower":
        return value.lower()
    if option == "spaces":
        return f"  {value} "
    if option == "mixed":
        return "".join(ch.upper() if i % 2 == 0 else ch.lower() for i, ch in enumerate(value))
    return value.replace(" ", "  ")


def dirty_number(value, rng, money=False, p=0.13):
    if rng.random() < 0.025:
        return None
    if rng.random() >= p:
        return round(value, 2)
    option = rng.choice(["spaces", "comma", "text", "currency"] if money else ["spaces", "comma", "text"])
    rounded = round(value, 2)
    if option == "spaces":
        return f" {rounded} "
    if option == "comma":
        return str(rounded).replace(".", ",")
    if option == "currency":
        return f"S/ {rounded}"
    return f"{rounded} aprox"


def dirty_date(year, month, day, rng):
    if rng.random() < 0.025:
        return None
    if rng.random() < 0.14:
        return rng.choice([
            f"{day:02d}/{month:02d}/{year}",
            f"{year}/{month:02d}/{day:02d}",
            f"{day:02d}-{month:02d}-{year}",
            f" {year}-{month:02d}-{day:02d} ",
        ])
    return f"{year}-{month:02d}-{day:02d}"


def write_csv(path, columns, rows):
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def insert_rows(conn, table, columns, rows):
    placeholders = ", ".join(["?"] * len(columns))
    col_sql = ", ".join(columns)
    sql = f"INSERT INTO {table} ({col_sql}) VALUES ({placeholders})"
    conn.executemany(sql, [[row.get(col) for col in columns] for row in rows])


def main():
    rng = random.Random(SEED)
    if CSV_DIR.exists():
        shutil.rmtree(CSV_DIR)
    CSV_DIR.mkdir(parents=True, exist_ok=True)
    if DB_PATH.exists():
        DB_PATH.unlink()

    schema = SCHEMA_PATH.read_text(encoding="utf-8")
    conn = sqlite3.connect(DB_PATH)
    conn.executescript(schema)

    maquina_rows = [
        {
            "id_maquina": i,
            "nombre": dirty_text(nombre, rng, 0.12),
            "linea": dirty_text(linea, rng, 0.20),
            "tipo_maquina": dirty_text(tipo, rng, 0.18),
            "antiguedad_anios": round(antiguedad * rng.uniform(0.92, 1.08), 2),
        }
        for i, (nombre, linea, tipo, antiguedad) in enumerate(MAQUINAS, start=1)
    ]
    proceso_rows = [
        {
            "id_proceso": i,
            "nombre": dirty_text(nombre, rng, 0.12),
            "familia": dirty_text(familia, rng, 0.18),
            "temperatura_objetivo_c": temp,
            "velocidad_objetivo_u_h": velocidad,
        }
        for i, (nombre, familia, temp, velocidad) in enumerate(PROCESOS, start=1)
    ]
    turno_rows = [
        {
            "id_turno": i,
            "nombre": dirty_text(nombre, rng, 0.10),
            "supervisor": dirty_text(supervisor, rng, 0.12),
            "hora_inicio": inicio,
            "hora_fin": fin,
        }
        for i, (nombre, supervisor, inicio, fin) in enumerate(TURNOS, start=1)
    ]

    insert_rows(conn, "maquinas", ["id_maquina", "nombre", "linea", "tipo_maquina", "antiguedad_anios"], maquina_rows)
    insert_rows(conn, "procesos", ["id_proceso", "nombre", "familia", "temperatura_objetivo_c", "velocidad_objetivo_u_h"], proceso_rows)
    insert_rows(conn, "turnos", ["id_turno", "nombre", "supervisor", "hora_inicio", "hora_fin"], turno_rows)

    parada_rows = []
    duplicate_pool = []
    for i in range(1, N_ROWS + 1):
        if duplicate_pool and rng.random() < 0.035:
            row = rng.choice(duplicate_pool).copy()
            row["id_parada"] = i
            parada_rows.append(row)
            continue

        maquina = maquina_rows[rng.randrange(len(maquina_rows))]
        proceso = proceso_rows[rng.randrange(len(proceso_rows))]
        turno = turno_rows[rng.randrange(len(turno_rows))]
        tiempo_operacion = rng.uniform(2.0, 11.5)
        temp_desvio = rng.gauss(0, 5.5)
        velocidad_objetivo = proceso["velocidad_objetivo_u_h"]
        velocidad_real = max(80.0, velocidad_objetivo * rng.uniform(0.70, 1.08))
        unidades = max(20, int(tiempo_operacion * velocidad_real * rng.uniform(0.65, 0.98)))
        defectos = max(0, int(rng.gauss(8, 5) + abs(temp_desvio) * 1.7 + maquina["antiguedad_anios"] * 0.7))
        causa = rng.choice(CAUSAS)
        criticidad = rng.choices(CRITICIDADES, weights=[0.30, 0.40, 0.22, 0.08])[0]
        causa_factor = {
            "Falla mecanica": 18,
            "Cambio de formato": 9,
            "Falta de insumo": 12,
            "Mantenimiento correctivo": 24,
            "Ajuste de calidad": 14,
            "Falla electrica": 20,
            "Limpieza no programada": 10,
            "Espera de operador": 7,
        }[causa]
        criticidad_factor = {"Baja": 0, "Media": 8, "Alta": 18, "Critica": 34}[criticidad]
        duracion = (
            6
            + causa_factor
            + criticidad_factor
            + maquina["antiguedad_anios"] * 1.8
            + defectos * 0.35
            + max(0, -temp_desvio) * 0.7
            + rng.gauss(0, 7.5)
        )
        if rng.random() < 0.018:
            duracion *= rng.uniform(2.2, 3.5)
        duracion = max(3.0, duracion)
        costo = 110 + duracion * rng.uniform(18, 32) + defectos * 4.5 + rng.gauss(0, 75)
        if criticidad == "Critica":
            costo *= rng.uniform(1.20, 1.55)
        costo = max(50.0, costo)

        row = {
            "id_parada": i,
            "id_maquina": maquina["id_maquina"],
            "id_proceso": proceso["id_proceso"],
            "id_turno": turno["id_turno"],
            "fecha_operacion": dirty_date(2026, rng.randint(1, 6), rng.randint(1, 28), rng),
            "tiempo_operacion_h": dirty_number(tiempo_operacion, rng, False, 0.13),
            "unidades_producidas": dirty_number(unidades, rng, False, 0.10),
            "defectos_unidades": dirty_number(defectos, rng, False, 0.12),
            "temperatura_promedio_c": dirty_number(proceso["temperatura_objetivo_c"] + temp_desvio, rng, False, 0.14),
            "velocidad_real_u_h": dirty_number(velocidad_real, rng, False, 0.12),
            "causa_parada": dirty_text(causa, rng, 0.22),
            "criticidad": dirty_text(criticidad, rng, 0.20),
            "duracion_parada_min": dirty_number(duracion, rng, False, 0.15),
            "costo_parada_soles": dirty_number(costo, rng, True, 0.13),
            "observacion": dirty_text(rng.choice(["OK", "Revisar sensor", "Validar causa", "Atencion mantenimiento", ""]), rng, 0.14),
        }
        if rng.random() < 0.08:
            row["observacion"] = None
        parada_rows.append(row)
        if rng.random() < 0.18:
            duplicate_pool.append(row.copy())

    parada_columns = [
        "id_parada",
        "id_maquina",
        "id_proceso",
        "id_turno",
        "fecha_operacion",
        "tiempo_operacion_h",
        "unidades_producidas",
        "defectos_unidades",
        "temperatura_promedio_c",
        "velocidad_real_u_h",
        "causa_parada",
        "criticidad",
        "duracion_parada_min",
        "costo_parada_soles",
        "observacion",
    ]
    insert_rows(conn, "paradas", parada_columns, parada_rows)
    conn.commit()
    conn.close()

    write_csv(CSV_DIR / "maquinas.csv", ["id_maquina", "nombre", "linea", "tipo_maquina", "antiguedad_anios"], maquina_rows)
    write_csv(CSV_DIR / "procesos.csv", ["id_proceso", "nombre", "familia", "temperatura_objetivo_c", "velocidad_objetivo_u_h"], proceso_rows)
    write_csv(CSV_DIR / "turnos.csv", ["id_turno", "nombre", "supervisor", "hora_inicio", "hora_fin"], turno_rows)
    write_csv(CSV_DIR / "paradas.csv", parada_columns, parada_rows)

    print(f"Generado {DB_PATH.name} con {len(parada_rows)} paradas.")


if __name__ == "__main__":
    main()
