import pandas as pd
import streamlit as st
import plotly.express as px

# -----------------------------
# 0) Título e Introducción
# -----------------------------
st.set_page_config(page_title="CDMX Crime Dashboard", layout="wide")

# Aplicando estilo con CSS
st.markdown("""
    <style>
    .stText {
        color: #F1C40F;
        font-weight: bold;
    }
    .stMetricValue {
        font-size: 24px;
        font-weight: bold;
        color: #333333;
    }
    .stHeader {
        background-color: #F1C40F;
        color: white;
        font-weight: bold;
    }
    .stTable th {
        background-color: #F1C40F;
        color: white;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Título de la app
st.title("👮‍♂️ Dashboard de Crímenes en la Ciudad de México")
st.markdown(
    """
    **Objetivo:** Visualizar la información de crímenes reportados en la Ciudad de México utilizando Streamlit y datos oficiales.
    **Datos:** Dataset de crímenes de la **Fiscalía General de Justicia de la Ciudad de México** (FGJCDMX).
    """, 
    unsafe_allow_html=True
)

# -----------------------------
# 1) Cargar los datos
# -----------------------------
# Cargar el archivo CSV
df = pd.read_csv('data/carpetasFGJ_acumulado_2025_01.csv', dtype={'alcaldia': str, 'delito': str})

# Limpiar los nombres de las columnas (eliminar espacios extras)
df.columns = df.columns.str.strip()

# -----------------------------
# 2) Filtros en la barra lateral
# -----------------------------
st.sidebar.header("Filtros")
crime_type = st.sidebar.selectbox(
    "Tipo de Crimen", options=sorted(df["delito"].unique()), default=None, key="crime_filter"
)
alcaldia_filter = st.sidebar.multiselect(
    "Selecciona Alcaldía", options=sorted(df["alcaldia"].unique()), default=None, key="alcaldia_filter"
)

# Radio button para tipo de gráfico
chart_type = st.sidebar.radio(
    "Tipo de Gráfico:",
    ["Gráfico de Barras", "Gráfico de Líneas"],
    key="chart_type_toggle"
)

fdf = df.copy()
if crime_type:
    fdf = fdf[fdf["delito"] == crime_type]
if alcaldia_filter:
    fdf = fdf[fdf["alcaldia"].isin(alcaldia_filter)]

# -----------------------------
# 3) KPIs (Indicadores Clave)
# -----------------------------
c1, c2, c3, c4 = st.columns(4)
total_crimes = int(fdf["delito"].count())
avg_crimes_per_alcaldia = float(fdf.groupby("alcaldia")["delito"].count().mean()) if not fdf.empty else 0.0
max_crimes = int(fdf["delito"].max())

c1.metric("Total de Crímenes", f"{total_crimes:,}")
c2.metric("Promedio Crímenes / Alcaldía", f"{avg_crimes_per_alcaldia:.1f}")
c3.metric("Máximo Crímenes / Alcaldía", f"{max_crimes}")
c4.metric("Alcaldías", f"{len(fdf['alcaldia'].unique())}")

# KPI: Max Satisfaction
st.metric("🌟 Satisfacción Máxima", f"{max_crimes:.2f}")

# -----------------------------
# 4) Tabla + Gráfico (segunda fila)
# -----------------------------
tcol, gcol = st.columns([1, 2])
with tcol:
    st.subheader("Datos Filtrados")
    st.dataframe(fdf, use_container_width=True, hide_index=True)

with gcol:
    st.subheader("Crímenes por Curso")
    if chart_type == "Gráfico de Barras":
        fig = px.bar(
            fdf,
            x="Course", y="Students",
            color="Semester",  # Ahora color por Semester
            title="Crímenes por Curso (filtrado)",
            text="Students"
        )
    else:
        fig = px.line(
            fdf,
            x="Course", y="Students",
            color="Semester",
            title="Crímenes por Curso (filtrado)",
            markers=True
        )
    fig.update_layout(xaxis_tickangle=-30)
    st.plotly_chart(fig, use_container_width=True, key="chart1")

# Segundo gráfico: Comparar Satisfacción por Departamento
fig2 = px.box(
    fdf,
    x="Department",
    y="Satisfaction",
    color="Department",
    title="Satisfacción por Departamento"
)
st.plotly_chart(fig2, use_container_width=True, key="chart2")

# -----------------------------
# 5) Mini-preguntas
# -----------------------------
with st.expander("Bonus: Responde estas preguntas directamente en los inputs de Streamlit"):
    q1 = st.text_input("Q1) ¿Cuál alcaldía tiene el mayor número de crímenes bajo tu filtro actual?", key="q1")
    q2 = st.text_input("Q2) ¿Cuál es el curso más popular?", key="q2")
    q3 = st.text_area("Q3) Proporciona una idea accionable basada en los gráficos/KPIs:", key="q3")
st.caption("Consejo: Ajusta los filtros y lee los KPIs + gráficos para justificar tus respuestas.")

# -----------------------------
# 6) TODOs para la actividad
# -----------------------------
st.markdown(
    """
    ---
    ## Tus TODOs para esta actividad
    1. **Agrupar en el gráfico:** Modifica el gráfico de barras para colorear por **Alcaldía** en lugar de Departamento. Explica brevemente la diferencia que observas.
    2. **Nuevo KPI:** Agrega un KPI que muestre la **máxima satisfacción** en los datos filtrados.
    3. **Segundo gráfico:** Crea un nuevo gráfico (de barras o caja) para comparar **Satisfacción por Departamento** o **Crímenes por Alcaldía**.
    4. **Botón de radio:** Agrega un toggle para el tipo de gráfico: un botón de radio en la barra lateral donde los usuarios puedan elegir entre **Gráfico de Barras** y **Gráfico de Líneas**. Según la selección, actualiza la visualización principal (px.bar o px.line) para **Crímenes por Curso**.
    """
)

st.toast("¡App lista! Completa los TODOs en el código y actualiza.", icon="✅")
