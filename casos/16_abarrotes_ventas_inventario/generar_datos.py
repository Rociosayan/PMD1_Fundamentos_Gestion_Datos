import csv
import random
import shutil
import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
CSV_DIR = BASE_DIR / "csv"
DB_PATH = BASE_DIR / "abarrotes_ventas_inventario.db"
SCHEMA_PATH = BASE_DIR / "schema.sql"
N_ROWS = 500
SEED = 202616


FIRST_NAMES = [
    "Ana", "Luis", "Maria", "Carlos", "Rocio", "Diego", "Lucia", "Jorge",
    "Valeria", "Miguel", "Camila", "Pedro", "Diana", "Jose", "Elena",
    "Raul", "Fiorella", "Marco", "Sofia", "Andre", "Claudia", "Victor",
]

LAST_NAMES = [
    "Sayan", "Quispe", "Ramos", "Torres", "Flores", "Salazar", "Gomez",
    "Vargas", "Castillo", "Mendoza", "Huaman", "Rojas", "Navarro",
    "Paredes", "Soto", "Cruz", "Reyes", "Campos",
]

DISTRICTS = [
    "Lima", "San Juan de Lurigancho", "Ate", "Comas", "Los Olivos",
    "San Miguel", "Miraflores", "Surco", "Callao", "Ventanilla",
    "Chorrillos", "La Molina", "Independencia", "Villa El Salvador",
]

PRODUCTOS = [
    ("Arroz extra 5kg", "Granos", "Molino Norte", 18.5, 24.9),
    ("Azucar rubia 1kg", "Endulzantes", "Dulce Peru", 3.2, 4.7),
    ("Aceite vegetal 1L", "Aceites", "Oleo Andino", 7.8, 11.5),
    ("Fideos spaghetti", "Pastas", "Pastas Sol", 2.1, 3.6),
    ("Leche evaporada", "Lacteos", "Lacteos Lima", 3.2, 4.9),
    ("Atun en lata", "Conservas", "Mar Azul", 4.1, 6.8),
    ("Cafe instantaneo", "Bebidas", "Cafe Sierra", 9.8, 14.9),
    ("Galletas soda", "Snacks", "Dulcesur", 1.7, 2.8),
    ("Detergente bolsa", "Limpieza", "Casa Limpia", 6.5, 9.9),
    ("Papel higienico", "Limpieza", "Suave Hogar", 5.6, 8.5),
    ("Yogurt familiar", "Lacteos", "Lacteos Lima", 4.4, 6.7),
    ("Lenteja 500g", "Menestras", "Campo Bueno", 3.4, 5.2),
]

CHANNELS = ["Mostrador", "WhatsApp", "Delivery local", "Telefono"]
PAYMENT_METHODS = ["Efectivo", "Tarjeta", "Yape", "Plin", "Transferencia"]
SEGMENTS = ["Ocasional", "Vecino frecuente", "Mayorista pequeno", "Familia", "Negocio"]
STORE_TYPES = ["Bodega", "Minimarket", "Tienda de mercado", "Almacen"]


def person_name(rng):
    return f"{rng.choice(FIRST_NAMES)} {rng.choice(LAST_NAMES)}"


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
    if rng.random() < 0.13:
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

    conn = sqlite3.connect(DB_PATH)
    conn.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))

    clientes = []
    for i in range(1, 91):
        clientes.append({
            "id_cliente": i,
            "nombre": dirty_text(person_name(rng), rng, 0.08),
            "distrito": dirty_text(rng.choice(DISTRICTS), rng, 0.25),
            "segmento": dirty_text(rng.choice(SEGMENTS), rng, 0.18),
            "fecha_registro": dirty_date(2025, rng.randint(1, 12), rng.randint(1, 28), rng),
        })

    productos = []
    for i, (nombre, categoria, proveedor, costo, precio) in enumerate(PRODUCTOS, start=1):
        productos.append({
            "id_producto": i,
            "nombre": dirty_text(nombre, rng, 0.12),
            "categoria": dirty_text(categoria, rng, 0.20),
            "proveedor": dirty_text(proveedor, rng, 0.15),
            "costo_unitario": round(costo * rng.uniform(0.94, 1.08), 2),
            "precio_lista": round(precio * rng.uniform(0.96, 1.12), 2),
        })

    tiendas = []
    for i in range(1, 8):
        tiendas.append({
            "id_tienda": i,
            "nombre": dirty_text(f"Abarrotes Esperanza {i}", rng, 0.10),
            "distrito": dirty_text(rng.choice(DISTRICTS), rng, 0.22),
            "zona": dirty_text(rng.choice(["Norte", "Sur", "Este", "Oeste", "Centro"]), rng, 0.18),
            "tipo_local": dirty_text(rng.choice(STORE_TYPES), rng, 0.18),
        })

    insert_rows(conn, "clientes", ["id_cliente", "nombre", "distrito", "segmento", "fecha_registro"], clientes)
    insert_rows(conn, "productos", ["id_producto", "nombre", "categoria", "proveedor", "costo_unitario", "precio_lista"], productos)
    insert_rows(conn, "tiendas", ["id_tienda", "nombre", "distrito", "zona", "tipo_local"], tiendas)

    ventas = []
    duplicate_pool = []
    for i in range(1, N_ROWS + 1):
        if duplicate_pool and rng.random() < 0.035:
            row = rng.choice(duplicate_pool).copy()
            row["id_venta"] = i
            ventas.append(row)
            continue

        producto = productos[rng.randrange(len(productos))]
        cantidad = rng.randint(4, 75)
        if rng.random() < 0.02:
            cantidad *= rng.randint(3, 5)
        descuento = rng.choice([0, 0, 0, 3, 5, 8, 10, 12, 15])
        precio_venta = producto["precio_lista"] * rng.uniform(0.96, 1.08)
        costo = producto["costo_unitario"] * rng.uniform(0.97, 1.05)
        stock_minimo = max(30, cantidad + 10)
        stock_inicial = rng.randint(stock_minimo, stock_minimo + 230)
        merma = rng.choices([0, 0, 0, 1, 2, 3, 5], weights=[35, 25, 15, 10, 7, 5, 3])[0]
        stock_final = max(0, stock_inicial - cantidad - merma)
        precio_promedio_didactico = 7.2 + rng.gauss(0, 1.1)
        monto = cantidad * precio_promedio_didactico * (1 - descuento / 100) + precio_venta * 1.8 + rng.gauss(0, 10.0)
        margen = cantidad * (precio_promedio_didactico - costo * 0.45) - merma * costo + rng.gauss(0, 5.0)
        if rng.random() < 0.014:
            monto *= rng.uniform(2.0, 3.8)
            margen *= rng.uniform(1.5, 2.8)

        row = {
            "id_venta": i,
            "id_cliente": rng.randint(1, len(clientes)),
            "id_producto": producto["id_producto"],
            "id_tienda": rng.randint(1, len(tiendas)),
            "fecha_operacion": dirty_date(2026, rng.randint(1, 6), rng.randint(1, 28), rng),
            "cantidad_unidades": dirty_number(cantidad, rng, False, 0.12),
            "precio_venta_unitario": dirty_number(precio_venta, rng, True, 0.14),
            "costo_unitario": dirty_number(costo, rng, True, 0.14),
            "descuento_pct": dirty_number(descuento, rng, False, 0.11),
            "stock_inicial": dirty_number(stock_inicial, rng, False, 0.10),
            "stock_final": dirty_number(stock_final, rng, False, 0.11),
            "merma_unidades": dirty_number(merma, rng, False, 0.10),
            "canal": dirty_text(rng.choice(CHANNELS), rng, 0.20),
            "metodo_pago": dirty_text(rng.choice(PAYMENT_METHODS), rng, 0.18),
            "monto_venta_soles": dirty_number(max(monto, 0.5), rng, True, 0.13),
            "margen_venta_soles": dirty_number(margen, rng, True, 0.13),
            "observacion": dirty_text(rng.choice(["OK", "Promocion", "Revisar stock", "Cliente frecuente", ""]), rng, 0.12),
        }
        if rng.random() < 0.08:
            row["observacion"] = None
        ventas.append(row)
        if rng.random() < 0.18:
            duplicate_pool.append(row.copy())

    venta_cols = [
        "id_venta",
        "id_cliente",
        "id_producto",
        "id_tienda",
        "fecha_operacion",
        "cantidad_unidades",
        "precio_venta_unitario",
        "costo_unitario",
        "descuento_pct",
        "stock_inicial",
        "stock_final",
        "merma_unidades",
        "canal",
        "metodo_pago",
        "monto_venta_soles",
        "margen_venta_soles",
        "observacion",
    ]
    insert_rows(conn, "ventas", venta_cols, ventas)
    conn.commit()
    conn.close()

    write_csv(CSV_DIR / "clientes.csv", ["id_cliente", "nombre", "distrito", "segmento", "fecha_registro"], clientes)
    write_csv(CSV_DIR / "productos.csv", ["id_producto", "nombre", "categoria", "proveedor", "costo_unitario", "precio_lista"], productos)
    write_csv(CSV_DIR / "tiendas.csv", ["id_tienda", "nombre", "distrito", "zona", "tipo_local"], tiendas)
    write_csv(CSV_DIR / "ventas.csv", venta_cols, ventas)

    print(f"Generado {DB_PATH.name} con {len(ventas)} ventas.")


if __name__ == "__main__":
    main()
