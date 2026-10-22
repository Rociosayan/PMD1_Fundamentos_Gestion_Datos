# ============================================================
# LavaYa · Panel de Análisis de Pedidos (Streamlit)
# ============================================================
import io, sqlite3
from pathlib import Path
import numpy as np
import pandas as pd
import requests
import streamlit as st
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

st.set_page_config(page_title="LavaYa · Panel de Análisis de Pedidos", page_icon="🧺", layout="wide")
SEMILLA = 42
X, Y = "peso_ropa_kg", "costo_servicio_soles"
NUM = ["peso_ropa_kg", "prendas_delicadas", "ocupacion_local_pct", "costo_servicio_soles"]
RUTA = Path(__file__).resolve().parent.parent / "PMD1_15_Casos_Sinteticos" / "16_Lavanderia_PMD1.xlsx"
URL = ("https://raw.githubusercontent.com/Rociosayan/PMD1_Fundamentos_Gestion_Datos/main/"
       "PMD1_15_Casos_Sinteticos/16_Lavanderia_PMD1.xlsx")

# ---------- 1. Carga: ruta del repo y, si falta, la URL raw de GitHub ----------
@st.cache_data
def cargar_hojas():
    if RUTA.exists():
        return pd.read_excel(RUTA, sheet_name=None), f"archivo del repositorio ({RUTA.name})"
    r = requests.get(URL, timeout=60); r.raise_for_status()
    return pd.read_excel(io.BytesIO(r.content), sheet_name=None), "URL raw de GitHub"

def crear_conexion(hojas):
    # SQLite en memoria: cada hoja (menos LEEME) es una tabla separada
    conn = sqlite3.connect(":memory:", check_same_thread=False)
    for nombre, df in hojas.items():
        if nombre != "LEEME":
            df.to_sql(nombre.lower(), conn, index=False)
    conn.execute("""CREATE VIEW vw_analitica AS
        SELECT o.id_operacion, o.fecha, o.id_cliente, c.ciudad, c.antiguedad_meses,
               o.id_catalogo, k.nombre_item, k.nivel, k.precio_referencia_soles,
               o.id_sede, s.nombre_sede, s.zona,
               o.peso_ropa_kg, o.prendas_delicadas, o.ocupacion_local_pct, o.costo_servicio_soles
        FROM operaciones o
        LEFT JOIN clientes c ON o.id_cliente = c.id_cliente
        LEFT JOIN catalogo k ON o.id_catalogo = k.id_catalogo
        LEFT JOIN sedes s    ON o.id_sede = s.id_sede""")
    return conn

# ---------- 2. Limpieza (misma lógica y orden que el notebook) ----------
def limpiar(antes):
    limpio, bit = antes.copy(), []
    def reg(paso, motivo): bit.append({"paso": paso, "motivo": motivo, "filas_resultantes": len(limpio)})
    n = len(limpio); limpio = limpio.drop_duplicates()
    reg(f"Eliminar {n-len(limpio)} duplicados exactos", "Mismo pedido digitado dos veces")
    txt = limpio["fecha"].astype(str).str.strip()
    limpio["fecha"] = pd.to_datetime(txt, format="%Y-%m-%d", errors="coerce").fillna(
        pd.to_datetime(txt, format="%d/%m/%Y", errors="coerce"))
    reg(f"Unificar fechas (sin convertir: {limpio['fecha'].isna().sum()})", "Formatos AAAA-MM-DD y D/M/AAAA")
    for c in ["ciudad", "nivel", "nombre_sede", "zona", "nombre_item"]:
        limpio[c] = limpio[c].astype("string").str.strip().str.lower()
    reg("Quitar espacios y unificar minúsculas", "Evita categorías duplicadas")
    limpio[["nivel", "nombre_item"]] = limpio[["nivel", "nombre_item"]].fillna("sin catalogo")
    limpio["precio_referencia_soles"] = limpio["precio_referencia_soles"].fillna(limpio["precio_referencia_soles"].median())
    reg("Marcar 'sin catalogo' en FK huérfanas", "El pedido es válido; falta la descripción del servicio")
    n = len(limpio)
    limpio = limpio[~((limpio[X] < 0.5) | (limpio[X] > 40) | (limpio[Y] <= 0))]
    reg(f"Eliminar {n-len(limpio)} valores fuera de rango", "Peso > 40 kg o costo ≤ 0: error de digitación")
    n = len(limpio); limpio = limpio.dropna(subset=[X, Y])
    reg(f"Eliminar {n-len(limpio)} filas sin peso o sin costo", "Imputarlas fabricaría la relación a medir")
    for c in ["prendas_delicadas", "ocupacion_local_pct"]:
        k = int(limpio[c].isna().sum())
        if k:
            limpio[c] = limpio[c].fillna(limpio[c].median())
            reg(f"Imputar {k} nulos de {c} con la mediana", "Variable secundaria; se conserva el pedido")
    limpio["prendas_delicadas"] = limpio["prendas_delicadas"].round().astype(int)
    reg("Convertir prendas_delicadas a entero", "Un conteo no puede ser decimal")
    return limpio, pd.DataFrame(bit)

@st.cache_data
def preparar():
    hojas, origen = cargar_hojas()
    conn = crear_conexion(hojas)
    antes = pd.read_sql_query("SELECT * FROM vw_analitica", conn)
    limpio, bitacora = limpiar(antes)
    return hojas, origen, antes, limpio, bitacora

hojas, origen, antes, limpio, bitacora = preparar()
conn = crear_conexion(hojas)

# ---------- 3. Regresión ----------
@st.cache_data
def regresion(limpio):
    Xd, yd = limpio[[X]], limpio[Y]
    Xtr, Xte, ytr, yte = train_test_split(Xd, yd, test_size=0.2, random_state=SEMILLA)
    m = LinearRegression().fit(Xtr, ytr); pred = m.predict(Xte)
    mse = mean_squared_error(yte, pred)
    return dict(b0=m.intercept_, b1=m.coef_[0], r2=r2_score(yte, pred), r2_tr=m.score(Xtr, ytr),
                mse=mse, rmse=np.sqrt(mse), mae=mean_absolute_error(yte, pred),
                n_tr=len(Xtr), n_te=len(Xte), xte=Xte[X].values, yte=yte.values, pred=pred)
R = regresion(limpio)

# ---------- Interfaz ----------
st.sidebar.title("🧺 LavaYa")
st.sidebar.caption("Panel de Análisis de Pedidos")
st.title("LavaYa · Panel de Análisis de Pedidos")

SECCIONES = [
    ("Resumen ejecutivo", "📌", "Indicadores clave del negocio"),
    ("Base de datos", "🗄️", "Tablas, relaciones y consultas"),
    ("Análisis exploratorio", "📊", "Distribuciones y comparativos por local"),
    ("Calidad de datos", "🧹", "Correcciones aplicadas y su impacto"),
    ("Modelo de tarifa", "📈", "Costo según el peso del pedido"),
    ("Simulador de costo", "🧮", "Estima el costo de un pedido"),
    ("Segmentación de pedidos", "🧩", "Tipos de pedido y acciones"),
]
if "seccion" not in st.session_state:
    st.session_state.seccion = "Inicio"
def ir(nombre):
    st.session_state.seccion = nombre

st.sidebar.markdown("### Navegación")
st.sidebar.button("🏠 Inicio", on_click=ir, args=("Inicio",), width="stretch")
for nombre, icono, _ in SECCIONES:
    st.sidebar.button(f"{icono} {nombre}", on_click=ir, args=(nombre,), width="stretch",
                      type="primary" if st.session_state.seccion == nombre else "secondary")
sec = st.session_state.seccion

if sec == "Inicio":
    st.markdown("#### Selecciona un módulo del panel")
    filas = [SECCIONES[i:i + 4] for i in range(0, len(SECCIONES), 4)]
    for fila in filas:
        cols = st.columns(4)
        for col, (nombre, icono, desc) in zip(cols, fila):
            with col.container(border=True):
                st.markdown(f"<div style='font-size:42px;text-align:center'>{icono}</div>"
                            f"<h4 style='text-align:center;margin:0'>{nombre}</h4>"
                            f"<p style='text-align:center;color:gray;font-size:0.9em'>{desc}</p>",
                            unsafe_allow_html=True)
                st.button("Abrir", key=f"abrir_{nombre}", on_click=ir, args=(nombre,), width="stretch")
else:
    icono = dict((n, i) for n, i, _ in SECCIONES)[sec]
    c1, c2 = st.columns([5, 1])
    c1.header(f"{icono} {sec}")
    c2.button("⬅️ Volver al inicio", on_click=ir, args=("Inicio",), width="stretch")

if sec == "Resumen ejecutivo":
    st.markdown("""
LavaYa opera **5 locales** de lavandería. Este panel consolida los pedidos registrados en 2025 para
**definir una tarifa de referencia por kilo**, comparar locales y orientar la atención según el tipo de pedido.
""")
    k = st.columns(4)
    k[0].metric("Pedidos válidos", f"{len(limpio):,}")
    k[1].metric("Ingreso total", f"S/ {limpio[Y].sum():,.0f}")
    k[2].metric("Ticket promedio", f"S/ {limpio[Y].mean():.2f}")
    k[3].metric("Peso promedio", f"{limpio[X].mean():.1f} kg")
    k = st.columns(4)
    k[0].metric("Tarifa estimada por kg", f"S/ {R['b1']:.2f}")
    k[1].metric("Clientes atendidos", limpio["id_cliente"].nunique())
    k[2].metric("Locales", limpio["nombre_sede"].nunique())
    k[3].metric("Registros descartados", len(antes) - len(limpio))
    v = limpio.groupby("nombre_sede")[Y].agg(["count", "sum", "mean"]).round(2)
    v.columns = ["Pedidos", "Ingreso (S/)", "Ticket promedio (S/)"]
    st.subheader("Desempeño por local"); st.dataframe(v.sort_values("Ingreso (S/)", ascending=False), width="stretch")

if sec == "Base de datos":
    st.subheader("Modelo relacional")
    st.code("clientes (PK id_cliente)  ─1:N─┐\ncatalogo (PK id_catalogo) ─1:N─┼─> operaciones (PK id_operacion; FK id_cliente, id_catalogo, id_sede)\nsedes    (PK id_sede)     ─1:N─┘", language="text")
    consultas = {
        "Verificar PK (duplicados)": "SELECT COUNT(*) AS filas, COUNT(DISTINCT id_operacion) AS pk_distintas FROM operaciones",
        "Claves huérfanas en catálogo (LEFT JOIN)": """SELECT o.id_operacion, o.id_catalogo FROM operaciones o
LEFT JOIN catalogo k ON o.id_catalogo = k.id_catalogo WHERE k.id_catalogo IS NULL""",
        "Top 5 pedidos más caros (WHERE + ORDER BY)": """SELECT id_operacion, id_sede, fecha, peso_ropa_kg, costo_servicio_soles
FROM operaciones WHERE peso_ropa_kg IS NOT NULL ORDER BY costo_servicio_soles DESC LIMIT 5""",
        "Promedios por local (JOIN + GROUP BY + HAVING)": """SELECT nombre_sede, zona, COUNT(*) AS pedidos,
 ROUND(AVG(peso_ropa_kg),2) AS peso_prom, ROUND(AVG(costo_servicio_soles),2) AS costo_prom
FROM vw_analitica GROUP BY nombre_sede, zona HAVING COUNT(*) > 50 ORDER BY costo_prom DESC""",
        "Costo por nivel de servicio": """SELECT COALESCE(nivel,'SIN CATALOGO') AS nivel, COUNT(*) AS pedidos,
 ROUND(AVG(costo_servicio_soles),2) AS costo_prom FROM vw_analitica GROUP BY nivel ORDER BY costo_prom DESC""",
        "Ciudades sobre el promedio (subconsulta)": """SELECT ciudad, COUNT(*) AS pedidos, ROUND(AVG(costo_servicio_soles),2) AS costo_prom
FROM vw_analitica GROUP BY ciudad
HAVING AVG(costo_servicio_soles) > (SELECT AVG(costo_servicio_soles) FROM operaciones) ORDER BY costo_prom DESC""",
    }
    elegida = st.selectbox("Consulta", list(consultas))
    sql = st.text_area("Consulta SQL (editable)", consultas[elegida], height=140)
    try:
        st.dataframe(pd.read_sql_query(sql, conn), width="stretch")
    except Exception as e:
        st.error(f"Error en la consulta: {e}")
    st.caption("Tablas: operaciones, clientes, catalogo, sedes y vista consolidada vw_analitica.")

if sec == "Análisis exploratorio":
    st.subheader("Vista general de los registros originales")
    st.write(f"Dimensiones: {antes.shape[0]} filas × {antes.shape[1]} columnas")
    st.dataframe(antes.head(10), width="stretch")
    st.dataframe(antes[NUM].describe().round(2), width="stretch")
    fig, ax = plt.subplots(1, 3, figsize=(16, 4.5))
    ax[0].hist(antes[Y].dropna(), bins=30, color="#164B70", edgecolor="white"); ax[0].set_title("Distribución del costo (S/)")
    ax[1].scatter(antes[X], antes[Y], alpha=.5, color="#E07B39"); ax[1].set_title("Peso (kg) vs costo (S/)")
    p = antes.groupby("nombre_sede")[Y].mean().sort_values(); ax[2].barh(p.index, p.values, color="#2E8B57")
    ax[2].set_title("Costo promedio por local (S/)"); plt.tight_layout(); st.pyplot(fig)
    st.info(f"Correlación peso–costo antes de limpiar: **{antes[X].corr(antes[Y]):.3f}**. "
            "Los registros originales contienen pesos imposibles (180 y 250 kg) que distorsionan la relación; ver Calidad de datos.")

if sec == "Calidad de datos":
    st.subheader("Correcciones aplicadas")
    st.dataframe(bitacora, width="stretch")
    comp = pd.DataFrame({
        "indicador": ["Filas", "Nulos totales", "Duplicados exactos", "Costo promedio (S/)", "Peso promedio (kg)", "Correlación X-Y"],
        "antes": [len(antes), int(antes.isna().sum().sum()), int(antes.duplicated().sum()),
                  round(antes[Y].mean(), 2), round(antes[X].mean(), 2), round(antes[X].corr(antes[Y]), 3)],
        "después": [len(limpio), int(limpio.isna().sum().sum()), int(limpio.duplicated().sum()),
                    round(limpio[Y].mean(), 2), round(limpio[X].mean(), 2), round(limpio[X].corr(limpio[Y]), 3)]})
    st.subheader("Antes vs después"); st.dataframe(comp.astype(str), width="stretch")
    st.success(f"Se conserva el {len(limpio)/len(antes):.1%} de los pedidos. Eliminar 3 valores imposibles "
               "cambia por completo la correlación peso–costo.")

if sec == "Modelo de tarifa":
    st.subheader("Tarifa estimada: costo del servicio según el peso")
    st.latex(rf"\text{{costo}} = {R['b0']:.2f} + {R['b1']:.2f}\times\text{{peso\_kg}}")
    m = st.columns(5)
    m[0].metric("R² prueba", f"{R['r2']:.3f}"); m[1].metric("MSE", f"{R['mse']:.2f}")
    m[2].metric("RMSE (S/)", f"{R['rmse']:.2f}"); m[3].metric("MAE (S/)", f"{R['mae']:.2f}")
    m[4].metric("Train / test", f"{R['n_tr']} / {R['n_te']}")
    fig, ax = plt.subplots(1, 2, figsize=(13, 4.5))
    xs = np.linspace(limpio[X].min(), limpio[X].max(), 50)
    ax[0].scatter(R["xte"], R["yte"], alpha=.6, label="Prueba (real)"); ax[0].plot(xs, R["b0"] + R["b1"] * xs, "r", label="Recta")
    ax[0].set_xlabel("Peso (kg)"); ax[0].set_ylabel("Costo (S/)"); ax[0].legend(); ax[0].set_title("Recta de regresión")
    ax[1].scatter(R["yte"], R["pred"], alpha=.6, color="#E07B39"); lim = [R["yte"].min(), R["yte"].max()]
    ax[1].plot(lim, lim, "k--"); ax[1].set_xlabel("Real"); ax[1].set_ylabel("Predicho"); ax[1].set_title("Real vs predicho")
    plt.tight_layout(); st.pyplot(fig)
    st.markdown(f"""
- **Pendiente:** cada kilo adicional se asocia con **S/ {R['b1']:.2f}** más de costo.
- **R² = {R['r2']:.3f}:** el peso explica cerca del {R['r2']:.0%} de la variación del costo.
- **RMSE = S/ {R['rmse']:.2f}:** sirve como tarifa de referencia, no para cotizar cada pedido.
- Es una asociación, no una relación causal; válido para pedidos de 1 a 25 kg.
""")

if sec == "Simulador de costo":
    st.subheader("Simula el costo de un pedido")
    kg = st.number_input("Peso de la ropa (kg)", min_value=0.5, max_value=40.0, value=8.0, step=0.5)
    est = R["b0"] + R["b1"] * kg
    st.metric("Costo estimado", f"S/ {est:.2f}", help="Estimación del modelo de tarifa")
    st.caption(f"Error típico ± S/ {R['rmse']:.2f}. Fuera de 1–25 kg la estimación no está validada.")
    if kg > 25:
        st.warning("Este peso está fuera del rango observado en los datos.")

if sec == "Segmentación de pedidos":
    st.subheader("Tipos de pedido (K-Means)")
    Z = StandardScaler().fit_transform(limpio[NUM])
    pr = pd.DataFrame([{"k": k, "inercia": KMeans(k, n_init=10, random_state=SEMILLA).fit(Z).inertia_,
                        "silueta": silhouette_score(Z, KMeans(k, n_init=10, random_state=SEMILLA).fit_predict(Z))}
                       for k in range(2, 8)]).round(3)
    fig, ax = plt.subplots(1, 2, figsize=(12, 3.6))
    ax[0].plot(pr.k, pr.inercia, "o-"); ax[0].set_title("Método del codo")
    ax[1].plot(pr.k, pr.silueta, "o-", color="green"); ax[1].set_title("Silueta"); st.pyplot(fig)
    k = st.slider("Número de grupos (k)", 2, 7, 3)
    seg = limpio[NUM].copy(); seg["segmento"] = KMeans(k, n_init=10, random_state=SEMILLA).fit_predict(Z)
    perfil = seg.groupby("segmento")[NUM].mean().round(2)
    perfil["pedidos"] = seg.segmento.value_counts().sort_index(); perfil["%"] = (perfil.pedidos / len(seg) * 100).round(1)
    st.dataframe(perfil, width="stretch")
    fig, ax = plt.subplots(figsize=(7, 4.2))
    for s, g in seg.groupby("segmento"):
        ax.scatter(g[X], g[Y], alpha=.6, label=f"Segmento {s}")
    ax.set_xlabel("Peso (kg)"); ax.set_ylabel("Costo (S/)"); ax.legend(); st.pyplot(fig)
    st.info("Con k = 3: pedido estándar en hora tranquila, pedido estándar en hora punta y pedido grande con "
            "prendas delicadas. La silueta (~0,24) indica grupos superpuestos: son orientativos.")

st.markdown("<hr style='margin-top:40px'><p style='text-align:center;color:#999;font-size:0.75em'>Datos sintéticos con fines de demostración.</p>", unsafe_allow_html=True)
