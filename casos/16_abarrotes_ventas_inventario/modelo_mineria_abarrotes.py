import re
import sqlite3
from pathlib import Path

import numpy as np
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "abarrotes_ventas_inventario.db"


QUERY = """
SELECT
    f.id_venta,
    c.nombre AS cliente,
    c.distrito AS distrito_cliente,
    c.segmento,
    p.nombre AS producto,
    p.categoria,
    p.proveedor,
    t.nombre AS tienda,
    t.distrito AS distrito_tienda,
    t.zona,
    t.tipo_local,
    f.fecha_operacion,
    f.cantidad_unidades,
    f.precio_venta_unitario,
    f.costo_unitario,
    f.descuento_pct,
    f.stock_inicial,
    f.stock_final,
    f.merma_unidades,
    f.canal,
    f.metodo_pago,
    f.monto_venta_soles,
    f.margen_venta_soles
FROM ventas f
LEFT JOIN clientes c ON f.id_cliente = c.id_cliente
LEFT JOIN productos p ON f.id_producto = p.id_producto
LEFT JOIN tiendas t ON f.id_tienda = t.id_tienda;
"""


def clean_number(value):
    if pd.isna(value):
        return np.nan
    text = str(value).strip()
    text = text.replace("S/", "").replace(",", ".")
    match = re.search(r"-?\d+(\.\d+)?", text)
    return float(match.group(0)) if match else np.nan


def clean_text(series):
    return series.astype("string").str.strip().str.replace(r"\s+", " ", regex=True).str.title()


def clean_dates(series):
    fecha_texto = series.astype("string").str.strip()
    es_anio_primero = fecha_texto.str.match(r"^\d{4}[-/]\d{2}[-/]\d{2}$", na=False)
    fechas = pd.Series(pd.NaT, index=series.index, dtype="datetime64[ns]")
    fechas.loc[es_anio_primero] = pd.to_datetime(
        fecha_texto.loc[es_anio_primero].str.replace("/", "-", regex=False),
        format="%Y-%m-%d",
        errors="coerce",
    )
    fechas.loc[~es_anio_primero] = pd.to_datetime(fecha_texto.loc[~es_anio_primero], errors="coerce", dayfirst=True)
    return fechas


def train_simple_linear_regression(df, x_col, y_col):
    data = df[[x_col, y_col]].dropna().copy()
    data = data.drop_duplicates()
    data = data.sample(frac=1, random_state=42).reset_index(drop=True)
    split = int(len(data) * 0.80)
    train = data.iloc[:split]
    test = data.iloc[split:]

    x_train = train[x_col].to_numpy(dtype=float)
    y_train = train[y_col].to_numpy(dtype=float)
    slope, intercept = np.polyfit(x_train, y_train, deg=1)

    predictions = test.copy()
    predictions["monto_predicho"] = intercept + slope * predictions[x_col]
    error = predictions[y_col] - predictions["monto_predicho"]
    mae = float(np.mean(np.abs(error)))
    rmse = float(np.sqrt(np.mean(error ** 2)))
    ss_res = float(np.sum(error ** 2))
    ss_tot = float(np.sum((predictions[y_col] - predictions[y_col].mean()) ** 2))
    r2 = 1 - ss_res / ss_tot if ss_tot else np.nan

    metrics = pd.DataFrame(
        [
            {"metrica": "registros_entrenamiento", "valor": len(train)},
            {"metrica": "registros_prueba", "valor": len(test)},
            {"metrica": "pendiente", "valor": float(slope)},
            {"metrica": "intercepto", "valor": float(intercept)},
            {"metrica": "mae", "valor": mae},
            {"metrica": "rmse", "valor": rmse},
            {"metrica": "r2", "valor": float(r2)},
        ]
    )
    return predictions, metrics


def main():
    if not DB_PATH.exists():
        raise FileNotFoundError(f"No existe la base: {DB_PATH}")

    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(QUERY, conn)

    text_cols = [
        "cliente", "distrito_cliente", "segmento", "producto", "categoria",
        "proveedor", "tienda", "distrito_tienda", "zona", "tipo_local",
        "canal", "metodo_pago",
    ]
    for col in text_cols:
        df[col] = clean_text(df[col])

    numeric_cols = [
        "cantidad_unidades",
        "precio_venta_unitario",
        "costo_unitario",
        "descuento_pct",
        "stock_inicial",
        "stock_final",
        "merma_unidades",
        "monto_venta_soles",
        "margen_venta_soles",
    ]
    for col in numeric_cols:
        df[col] = df[col].apply(clean_number)

    df["fecha_operacion"] = clean_dates(df["fecha_operacion"])
    df = df.dropna(subset=["cantidad_unidades", "monto_venta_soles"])
    df = df.drop_duplicates(subset=["cliente", "producto", "tienda", "fecha_operacion", "cantidad_unidades", "monto_venta_soles"])

    predictions, metrics = train_simple_linear_regression(df, "cantidad_unidades", "monto_venta_soles")

    df.to_sql("dataset_abarrotes_limpio", conn, if_exists="replace", index=False)
    predictions.to_sql("predicciones_monto_venta", conn, if_exists="replace", index=False)
    metrics.to_sql("metricas_modelo_abarrotes", conn, if_exists="replace", index=False)
    conn.close()

    print("Modelo de abarrotes generado correctamente.")
    print(metrics.to_string(index=False))


if __name__ == "__main__":
    main()
