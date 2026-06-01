import csv
import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
CSV_DIR = BASE_DIR / "csv"
DB_PATH = BASE_DIR / "minimarket_normalizacion.db"
SCHEMA_PATH = BASE_DIR / "schema.sql"


categorias = [
    (1, "Abarrotes"),
    (2, "Bebidas"),
    (3, "Limpieza"),
    (4, "Cuidado personal"),
]

productos = [
    (1, "Arroz Costeno 5kg", 1, 28.50),
    (2, "Aceite Primor 1L", 1, 12.80),
    (3, "Fideo Don Vittorio 500g", 1, 4.20),
    (4, "Gaseosa Inca Kola 3L", 2, 10.50),
    (5, "Agua San Luis 2.5L", 2, 3.80),
    (6, "Detergente Bolivar 1kg", 3, 16.50),
    (7, "Lejia Clorox 1L", 3, 5.90),
    (8, "Jabon Protex", 4, 4.80),
]

clientes = [
    (1, "Ana Torres", "Los Olivos"),
    (2, "Luis Ramos", "Comas"),
    (3, "Maria Perez", "Independencia"),
    (4, "Carlos Rios", "San Martin"),
    (5, "Rosa Salazar", "Puente Piedra"),
    (6, "Jorge Medina", "Los Olivos"),
    (7, "Belen Castro", "Comas"),
]

locales = [
    (1, "MiniMarket Central", "Los Olivos"),
    (2, "MiniMarket Norte", "Comas"),
    (3, "MiniMarket Plaza", "Independencia"),
]

ventas = [
    (1, "2026-04-01", 1, 1, 1, 2),
    (2, "2026-04-01", 2, 4, 2, 5),
    (3, "2026-04-02", 1, 2, 1, 3),
    (4, "2026-04-02", 3, 6, 3, 1),
    (5, "2026-04-03", 2, 1, 2, 1),
    (6, "2026-04-03", 1, 5, 1, 6),
    (7, "2026-04-04", 4, 3, 3, 4),
    (8, "2026-04-04", 5, 7, 2, 2),
    (9, "2026-04-05", 6, 8, 1, 3),
    (10, "2026-04-05", 3, 4, 3, 2),
    (11, "2026-04-06", 4, 6, 2, 2),
    (12, "2026-04-06", 5, 2, 1, 1),
]


schema = """
DROP TABLE IF EXISTS ventas;
DROP TABLE IF EXISTS productos;
DROP TABLE IF EXISTS categorias;
DROP TABLE IF EXISTS clientes;
DROP TABLE IF EXISTS locales;
DROP TABLE IF EXISTS ventas_original;

CREATE TABLE ventas_original (
    id_venta INTEGER PRIMARY KEY,
    fecha TEXT NOT NULL,
    cliente TEXT NOT NULL,
    distrito_cliente TEXT NOT NULL,
    producto TEXT NOT NULL,
    categoria TEXT NOT NULL,
    local TEXT NOT NULL,
    distrito_local TEXT NOT NULL,
    cantidad INTEGER NOT NULL,
    precio_unitario REAL NOT NULL,
    total_venta REAL NOT NULL
);

CREATE TABLE categorias (
    id_categoria INTEGER PRIMARY KEY,
    nombre_categoria TEXT NOT NULL
);

CREATE TABLE productos (
    id_producto INTEGER PRIMARY KEY,
    nombre_producto TEXT NOT NULL,
    id_categoria INTEGER NOT NULL,
    precio_unitario REAL NOT NULL,
    FOREIGN KEY (id_categoria) REFERENCES categorias(id_categoria)
);

CREATE TABLE clientes (
    id_cliente INTEGER PRIMARY KEY,
    nombre_cliente TEXT NOT NULL,
    distrito_cliente TEXT NOT NULL
);

CREATE TABLE locales (
    id_local INTEGER PRIMARY KEY,
    nombre_local TEXT NOT NULL,
    distrito_local TEXT NOT NULL
);

CREATE TABLE ventas (
    id_venta INTEGER PRIMARY KEY,
    fecha TEXT NOT NULL,
    id_cliente INTEGER NOT NULL,
    id_producto INTEGER NOT NULL,
    id_local INTEGER NOT NULL,
    cantidad INTEGER NOT NULL,
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente),
    FOREIGN KEY (id_producto) REFERENCES productos(id_producto),
    FOREIGN KEY (id_local) REFERENCES locales(id_local)
);
""".strip()


def write_csv(name, headers, rows):
    path = CSV_DIR / name
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)


def main():
    CSV_DIR.mkdir(parents=True, exist_ok=True)
    if DB_PATH.exists():
        DB_PATH.unlink()

    conn = sqlite3.connect(DB_PATH)
    conn.executescript(schema)

    conn.executemany("INSERT INTO categorias VALUES (?, ?)", categorias)
    conn.executemany("INSERT INTO productos VALUES (?, ?, ?, ?)", productos)
    conn.executemany("INSERT INTO clientes VALUES (?, ?, ?)", clientes)
    conn.executemany("INSERT INTO locales VALUES (?, ?, ?)", locales)
    conn.executemany("INSERT INTO ventas VALUES (?, ?, ?, ?, ?, ?)", ventas)

    productos_map = {row[0]: row for row in productos}
    categorias_map = {row[0]: row for row in categorias}
    clientes_map = {row[0]: row for row in clientes}
    locales_map = {row[0]: row for row in locales}

    ventas_original = []
    for id_venta, fecha, id_cliente, id_producto, id_local, cantidad in ventas:
        _, nombre_cliente, distrito_cliente = clientes_map[id_cliente]
        _, nombre_producto, id_categoria, precio = productos_map[id_producto]
        _, nombre_categoria = categorias_map[id_categoria]
        _, nombre_local, distrito_local = locales_map[id_local]
        ventas_original.append(
            (
                id_venta,
                fecha,
                nombre_cliente,
                distrito_cliente,
                nombre_producto,
                nombre_categoria,
                nombre_local,
                distrito_local,
                cantidad,
                precio,
                round(cantidad * precio, 2),
            )
        )

    conn.executemany(
        "INSERT INTO ventas_original VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        ventas_original,
    )
    conn.commit()
    conn.close()

    SCHEMA_PATH.write_text(schema + "\n", encoding="utf-8")
    write_csv("categorias.csv", ["id_categoria", "nombre_categoria"], categorias)
    write_csv(
        "productos.csv",
        ["id_producto", "nombre_producto", "id_categoria", "precio_unitario"],
        productos,
    )
    write_csv(
        "clientes.csv",
        ["id_cliente", "nombre_cliente", "distrito_cliente"],
        clientes,
    )
    write_csv("locales.csv", ["id_local", "nombre_local", "distrito_local"], locales)
    write_csv(
        "ventas.csv",
        ["id_venta", "fecha", "id_cliente", "id_producto", "id_local", "cantidad"],
        ventas,
    )
    write_csv(
        "ventas_original.csv",
        [
            "id_venta",
            "fecha",
            "cliente",
            "distrito_cliente",
            "producto",
            "categoria",
            "local",
            "distrito_local",
            "cantidad",
            "precio_unitario",
            "total_venta",
        ],
        ventas_original,
    )

    print(f"Base creada: {DB_PATH}")


if __name__ == "__main__":
    main()
