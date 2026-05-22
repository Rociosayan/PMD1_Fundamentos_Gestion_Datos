import re
import sqlite3
from pathlib import Path

import numpy as np
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "industria_paradas_procesos.db"


QUERY = """
SELECT
    f.id_parada,
    m.nombre AS maquina,
    m.linea,
    m.tipo_maquina,
    m.antiguedad_anios,
    p.nombre AS proceso,
    p.familia,
    p.temperatura_objetivo_c,
    p.velocidad_objetivo_u_h,
    t.nombre AS turno,
    t.supervisor,
    f.fecha_operacion,
    f.tiempo_operacion_h,
    f.unidades_producidas,
    f.defectos_unidades,
    f.temperatura_promedio_c,
    f.velocidad_real_u_h,
    f.causa_parada,
    f.criticidad,
    f.duracion_parada_min,
    f.costo_parada_soles
FROM paradas f
LEFT JOIN maquinas m ON f.id_maquina = m.id_maquina
LEFT JOIN procesos p ON f.id_proceso = p.id_proceso
LEFT JOIN turnos t ON f.id_turno = t.id_turno;
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
    predictions["costo_predicho"] = intercept + slope * predictions[x_col]
    error = predictions[y_col] - predictions["costo_predicho"]
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

    text_cols = ["maquina", "linea", "tipo_maquina", "proceso", "familia", "turno", "supervisor", "causa_parada", "criticidad"]
    for col in text_cols:
        df[col] = clean_text(df[col])

    numeric_cols = [
        "antiguedad_anios",
        "temperatura_objetivo_c",
        "velocidad_objetivo_u_h",
        "tiempo_operacion_h",
        "unidades_producidas",
        "defectos_unidades",
        "temperatura_promedio_c",
        "velocidad_real_u_h",
        "duracion_parada_min",
        "costo_parada_soles",
    ]
    for col in numeric_cols:
        df[col] = df[col].apply(clean_number)

    fecha_texto = df["fecha_operacion"].astype("string").str.strip()
    es_anio_primero = fecha_texto.str.match(r"^\d{4}[-/]\d{2}[-/]\d{2}$", na=False)
    fechas = pd.Series(pd.NaT, index=df.index, dtype="datetime64[ns]")
    fechas.loc[es_anio_primero] = pd.to_datetime(
        fecha_texto.loc[es_anio_primero].str.replace("/", "-", regex=False),
        format="%Y-%m-%d",
        errors="coerce",
    )
    fechas.loc[~es_anio_primero] = pd.to_datetime(fecha_texto.loc[~es_anio_primero], errors="coerce", dayfirst=True)
    df["fecha_operacion"] = fechas
    df = df.dropna(subset=["duracion_parada_min", "costo_parada_soles"])
    df = df.drop_duplicates(subset=["maquina", "proceso", "turno", "fecha_operacion", "duracion_parada_min", "costo_parada_soles"])

    predictions, metrics = train_simple_linear_regression(df, "duracion_parada_min", "costo_parada_soles")

    df.to_sql("dataset_paradas_limpio", conn, if_exists="replace", index=False)
    predictions.to_sql("predicciones_costo_parada", conn, if_exists="replace", index=False)
    metrics.to_sql("metricas_modelo_paradas", conn, if_exists="replace", index=False)
    conn.close()

    print("Modelo generado correctamente.")
    print(metrics.to_string(index=False))


if __name__ == "__main__":
    main()
