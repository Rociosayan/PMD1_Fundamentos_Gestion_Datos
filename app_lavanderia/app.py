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
    for c in ["ciudad", "nivel", "zona"]:
        limpio[c] = limpio[c].astype("string").str.strip().str.lower()
    for c in ["nombre_sede", "nombre_item"]:
        limpio[c] = limpio[c].astype("string").str.strip()
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

def sql_box(titulo, icono, sql, nota=None):
    # Desplegable con la consulta SQL y su resultado
    with st.expander(titulo, icon=icono, expanded=False):
        st.code(sql.strip(), language="sql")
        st.dataframe(pd.read_sql_query(sql, conn), width="stretch", hide_index=True)
        if nota:
            st.caption(nota)

def grafico():
    return plt.subplots(figsize=(8, 4))

if sec == "Resumen ejecutivo":
    st.markdown("LavaYa opera **5 locales** de lavandería. Este panel consolida los pedidos de 2025 para "
                "**definir una tarifa de referencia por kilo**, comparar locales y orientar la atención según el tipo de pedido.")
    k = st.columns(4)
    k[0].metric("Pedidos válidos", f"{len(limpio):,}")
    k[1].metric("Ingreso total", f"S/ {limpio[Y].sum():,.0f}")
    k[2].metric("Ticket promedio", f"S/ {limpio[Y].mean():.2f}")
    k[3].metric("Tarifa estimada por kg", f"S/ {R['b1']:.2f}")
    with st.expander("Más indicadores", icon="📌"):
        k = st.columns(4)
        k[0].metric("Peso promedio", f"{limpio[X].mean():.1f} kg")
        k[1].metric("Clientes atendidos", limpio["id_cliente"].nunique())
        k[2].metric("Locales", limpio["nombre_sede"].nunique())
        k[3].metric("Registros descartados", len(antes) - len(limpio))
    with st.expander("Desempeño por local", icon="🏪"):
        v = limpio.groupby("nombre_sede")[Y].agg(["count", "sum", "mean"]).round(2)
        v.columns = ["Pedidos", "Ingreso (S/)", "Ticket promedio (S/)"]
        st.dataframe(v.sort_values("Ingreso (S/)", ascending=False), width="stretch")
    with st.expander("Hallazgos principales", icon="💡"):
        st.markdown(f"""
- Cada kilo adicional se asocia con **S/ {R['b1']:.2f}** más de costo: base para una tarifa común.
- Los servicios de nivel *especial* cuestan aproximadamente el doble que los básicos.
- Casi 4 de cada 10 pedidos son pequeños y llegan en horas de alta ocupación (ver Segmentación).
""")

if sec == "Base de datos":
    with st.expander("Ver tablas", icon="📋"):
        t = st.selectbox("Tabla", ["operaciones", "clientes", "catalogo", "sedes"])
        n = pd.read_sql_query(f"SELECT COUNT(*) n FROM {t}", conn).n[0]
        st.caption(f"{n} registros")
        st.dataframe(pd.read_sql_query(f"SELECT * FROM {t}", conn), width="stretch", hide_index=True)
    with st.expander("Unir tablas", icon="🔗"):
        st.code("clientes (PK id_cliente)  ─1:N─┐\ncatalogo (PK id_catalogo) ─1:N─┼─> operaciones (PK id_operacion; FK id_cliente, id_catalogo, id_sede)\nsedes    (PK id_sede)     ─1:N─┘", language="text")
        q = """SELECT o.id_operacion, o.fecha, c.nombre_cliente, c.ciudad, k.nombre_item, k.nivel,
       s.nombre_sede, s.zona, o.peso_ropa_kg, o.costo_servicio_soles
FROM operaciones o
LEFT JOIN clientes c ON o.id_cliente  = c.id_cliente
LEFT JOIN catalogo k ON o.id_catalogo = k.id_catalogo
LEFT JOIN sedes    s ON o.id_sede     = s.id_sede"""
        st.code(q, language="sql")
        st.dataframe(pd.read_sql_query(q, conn), width="stretch", hide_index=True)
        h = pd.read_sql_query("""SELECT COUNT(*) n FROM operaciones o LEFT JOIN catalogo k
                                 ON o.id_catalogo = k.id_catalogo WHERE k.id_catalogo IS NULL""", conn).n[0]
        st.caption(f"LEFT JOIN conserva todos los pedidos; {h} pedidos tienen un servicio que no existe en el catálogo.")
    sql_box("Top 5 clientes por gasto", "🏆", """
SELECT c.id_cliente, TRIM(c.nombre_cliente) AS cliente, c.ciudad,
       COUNT(*) AS pedidos, ROUND(SUM(o.costo_servicio_soles), 2) AS gasto_total_soles
FROM operaciones o JOIN clientes c ON o.id_cliente = c.id_cliente
WHERE o.costo_servicio_soles > 0
GROUP BY c.id_cliente ORDER BY gasto_total_soles DESC LIMIT 5""")
    sql_box("Top 5 servicios más pedidos", "🧺", """
SELECT k.nombre_item AS servicio, k.nivel, COUNT(*) AS pedidos,
       ROUND(AVG(o.costo_servicio_soles), 2) AS costo_promedio
FROM operaciones o JOIN catalogo k ON o.id_catalogo = k.id_catalogo
GROUP BY k.id_catalogo ORDER BY pedidos DESC LIMIT 5""")
    sql_box("Ingresos por sede", "🏪", """
SELECT s.nombre_sede, s.zona, COUNT(*) AS pedidos,
       ROUND(SUM(o.costo_servicio_soles), 2) AS ingreso_soles,
       ROUND(AVG(o.costo_servicio_soles), 2) AS ticket_promedio
FROM operaciones o JOIN sedes s ON o.id_sede = s.id_sede
WHERE o.costo_servicio_soles > 0
GROUP BY s.id_sede HAVING COUNT(*) > 50 ORDER BY ingreso_soles DESC""")
    sql_box("Costo promedio por nivel de servicio", "🏷️", """
SELECT COALESCE(k.nivel, 'sin catálogo') AS nivel, COUNT(*) AS pedidos,
       ROUND(AVG(o.costo_servicio_soles), 2) AS costo_promedio
FROM operaciones o LEFT JOIN catalogo k ON o.id_catalogo = k.id_catalogo
GROUP BY k.nivel ORDER BY costo_promedio DESC""")
    sql_box("Pedidos por mes", "📅", """
SELECT CASE WHEN fecha LIKE '____-__-__' THEN SUBSTR(fecha, 1, 7)
            ELSE SUBSTR(fecha, -4) || '-' || printf('%02d', CAST(SUBSTR(fecha, INSTR(fecha, '/') + 1,
                 INSTR(SUBSTR(fecha, INSTR(fecha, '/') + 1), '/') - 1) AS INTEGER)) END AS mes,
       COUNT(*) AS pedidos, ROUND(SUM(costo_servicio_soles), 2) AS ingreso_soles
FROM operaciones GROUP BY mes ORDER BY mes""", "Las fechas en formato D/M/AAAA se convierten a AAAA-MM dentro de la consulta.")
    with st.expander("Consulta SQL libre", icon="⌨️"):
        sql = st.text_area("Consulta SQL", "SELECT * FROM vw_analitica LIMIT 10", height=120)
        try:
            st.dataframe(pd.read_sql_query(sql, conn), width="stretch", hide_index=True)
        except Exception as e:
            st.error(f"Error en la consulta: {e}")
        st.caption("Tablas: operaciones, clientes, catalogo, sedes y vista vw_analitica.")

if sec == "Análisis exploratorio":
    with st.expander("Vista general de los registros", icon="🔎"):
        st.write(f"{antes.shape[0]} registros × {antes.shape[1]} columnas")
        st.dataframe(antes.head(10), width="stretch", hide_index=True)
    with st.expander("Estadísticas descriptivas", icon="📐"):
        st.dataframe(antes[NUM].describe().round(2), width="stretch")
    with st.expander("Distribución del costo", icon="📊"):
        fig, ax = grafico(); ax.hist(antes[Y].dropna(), bins=30, color="#164B70", edgecolor="white")
        ax.set_xlabel("Costo del servicio (S/)"); ax.set_ylabel("Pedidos"); st.pyplot(fig)
        st.caption("La mayoría de pedidos cuesta entre S/ 29 y S/ 64; hay un valor negativo (error de registro).")
    with st.expander("Peso vs costo", icon="⚖️"):
        fig, ax = grafico(); ax.scatter(antes[X], antes[Y], alpha=.5, color="#E07B39")
        ax.set_xlabel("Peso (kg)"); ax.set_ylabel("Costo (S/)"); st.pyplot(fig)
        st.caption(f"Correlación en registros originales: {antes[X].corr(antes[Y]):.3f}. Dos pesos imposibles (180 y 250 kg) distorsionan la relación.")
    with st.expander("Costo promedio por local", icon="🏪"):
        p = antes.groupby("nombre_sede")[Y].mean().sort_values()
        fig, ax = grafico(); ax.barh(p.index, p.values, color="#2E8B57"); ax.set_xlabel("Costo promedio (S/)"); st.pyplot(fig)
    with st.expander("Pedidos por zona y nivel", icon="🗺️"):
        c1, c2 = st.columns(2)
        c1.dataframe(antes["zona"].value_counts(dropna=False), width="stretch")
        c2.dataframe(antes["nivel"].value_counts(dropna=False), width="stretch")

if sec == "Calidad de datos":
    m = st.columns(3)
    m[0].metric("Registros originales", len(antes)); m[1].metric("Registros válidos", len(limpio))
    m[2].metric("Conservados", f"{len(limpio)/len(antes):.1%}")
    txt = antes["fecha"].astype(str).str.strip()
    cli = pd.read_sql_query("SELECT nombre_cliente FROM clientes", conn).nombre_cliente
    fuera = antes[(antes[X] < 0.5) | (antes[X] > 40) | (antes[Y] <= 0)]
    problemas = [
        ("Pedidos duplicados", "♻️", int(antes.duplicated().sum()), "Se eliminaron: era el mismo pedido registrado dos veces.", antes[antes.duplicated(keep=False)]),
        ("Fechas con formato distinto", "📅", int((~txt.str.match(r"^\d{4}-\d{2}-\d{2}$")).sum()), "Se unificaron a AAAA-MM-DD.", antes[~txt.str.match(r"^\d{4}-\d{2}-\d{2}$")][["id_operacion", "fecha"]]),
        ("Espacios extra en nombres de cliente", "✂️", int((cli != cli.str.strip()).sum()), "Se recortaron los espacios.", None),
        ("Servicios inexistentes en el catálogo", "🔗", int(antes["nivel"].isna().sum()), "Se conservan como 'sin catálogo'; el pedido es válido.", antes[antes["nivel"].isna()][["id_operacion", "id_catalogo", X, Y]]),
        ("Valores imposibles", "🚫", len(fuera), "Se eliminaron: peso mayor a 40 kg o costo menor o igual a cero.", fuera[["id_operacion", X, Y]]),
        ("Datos faltantes", "❓", int(antes[NUM].isna().sum().sum()), "Sin peso o sin costo: se descartan. Prendas y ocupación: se completan con la mediana.", antes[NUM].isna().sum().to_frame("vacíos")),
    ]
    for titulo, icono, n, accion, detalle in problemas:
        with st.expander(f"{titulo} ({n})", icon=icono):
            st.markdown(f"**Corrección:** {accion}")
            if detalle is not None and len(detalle):
                st.dataframe(detalle, width="stretch")
    with st.expander("Registro de correcciones", icon="📝"):
        st.dataframe(bitacora, width="stretch", hide_index=True)
    with st.expander("Antes vs después", icon="🔄"):
        comp = pd.DataFrame({
            "Indicador": ["Registros", "Datos faltantes", "Duplicados", "Costo promedio (S/)", "Peso promedio (kg)", "Correlación peso-costo"],
            "Antes": [len(antes), int(antes.isna().sum().sum()), int(antes.duplicated().sum()),
                      round(antes[Y].mean(), 2), round(antes[X].mean(), 2), round(antes[X].corr(antes[Y]), 3)],
            "Después": [len(limpio), int(limpio.isna().sum().sum()), int(limpio.duplicated().sum()),
                        round(limpio[Y].mean(), 2), round(limpio[X].mean(), 2), round(limpio[X].corr(limpio[Y]), 3)]})
        st.dataframe(comp.astype(str), width="stretch", hide_index=True)

if sec == "Modelo de tarifa":
    st.latex(rf"\text{{costo}} = {R['b0']:.2f} + {R['b1']:.2f}\times\text{{peso (kg)}}")
    with st.expander("Indicadores del modelo", icon="🎯"):
        m = st.columns(4)
        m[0].metric("R²", f"{R['r2']:.3f}"); m[1].metric("MSE", f"{R['mse']:.2f}")
        m[2].metric("RMSE (S/)", f"{R['rmse']:.2f}"); m[3].metric("MAE (S/)", f"{R['mae']:.2f}")
        st.caption(f"Entrenamiento: {R['n_tr']} pedidos · Evaluación: {R['n_te']} pedidos.")
    with st.expander("Recta de tarifa", icon="📈"):
        xs = np.linspace(limpio[X].min(), limpio[X].max(), 50)
        fig, ax = grafico(); ax.scatter(R["xte"], R["yte"], alpha=.6, label="Pedidos reales")
        ax.plot(xs, R["b0"] + R["b1"] * xs, "r", label="Tarifa estimada"); ax.legend()
        ax.set_xlabel("Peso (kg)"); ax.set_ylabel("Costo (S/)"); st.pyplot(fig)
    with st.expander("Real vs estimado", icon="🎯"):
        fig, ax = grafico(); ax.scatter(R["yte"], R["pred"], alpha=.6, color="#E07B39")
        lim = [R["yte"].min(), R["yte"].max()]; ax.plot(lim, lim, "k--")
        ax.set_xlabel("Costo real (S/)"); ax.set_ylabel("Costo estimado (S/)"); st.pyplot(fig)
    with st.expander("Interpretación", icon="💡"):
        st.markdown(f"""
- Cada kilo adicional se asocia con **S/ {R['b1']:.2f}** más de costo.
- El peso explica cerca del **{R['r2']:.0%}** de la variación del costo.
- Error típico de **± S/ {R['rmse']:.2f}**: útil como tarifa de referencia, no para cotizar cada pedido.
- Es una asociación, no una relación causal; válido para pedidos de 1 a 25 kg.
""")

if sec == "Simulador de costo":
    kg = st.number_input("Peso de la ropa (kg)", min_value=0.5, max_value=40.0, value=8.0, step=0.5)
    est = R["b0"] + R["b1"] * kg
    st.metric("Costo estimado", f"S/ {est:.2f}", help="Estimación del modelo de tarifa")
    st.caption(f"Margen típico ± S/ {R['rmse']:.2f}.")
    if kg > 25:
        st.warning("Este peso está fuera del rango habitual de pedidos (1 a 25 kg).")
    with st.expander("Tabla de tarifas de referencia", icon="🧾"):
        tab = pd.DataFrame({"Peso (kg)": [2, 4, 6, 8, 10, 15, 20]})
        tab["Costo estimado (S/)"] = (R["b0"] + R["b1"] * tab["Peso (kg)"]).round(2)
        st.dataframe(tab, width="stretch", hide_index=True)

if sec == "Segmentación de pedidos":
    Z = StandardScaler().fit_transform(limpio[NUM])
    with st.expander("Número de grupos", icon="🔢"):
        pr = []
        for kk in range(2, 8):
            km = KMeans(kk, n_init=10, random_state=SEMILLA).fit(Z)
            pr.append({"k": kk, "inercia": km.inertia_, "silueta": silhouette_score(Z, km.labels_)})
        pr = pd.DataFrame(pr).round(3)
        fig, ax = plt.subplots(1, 2, figsize=(11, 3.5))
        ax[0].plot(pr.k, pr.inercia, "o-"); ax[0].set_title("Método del codo")
        ax[1].plot(pr.k, pr.silueta, "o-", color="green"); ax[1].set_title("Silueta"); st.pyplot(fig)
    k = st.slider("Número de grupos (k)", 2, 7, 3)
    seg = limpio[NUM].copy(); seg["segmento"] = KMeans(k, n_init=10, random_state=SEMILLA).fit_predict(Z)
    with st.expander("Perfil de cada grupo", icon="🧩"):
        perfil = seg.groupby("segmento")[NUM].mean().round(2)
        perfil["pedidos"] = seg.segmento.value_counts().sort_index(); perfil["%"] = (perfil.pedidos / len(seg) * 100).round(1)
        st.dataframe(perfil, width="stretch")
    with st.expander("Mapa de grupos", icon="🗺️"):
        fig, ax = grafico()
        for s_, g in seg.groupby("segmento"):
            ax.scatter(g[X], g[Y], alpha=.6, label=f"Grupo {s_}")
        ax.set_xlabel("Peso (kg)"); ax.set_ylabel("Costo (S/)"); ax.legend(); st.pyplot(fig)
    with st.expander("Acciones sugeridas", icon="✅"):
        st.markdown("""
Con 3 grupos:
- **Pedido estándar en hora tranquila:** promociones para atraer más pedidos en estos horarios.
- **Pedido estándar en hora punta:** descuento por dejar el pedido en horas de baja ocupación.
- **Pedido grande con prendas delicadas:** atención prioritaria y personal especializado.

Los grupos se superponen (silueta ≈ 0,24): son una orientación, no categorías exactas.
""")

st.markdown("<hr style='margin-top:40px'><p style='text-align:center;color:#999;font-size:0.75em'>Datos sintéticos con fines de demostración.</p>", unsafe_allow_html=True)
