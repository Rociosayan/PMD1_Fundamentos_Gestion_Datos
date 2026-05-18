import csv
import random
import shutil
import sqlite3
from dataclasses import dataclass
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
CASES_DIR = BASE_DIR / "casos"
N_FACT_ROWS = 500
SEED = 202601


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

CHANNELS = ["Presencial", "Web", "WhatsApp", "App", "Telefono"]
PAYMENT_METHODS = ["Efectivo", "Tarjeta", "Yape", "Plin", "Transferencia"]


@dataclass(frozen=True)
class CaseSpec:
    number: int
    slug: str
    title: str
    context: str
    party_table: str
    party_id: str
    party_label: str
    item_table: str
    item_id: str
    item_label: str
    location_table: str
    location_id: str
    location_label: str
    fact_table: str
    fact_id: str
    target_col: str
    driver_col: str
    driver_label: str
    unit_col: str
    quantity_col: str
    items: list[tuple[str, str, float]]
    driver_range: tuple[float, float]
    target_base: float
    target_driver_weight: float
    target_quantity_weight: float
    target_unit_weight: float
    target_noise: float
    regression_question: str


CASES = [
    CaseSpec(
        1, "retailmax_ventas", "RetailMax - Ventas en tienda",
        "Una cadena pequena de tiendas analiza ventas por cliente, producto y sede.",
        "clientes", "id_cliente", "cliente", "productos", "id_producto", "producto",
        "sucursales", "id_sucursal", "sucursal", "ventas", "id_venta",
        "monto_total", "cantidad_productos", "cantidad de productos", "precio_unitario", "cantidad",
        [("Arroz extra", "Abarrotes", 5.8), ("Aceite vegetal", "Abarrotes", 12.5), ("Detergente", "Limpieza", 18.9),
         ("Shampoo", "Cuidado personal", 16.0), ("Galletas", "Snacks", 3.2), ("Cafe", "Bebidas", 14.5),
         ("Leche evaporada", "Lacteos", 4.7), ("Atun", "Conservas", 6.5), ("Papel higienico", "Limpieza", 10.8)],
        (1, 15), 4.0, 0.3, 2.5, 0.95, 9.0,
        "Predecir el monto total de venta a partir de la cantidad de productos."
    ),
    CaseSpec(
        2, "restaurante_pedidos", "Restaurante - Pedidos y consumo",
        "Un restaurante de menu y platos a la carta analiza pedidos diarios.",
        "clientes", "id_cliente", "cliente", "platos", "id_plato", "plato",
        "locales", "id_local", "local", "pedidos", "id_pedido",
        "total_pedido", "tiempo_preparacion_min", "tiempo de preparacion", "precio_plato", "cantidad_platos",
        [("Lomo saltado", "Criollo", 28.0), ("Aji de gallina", "Criollo", 24.0), ("Ceviche", "Marino", 34.0),
         ("Chaufa", "Fusion", 22.0), ("Pollo a la brasa", "Parrilla", 32.0), ("Tallarines verdes", "Pastas", 20.0),
         ("Sopa criolla", "Sopas", 18.0), ("Menu ejecutivo", "Menu", 16.0), ("Ensalada especial", "Ligero", 19.0)],
        (8, 55), 7.0, 0.12, 4.0, 0.9, 8.5,
        "Predecir el total del pedido usando el tiempo de preparacion o la cantidad de platos."
    ),
    CaseSpec(
        3, "farmacia_ventas", "Farmacia - Ventas de productos",
        "Una farmacia de barrio revisa ventas de medicamentos y cuidado personal.",
        "clientes", "id_cliente", "cliente", "medicamentos", "id_medicamento", "medicamento",
        "sucursales", "id_sucursal", "sucursal", "ventas", "id_venta",
        "monto_boleta", "cantidad_medicamentos", "cantidad de medicamentos", "precio_unitario", "cantidad",
        [("Paracetamol", "Analgesico", 4.5), ("Ibuprofeno", "Analgesico", 6.2), ("Alcohol gel", "Higiene", 8.0),
         ("Vitamina C", "Suplemento", 15.0), ("Jabon antibacterial", "Higiene", 5.5), ("Antigripal", "Respiratorio", 12.0),
         ("Protector solar", "Dermocosmetica", 38.0), ("Suero oral", "Hidratacion", 7.5), ("Panal adulto", "Cuidado", 42.0)],
        (1, 12), 3.0, 0.15, 2.2, 0.98, 7.0,
        "Predecir el monto de la boleta segun la cantidad de medicamentos."
    ),
    CaseSpec(
        4, "ferreteria_ventas", "Ferreteria - Compras de articulos",
        "Una ferreteria analiza compras de materiales, herramientas e insumos.",
        "clientes", "id_cliente", "cliente", "articulos", "id_articulo", "articulo",
        "tiendas", "id_tienda", "tienda", "ventas", "id_venta",
        "monto_compra", "cantidad_articulos", "cantidad de articulos", "precio_unitario", "cantidad",
        [("Cemento", "Materiales", 32.0), ("Pintura blanca", "Pinturas", 65.0), ("Brocha", "Herramientas", 12.0),
         ("Taladro", "Herramientas", 180.0), ("Clavos", "Fijaciones", 9.0), ("Tubo PVC", "Gasfiteria", 18.0),
         ("Cable electrico", "Electricidad", 45.0), ("Foco LED", "Electricidad", 10.0), ("Lija", "Acabados", 4.0)],
        (1, 20), 8.0, 0.4, 3.0, 0.92, 16.0,
        "Predecir el monto de compra a partir de la cantidad de articulos."
    ),
    CaseSpec(
        5, "clinica_atenciones", "Clinica - Atenciones ambulatorias",
        "Una clinica pequena analiza costos de atencion por servicio y sede.",
        "pacientes", "id_paciente", "paciente", "servicios", "id_servicio", "servicio",
        "sedes", "id_sede", "sede", "atenciones", "id_atencion",
        "costo_atencion", "duracion_consulta_min", "duracion de consulta", "tarifa_base", "cantidad_servicios",
        [("Consulta general", "Medicina", 70.0), ("Laboratorio basico", "Laboratorio", 55.0), ("Radiografia", "Imagenes", 95.0),
         ("Ecografia", "Imagenes", 140.0), ("Curacion", "Procedimiento", 45.0), ("Control nutricional", "Nutricion", 60.0),
         ("Terapia fisica", "Rehabilitacion", 75.0), ("Consulta pediatrica", "Pediatria", 80.0), ("Consulta dental", "Dental", 85.0)],
        (10, 75), 25.0, 1.1, 5.0, 0.75, 18.0,
        "Predecir el costo de atencion segun la duracion de la consulta."
    ),
    CaseSpec(
        6, "veterinaria_atenciones", "Veterinaria - Servicios para mascotas",
        "Una veterinaria revisa atenciones, servicios y costos por mascota.",
        "mascotas", "id_mascota", "mascota", "servicios", "id_servicio", "servicio",
        "sedes", "id_sede", "sede", "atenciones", "id_atencion",
        "costo_servicio", "peso_mascota_kg", "peso de mascota", "tarifa_base", "cantidad_servicios",
        [("Consulta", "Salud", 45.0), ("Vacuna", "Prevencion", 60.0), ("Bano medicado", "Estetica", 50.0),
         ("Desparasitacion", "Prevencion", 35.0), ("Radiografia", "Diagnostico", 120.0), ("Cirugia menor", "Procedimiento", 180.0),
         ("Corte de pelo", "Estetica", 40.0), ("Analisis sangre", "Laboratorio", 90.0), ("Hospitalizacion", "Internamiento", 220.0)],
        (2, 45), 18.0, 0.9, 8.0, 0.82, 20.0,
        "Predecir el costo del servicio usando el peso de la mascota."
    ),
    CaseSpec(
        7, "hotel_reservas", "HotelSmart - Reservas hoteleras",
        "Un hotel analiza reservas, tipo de habitacion y monto facturado.",
        "huespedes", "id_huesped", "huesped", "habitaciones", "id_habitacion", "habitacion",
        "hoteles", "id_hotel", "hotel", "reservas", "id_reserva",
        "monto_reserva", "noches_estadia", "noches de estadia", "tarifa_noche", "cantidad_habitaciones",
        [("Simple", "Estandar", 95.0), ("Doble", "Estandar", 150.0), ("Matrimonial", "Estandar", 170.0),
         ("Familiar", "Familiar", 240.0), ("Suite junior", "Suite", 320.0), ("Suite ejecutiva", "Suite", 420.0),
         ("Bungalow", "Especial", 380.0), ("Habitacion vista mar", "Premium", 360.0), ("Habitacion business", "Ejecutiva", 280.0)],
        (1, 10), 35.0, 4.0, 12.0, 0.96, 35.0,
        "Predecir el monto de reserva a partir de las noches de estadia."
    ),
    CaseSpec(
        8, "food_delivery_entregas", "FoodDelivery - Pedidos a domicilio",
        "Una plataforma local mide tiempos de entrega de pedidos.",
        "clientes", "id_cliente", "cliente", "restaurantes", "id_restaurante", "restaurante",
        "zonas", "id_zona", "zona", "entregas", "id_entrega",
        "tiempo_entrega_min", "distancia_km", "distancia", "costo_pedido", "cantidad_items",
        [("Polleria El Carbon", "Polleria", 42.0), ("Sushi Barrio", "Japonesa", 58.0), ("Pizza Centro", "Pizzeria", 45.0),
         ("Menu Criollo", "Criolla", 24.0), ("Burger Norte", "Comida rapida", 32.0), ("Cevicheria Azul", "Marina", 55.0),
         ("Chifa Dragon", "Chifa", 35.0), ("Cafe Dulce", "Cafeteria", 22.0), ("Tacos Urbanos", "Mexicana", 30.0)],
        (0.5, 15), 14.0, 2.2, 0.8, 0.04, 6.0,
        "Predecir el tiempo de entrega segun la distancia en kilometros."
    ),
    CaseSpec(
        9, "logiexpress_envios", "LogiExpress - Envios urbanos",
        "Una empresa de mensajeria analiza costos y tiempos de envio.",
        "clientes", "id_cliente", "cliente", "tipos_envio", "id_tipo_envio", "tipo_envio",
        "sedes", "id_sede", "sede", "envios", "id_envio",
        "costo_envio", "peso_paquete_kg", "peso del paquete", "tarifa_base", "cantidad_paquetes",
        [("Documento", "Liviano", 8.0), ("Paquete pequeno", "Liviano", 15.0), ("Paquete mediano", "Regular", 25.0),
         ("Paquete grande", "Regular", 40.0), ("Fragil", "Especial", 55.0), ("Express", "Urgente", 70.0),
         ("Refrigerado", "Especial", 85.0), ("Courier empresarial", "Empresa", 60.0), ("Mudanza pequena", "Volumen", 120.0)],
        (0.2, 35), 10.0, 1.6, 5.0, 0.8, 12.0,
        "Predecir el costo de envio segun el peso del paquete."
    ),
    CaseSpec(
        10, "agrodata_cultivos", "AgroData - Produccion de cultivos",
        "Una asociacion agricola analiza rendimiento de cultivos por parcela.",
        "parcelas", "id_parcela", "parcela", "cultivos", "id_cultivo", "cultivo",
        "zonas", "id_zona", "zona", "produccion", "id_produccion",
        "rendimiento_kg", "hectareas", "hectareas", "costo_insumo", "cantidad_jornales",
        [("Papa blanca", "Tuberculo", 850.0), ("Maiz amarillo", "Cereal", 760.0), ("Quinua", "Grano", 680.0),
         ("Arandano", "Fruta", 1500.0), ("Palta", "Fruta", 1200.0), ("Cafe", "Perenne", 980.0),
         ("Cacao", "Perenne", 1050.0), ("Cebolla", "Hortaliza", 620.0), ("Tomate", "Hortaliza", 700.0)],
        (0.5, 12), 120.0, 310.0, 18.0, 0.08, 180.0,
        "Predecir el rendimiento en kilogramos segun las hectareas sembradas."
    ),
    CaseSpec(
        11, "energyhome_consumo", "EnergyHome - Consumo electrico",
        "Una empresa local analiza consumo electrico mensual de hogares.",
        "hogares", "id_hogar", "hogar", "tarifas", "id_tarifa", "tarifa",
        "distritos", "id_distrito", "distrito", "consumos", "id_consumo",
        "consumo_kwh", "numero_habitantes", "numero de habitantes", "tarifa_base", "electrodomesticos",
        [("Residencial basica", "Residencial", 0.65), ("Residencial media", "Residencial", 0.72), ("Residencial alta", "Residencial", 0.85),
         ("Comercial pequena", "Comercial", 0.9), ("Comercial media", "Comercial", 1.05), ("Social", "Subvencionada", 0.45),
         ("Nocturna", "Especial", 0.6), ("Solar mixta", "Especial", 0.55), ("Temporal", "Temporal", 0.78)],
        (1, 8), 55.0, 32.0, 7.0, 22.0, 28.0,
        "Predecir el consumo electrico segun el numero de habitantes."
    ),
    CaseSpec(
        12, "gimnasio_socios", "Gimnasio - Socios y asistencias",
        "Un gimnasio analiza pagos, asistencias y planes contratados.",
        "socios", "id_socio", "socio", "planes", "id_plan", "plan",
        "sedes", "id_sede", "sede", "asistencias_pagos", "id_registro",
        "pago_mensual", "asistencias_mes", "asistencias al mes", "tarifa_plan", "clases_tomadas",
        [("Plan basico", "Mensual", 69.0), ("Plan full", "Mensual", 109.0), ("Plan premium", "Mensual", 149.0),
         ("Plan estudiante", "Promocional", 59.0), ("Plan familiar", "Familiar", 189.0), ("Yoga", "Especial", 85.0),
         ("Cross training", "Especial", 130.0), ("Funcional", "Especial", 95.0), ("Personalizado", "Premium", 220.0)],
        (1, 28), 30.0, 2.2, 3.0, 0.82, 14.0,
        "Predecir el pago mensual usando las asistencias del mes."
    ),
    CaseSpec(
        13, "panaderia_ventas", "Panaderia - Ventas diarias",
        "Una panaderia analiza ventas de productos por local y turno.",
        "clientes", "id_cliente", "cliente", "productos", "id_producto", "producto",
        "locales", "id_local", "local", "ventas", "id_venta",
        "ingreso_venta", "cantidad_unidades", "cantidad de unidades", "precio_unitario", "cantidad",
        [("Pan frances", "Panes", 0.35), ("Pan integral", "Panes", 0.55), ("Empanada", "Salados", 4.5),
         ("Torta chocolate", "Pasteles", 45.0), ("Alfajor", "Dulces", 3.0), ("Cafe pasado", "Bebidas", 5.0),
         ("Jugo natural", "Bebidas", 7.0), ("Paneton", "Temporada", 28.0), ("Queque", "Pasteles", 18.0)],
        (1, 60), 1.0, 0.06, 0.9, 0.98, 5.0,
        "Predecir el ingreso de venta segun la cantidad de unidades vendidas."
    ),
    CaseSpec(
        14, "taller_mecanico_ordenes", "Taller mecanico - Ordenes de servicio",
        "Un taller mecanico analiza costos de reparacion por servicio y sede.",
        "clientes", "id_cliente", "cliente", "servicios", "id_servicio", "servicio",
        "sedes", "id_sede", "sede", "ordenes", "id_orden",
        "costo_reparacion", "horas_trabajo", "horas de trabajo", "tarifa_base", "cantidad_repuestos",
        [("Cambio de aceite", "Mantenimiento", 90.0), ("Alineamiento", "Mantenimiento", 80.0), ("Frenos", "Seguridad", 180.0),
         ("Suspension", "Mecanica", 260.0), ("Revision electrica", "Electricidad", 150.0), ("Afinamiento", "Motor", 220.0),
         ("Cambio bateria", "Electricidad", 280.0), ("Diagnostico scanner", "Diagnostico", 120.0), ("Embrague", "Mecanica", 450.0)],
        (0.5, 12), 45.0, 38.0, 15.0, 0.72, 35.0,
        "Predecir el costo de reparacion segun las horas de trabajo."
    ),
]


def dirty_text(value: str, rng: random.Random, p: float = 0.16) -> str | None:
    if rng.random() < 0.035:
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


def dirty_number(value: float, rng: random.Random, money: bool = False, p: float = 0.13):
    if rng.random() < 0.025:
        return None
    if rng.random() >= p:
        return round(value, 2)
    option = rng.choice(["spaces", "comma", "text", "currency"] if money else ["spaces", "comma", "text"])
    if option == "spaces":
        return f" {round(value, 2)} "
    if option == "comma":
        return str(round(value, 2)).replace(".", ",")
    if option == "currency":
        return f"S/ {round(value, 2)}"
    return f"{round(value, 2)} aprox"


def dirty_date(year: int, month: int, day: int, rng: random.Random) -> str | None:
    if rng.random() < 0.025:
        return None
    if rng.random() < 0.12:
        return rng.choice([
            f"{day:02d}/{month:02d}/{year}",
            f"{year}/{month:02d}/{day:02d}",
            f"{day:02d}-{month:02d}-{year}",
            f" {year}-{month:02d}-{day:02d} ",
        ])
    return f"{year}-{month:02d}-{day:02d}"


def make_driver_value(spec: CaseSpec, rng: random.Random) -> float:
    count_like = {
        "cantidad_productos",
        "cantidad_medicamentos",
        "cantidad_articulos",
        "duracion_consulta_min",
        "noches_estadia",
        "numero_habitantes",
        "asistencias_mes",
        "cantidad_unidades",
    }
    if spec.driver_col in count_like:
        low, high = spec.driver_range
        value = rng.randint(round(low), round(high))
    else:
        value = rng.uniform(*spec.driver_range)
    if rng.random() < 0.015:
        value *= rng.uniform(2.8, 5.0)
    return value


def person_name(rng: random.Random) -> str:
    return f"{rng.choice(FIRST_NAMES)} {rng.choice(LAST_NAMES)}"


def write_csv(path: Path, columns: list[str], rows: list[dict]):
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def build_schema(spec: CaseSpec) -> str:
    return f"""
PRAGMA foreign_keys = ON;

CREATE TABLE {spec.party_table} (
    {spec.party_id} INTEGER PRIMARY KEY,
    nombre TEXT,
    distrito TEXT,
    segmento TEXT,
    fecha_registro TEXT
);

CREATE TABLE {spec.item_table} (
    {spec.item_id} INTEGER PRIMARY KEY,
    nombre TEXT,
    categoria TEXT,
    {spec.unit_col} REAL
);

CREATE TABLE {spec.location_table} (
    {spec.location_id} INTEGER PRIMARY KEY,
    nombre TEXT,
    distrito TEXT,
    zona TEXT
);

CREATE TABLE {spec.fact_table} (
    {spec.fact_id} INTEGER PRIMARY KEY,
    {spec.party_id} INTEGER,
    {spec.item_id} INTEGER,
    {spec.location_id} INTEGER,
    fecha_operacion TEXT,
    {spec.quantity_col} TEXT,
    {spec.driver_col} TEXT,
    {spec.unit_col} TEXT,
    descuento_pct TEXT,
    canal TEXT,
    metodo_pago TEXT,
    calificacion TEXT,
    {spec.target_col} TEXT,
    observacion TEXT,
    FOREIGN KEY ({spec.party_id}) REFERENCES {spec.party_table}({spec.party_id}),
    FOREIGN KEY ({spec.item_id}) REFERENCES {spec.item_table}({spec.item_id}),
    FOREIGN KEY ({spec.location_id}) REFERENCES {spec.location_table}({spec.location_id})
);
""".strip()


def insert_rows(conn: sqlite3.Connection, table: str, columns: list[str], rows: list[dict]):
    placeholders = ", ".join(["?"] * len(columns))
    col_sql = ", ".join(columns)
    sql = f"INSERT INTO {table} ({col_sql}) VALUES ({placeholders})"
    conn.executemany(sql, [[row.get(col) for col in columns] for row in rows])


def generate_case(spec: CaseSpec):
    rng = random.Random(SEED + spec.number)
    case_dir = CASES_DIR / f"{spec.number:02d}_{spec.slug}"
    if case_dir.exists():
        shutil.rmtree(case_dir)
    (case_dir / "csv").mkdir(parents=True, exist_ok=True)

    schema = build_schema(spec)
    db_path = case_dir / f"{spec.slug}.db"
    conn = sqlite3.connect(db_path)
    conn.executescript(schema)

    party_rows = []
    for i in range(1, 86):
        party_rows.append({
            spec.party_id: i,
            "nombre": dirty_text(person_name(rng), rng, 0.08),
            "distrito": dirty_text(rng.choice(DISTRICTS), rng, 0.28),
            "segmento": dirty_text(rng.choice(["Regular", "Nuevo", "Frecuente", "Premium", "Corporativo"]), rng, 0.18),
            "fecha_registro": dirty_date(2025, rng.randint(1, 12), rng.randint(1, 28), rng),
        })

    item_rows = []
    for i, (name, category, price) in enumerate(spec.items, start=1):
        item_rows.append({
            spec.item_id: i,
            "nombre": dirty_text(name, rng, 0.14),
            "categoria": dirty_text(category, rng, 0.24),
            spec.unit_col: round(price * rng.uniform(0.92, 1.12), 2),
        })

    location_rows = []
    for i in range(1, 8):
        district = rng.choice(DISTRICTS)
        location_rows.append({
            spec.location_id: i,
            "nombre": dirty_text(f"{spec.location_label.title()} {i}", rng, 0.12),
            "distrito": dirty_text(district, rng, 0.25),
            "zona": dirty_text(rng.choice(["Norte", "Sur", "Este", "Oeste", "Centro"]), rng, 0.20),
        })

    insert_rows(conn, spec.party_table, [spec.party_id, "nombre", "distrito", "segmento", "fecha_registro"], party_rows)
    insert_rows(conn, spec.item_table, [spec.item_id, "nombre", "categoria", spec.unit_col], item_rows)
    insert_rows(conn, spec.location_table, [spec.location_id, "nombre", "distrito", "zona"], location_rows)

    fact_rows = []
    duplicate_pool = []
    for i in range(1, N_FACT_ROWS + 1):
        if duplicate_pool and rng.random() < 0.035:
            base = rng.choice(duplicate_pool).copy()
            base[spec.fact_id] = i
            fact_rows.append(base)
            continue

        item_id = rng.randint(1, len(item_rows))
        item_price = item_rows[item_id - 1][spec.unit_col]
        quantity = rng.randint(1, 8)
        driver = make_driver_value(spec, rng)
        discount = rng.choice([0, 0, 0, 5, 8, 10, 12, 15, 20])
        target = (
            spec.target_base
            + spec.target_driver_weight * driver
            + spec.target_quantity_weight * quantity
            + spec.target_unit_weight * item_price
            - discount * 0.25
            + rng.gauss(0, spec.target_noise)
        )
        if rng.random() < 0.015:
            target *= rng.uniform(2.5, 4.2)
        target = max(target, 0.5)

        row = {
            spec.fact_id: i,
            spec.party_id: rng.randint(1, len(party_rows)),
            spec.item_id: item_id,
            spec.location_id: rng.randint(1, len(location_rows)),
            "fecha_operacion": dirty_date(2026, rng.randint(1, 6), rng.randint(1, 28), rng),
            spec.quantity_col: dirty_number(quantity, rng, False, 0.10),
            spec.driver_col: dirty_number(driver, rng, False, 0.14),
            spec.unit_col: dirty_number(item_price, rng, True, 0.15),
            "descuento_pct": dirty_number(discount, rng, False, 0.12),
            "canal": dirty_text(rng.choice(CHANNELS), rng, 0.20),
            "metodo_pago": dirty_text(rng.choice(PAYMENT_METHODS), rng, 0.18),
            "calificacion": dirty_number(rng.randint(1, 5), rng, False, 0.08),
            spec.target_col: dirty_number(target, rng, True, 0.12),
            "observacion": dirty_text(rng.choice(["OK", "Revisar", "Cliente frecuente", "Promocion", ""]), rng, 0.12),
        }
        if rng.random() < 0.08:
            row["observacion"] = None
        fact_rows.append(row)
        if rng.random() < 0.18:
            duplicate_pool.append(row.copy())

    fact_columns = [
        spec.fact_id, spec.party_id, spec.item_id, spec.location_id, "fecha_operacion",
        spec.quantity_col, spec.driver_col, spec.unit_col, "descuento_pct", "canal",
        "metodo_pago", "calificacion", spec.target_col, "observacion",
    ]
    insert_rows(conn, spec.fact_table, fact_columns, fact_rows)
    conn.commit()
    conn.close()

    (case_dir / "schema.sql").write_text(schema + "\n", encoding="utf-8")
    write_csv(case_dir / "csv" / f"{spec.party_table}.csv", [spec.party_id, "nombre", "distrito", "segmento", "fecha_registro"], party_rows)
    write_csv(case_dir / "csv" / f"{spec.item_table}.csv", [spec.item_id, "nombre", "categoria", spec.unit_col], item_rows)
    write_csv(case_dir / "csv" / f"{spec.location_table}.csv", [spec.location_id, "nombre", "distrito", "zona"], location_rows)
    write_csv(case_dir / "csv" / f"{spec.fact_table}.csv", fact_columns, fact_rows)

    query = f"""
SELECT
    f.{spec.fact_id},
    p.nombre AS {spec.party_label},
    p.distrito AS distrito_{spec.party_label},
    p.segmento,
    i.nombre AS {spec.item_label},
    i.categoria,
    l.nombre AS {spec.location_label},
    l.zona,
    f.fecha_operacion,
    f.{spec.quantity_col},
    f.{spec.driver_col},
    f.{spec.unit_col},
    f.descuento_pct,
    f.canal,
    f.metodo_pago,
    f.calificacion,
    f.{spec.target_col}
FROM {spec.fact_table} f
LEFT JOIN {spec.party_table} p ON f.{spec.party_id} = p.{spec.party_id}
LEFT JOIN {spec.item_table} i ON f.{spec.item_id} = i.{spec.item_id}
LEFT JOIN {spec.location_table} l ON f.{spec.location_id} = l.{spec.location_id};
""".strip()

    readme = f"""# {spec.title}

## Contexto
{spec.context}

## Tablas
- `{spec.party_table}`: datos de {spec.party_label}s.
- `{spec.item_table}`: catalogo de {spec.item_label}s.
- `{spec.location_table}`: sedes, zonas o puntos de operacion.
- `{spec.fact_table}`: tabla principal con {N_FACT_ROWS} registros y claves foraneas.

## Reto PMD1
{spec.regression_question}

Variable objetivo sugerida: `{spec.target_col}`.
Variable predictora basica sugerida: `{spec.driver_col}`.

## Suciedad incluida
- Espacios en blanco al inicio/final.
- Mayusculas y minusculas inconsistentes.
- Valores nulos.
- Fechas con formatos mezclados.
- Numeros guardados como texto, con coma decimal o simbolo `S/`.
- Duplicados parciales en la tabla principal.
- Algunos valores extremos.

## Consulta base para Pandas

```sql
{query}
```
"""
    (case_dir / "README.md").write_text(readme, encoding="utf-8")
    return case_dir


def build_main_readme():
    rows = []
    for spec in CASES:
        rows.append(
            f"| {spec.number:02d} | {spec.title} | `{spec.slug}.db` | `{spec.target_col}` | `{spec.driver_col}` |"
        )
    table = "\n".join(rows)
    content = f"""# PMD1 - Bases de datos sinteticas para Fundamentos de Gestion de Datos

Este paquete contiene 14 casos cotidianos para el PMD1. Cada caso incluye una base SQLite relacional, archivos CSV por tabla, un `schema.sql` y una guia breve.

La idea didactica es que el estudiante:

1. Descargue la base desde GitHub.
2. Se conecte a SQLite desde Colab.
3. Use SQL para unir tablas y construir un dataset analitico.
4. Limpie datos con Pandas.
5. Entrene una regresion lineal simple.
6. Guarde la tabla limpia y/o predicciones nuevamente en SQLite.

## Casos disponibles

| N | Caso | Base SQLite | Variable objetivo | Predictora sugerida |
|---|---|---|---|---|
{table}

## Ejemplo para descargar desde GitHub en Colab

```python
import requests
import sqlite3
import pandas as pd

url = "https://raw.githubusercontent.com/USUARIO/REPO/main/casos/01_retailmax_ventas/retailmax_ventas.db"
r = requests.get(url)
open("retailmax_ventas.db", "wb").write(r.content)

conn = sqlite3.connect("retailmax_ventas.db")

df = pd.read_sql_query("SELECT * FROM ventas LIMIT 5", conn)
df
```

## Nota sobre claves primarias y foraneas

Cada base ya viene con claves primarias y foraneas. El estudiante no necesita inventarlas desde cero para iniciar el analisis, pero si debe entenderlas para hacer los `JOIN`.

Tambien puede revisar el archivo `schema.sql` de cada caso para ver como se crea la estructura.
"""
    (BASE_DIR / "README.md").write_text(content, encoding="utf-8")


def main():
    CASES_DIR.mkdir(parents=True, exist_ok=True)
    generated = [generate_case(spec) for spec in CASES]
    build_main_readme()
    print(f"Generados {len(generated)} casos en: {CASES_DIR}")
    for path in generated:
        print(f"- {path}")


if __name__ == "__main__":
    main()
