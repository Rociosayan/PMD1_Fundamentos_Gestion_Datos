from pathlib import Path
import csv
import sqlite3


BASE_DIR = Path(__file__).resolve().parent
CSV_DIR = BASE_DIR / "csv"
DB_PATH = BASE_DIR / "panaderia_normalizacion.db"
SCHEMA_PATH = BASE_DIR / "schema.sql"


categorias = [
    (1, "Panes"),
    (2, "Pasteles"),
    (3, "Bebidas"),
    (4, "Salados"),
]

productos = [
    (1, "Pan frances", 1, 0.50),
    (2, "Pan integral", 1, 0.80),
    (3, "Empanada de pollo", 4, 4.50),
    (4, "Torta de chocolate", 2, 8.00),
    (5, "Jugo de naranja", 3, 5.00),
    (6, "Cafe americano", 3, 4.00),
]

clientes = [
    (1, "Ana Torres", "Los Olivos"),
    (2, "Luis Ramos", "Comas"),
    (3, "Maria Perez", "Independencia"),
    (4, "Carlos Rios", "San Martin de Porres"),
    (5, "Rosa Diaz", "Los Olivos"),
    (6, "Jorge Salas", "Comas"),
]

locales = [
    (1, "Panaderia Central", "Los Olivos"),
    (2, "Panaderia Norte", "Comas"),
    (3, "Panaderia Plaza", "Independencia"),
]

ventas = [
    (1, "2026-04-01", 1, 1, 1, 20, "Efectivo"),
    (2, "2026-04-01", 2, 3, 2, 4, "Yape"),
    (3, "2026-04-01", 3, 5, 3, 2, "Tarjeta"),
    (4, "2026-04-02", 1, 4, 1, 1, "Tarjeta"),
    (5, "2026-04-02", 4, 2, 2, 12, "Efectivo"),
    (6, "2026-04-02", 5, 6, 1, 3, "Yape"),
    (7, "2026-04-03", 2, 1, 2, 15, "Efectivo"),
    (8, "2026-04-03", 6, 3, 3, 2, "Yape"),
    (9, "2026-04-03", 3, 4, 3, 2, "Tarjeta"),
    (10, "2026-04-04", 4, 5, 2, 4, "Yape"),
    (11, "2026-04-04", 5, 1, 1, 25, "Efectivo"),
    (12, "2026-04-04", 6, 2, 3, 10, "Tarjeta"),
    (13, "2026-04-05", 1, 3, 1, 3, "Efectivo"),
    (14, "2026-04-05", 2, 6, 2, 2, "Yape"),
    (15, "2026-04-05", 3, 1, 3, 18, "Efectivo"),
    (16, "2026-04-06", 4, 4, 2, 1, "Tarjeta"),
    (17, "2026-04-06", 5, 5, 1, 2, "Yape"),
    (18, "2026-04-06", 6, 3, 3, 4, "Efectivo"),
]


def dict_by_id(rows):
    return {row[0]: row for row in rows}


cat_by_id = dict_by_id(categorias)
prod_by_id = dict_by_id(productos)
cli_by_id = dict_by_id(clientes)
loc_by_id = dict_by_id(locales)


ventas_original = []
for id_venta, fecha, id_cliente, id_producto, id_local, cantidad, metodo_pago in ventas:
    producto = prod_by_id[id_producto]
    categoria = cat_by_id[producto[2]]
    cliente = cli_by_id[id_cliente]
    local = loc_by_id[id_local]
    precio = producto[3]
    total = round(cantidad * precio, 2)
    ventas_original.append(
        (
            id_venta,
            fecha,
            cliente[1],
            cliente[2],
            producto[1],
            categoria[1],
            local[1],
            local[2],
            cantidad,
            precio,
            metodo_pago,
            total,
        )
    )


schema = """
PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS ventas_original;
DROP TABLE IF EXISTS ventas;
DROP TABLE IF EXISTS productos;
DROP TABLE IF EXISTS categorias;
DROP TABLE IF EXISTS clientes;
DROP TABLE IF EXISTS locales;

CREATE TABLE ventas_original (
    id_venta INTEGER PRIMARY KEY,
    fecha TEXT NOT NULL,
    cliente_nombre TEXT NOT NULL,
    cliente_distrito TEXT NOT NULL,
    producto_nombre TEXT NOT NULL,
    categoria_nombre TEXT NOT NULL,
    local_nombre TEXT NOT NULL,
    local_distrito TEXT NOT NULL,
    cantidad INTEGER NOT NULL,
    precio_unitario REAL NOT NULL,
    metodo_pago TEXT NOT NULL,
    total_venta REAL NOT NULL
);

CREATE TABLE categorias (
    id_categoria INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL UNIQUE
);

CREATE TABLE productos (
    id_producto INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL,
    id_categoria INTEGER NOT NULL,
    precio_unitario REAL NOT NULL,
    FOREIGN KEY (id_categoria) REFERENCES categorias(id_categoria)
);

CREATE TABLE clientes (
    id_cliente INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL,
    distrito TEXT NOT NULL
);

CREATE TABLE locales (
    id_local INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL,
    distrito TEXT NOT NULL
);

CREATE TABLE ventas (
    id_venta INTEGER PRIMARY KEY,
    fecha TEXT NOT NULL,
    id_cliente INTEGER NOT NULL,
    id_producto INTEGER NOT NULL,
    id_local INTEGER NOT NULL,
    cantidad INTEGER NOT NULL,
    metodo_pago TEXT NOT NULL,
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente),
    FOREIGN KEY (id_producto) REFERENCES productos(id_producto),
    FOREIGN KEY (id_local) REFERENCES locales(id_local)
);
"""


def write_csv(name, header, rows):
    path = CSV_DIR / name
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)


def main():
    CSV_DIR.mkdir(parents=True, exist_ok=True)
    if DB_PATH.exists():
        DB_PATH.unlink()

    SCHEMA_PATH.write_text(schema.strip() + "\n", encoding="utf-8")

    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.executescript(schema)

    conn.executemany("INSERT INTO categorias VALUES (?, ?);", categorias)
    conn.executemany("INSERT INTO productos VALUES (?, ?, ?, ?);", productos)
    conn.executemany("INSERT INTO clientes VALUES (?, ?, ?);", clientes)
    conn.executemany("INSERT INTO locales VALUES (?, ?, ?);", locales)
    conn.executemany("INSERT INTO ventas VALUES (?, ?, ?, ?, ?, ?, ?);", ventas)
    conn.executemany(
        "INSERT INTO ventas_original VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);",
        ventas_original,
    )
    conn.commit()
    conn.close()

    write_csv(
        "ventas_original.csv",
        [
            "id_venta",
            "fecha",
            "cliente_nombre",
            "cliente_distrito",
            "producto_nombre",
            "categoria_nombre",
            "local_nombre",
            "local_distrito",
            "cantidad",
            "precio_unitario",
            "metodo_pago",
            "total_venta",
        ],
        ventas_original,
    )
    write_csv("categorias.csv", ["id_categoria", "nombre"], categorias)
    write_csv("productos.csv", ["id_producto", "nombre", "id_categoria", "precio_unitario"], productos)
    write_csv("clientes.csv", ["id_cliente", "nombre", "distrito"], clientes)
    write_csv("locales.csv", ["id_local", "nombre", "distrito"], locales)
    write_csv("ventas.csv", ["id_venta", "fecha", "id_cliente", "id_producto", "id_local", "cantidad", "metodo_pago"], ventas)

    print(DB_PATH)


if __name__ == "__main__":
    main()
