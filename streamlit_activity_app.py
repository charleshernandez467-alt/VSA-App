import streamlit as st
import pandas as pd
import plotly.express as px

# Page Configuration
st.set_page_config(page_title="CDMX Crime Dashboard", layout="wide")

# -----------------------------
# 0) Title & Introduction
# -----------------------------
st.title("👮‍♂️ CDMX Crime Dashboard")
st.markdown(
    """
    **Goal:** Visualize crime data from Mexico City using Streamlit and official data.
    **Dataset:** Crime data from the **Mexico City Attorney General's Office** (FGJCDMX).
    """
)

# -----------------------------
# 1) Load Data
# -----------------------------
url = "https://raw.githubusercontent.com/charleshernandez467-alt/VSA-App/main/data/carpetasFGJ_acumulado_2025_01_.csv"
df = pd.read_csv(url)

# Show a preview of the data
st.subheader("Dataset Preview")
st.dataframe(df.head())

# -----------------------------
# 2) Filters in the Sidebar
# -----------------------------
st.sidebar.header("Filters")
# Crime type: include an "All" option so default is valid
crime_options = ["All"] + sorted(df["delito"].dropna().unique().tolist())
crime_type = st.sidebar.selectbox(
    "Crime Type", options=crime_options, index=0, key="crime_filter"
)
# Alcaldía multiselect: default to all (empty selection means show all)
alcaldia_options = sorted(df["alcaldia"].dropna().unique().tolist())
alcaldia_filter = st.sidebar.multiselect(
    "Select Alcaldía", options=alcaldia_options, default=None, key="alcaldia_filter"
)

# Filter data based on selections
filtered_df = df.copy()
# Apply crime_type filter only when a specific crime is selected
if crime_type and crime_type != "All":
    filtered_df = filtered_df[filtered_df["delito"] == crime_type]
# Apply alcaldia filter if the user selected one or more alcaldías
if alcaldia_filter:
    filtered_df = filtered_df[filtered_df["alcaldia"].isin(alcaldia_filter)]

# -----------------------------
# 3) KPIs (Key Performance Indicators)
# -----------------------------
c1, c2, c3 = st.columns(3)
# Total crimes is simply the number of rows in the filtered dataframe
total_crimes = int(len(filtered_df))
# Crimes per alcaldía (grouped counts)
if not filtered_df.empty and "alcaldia" in filtered_df.columns:
    counts_by_alcaldia = filtered_df.groupby("alcaldia")["delito"].count()
    avg_crimes_per_alcaldia = float(counts_by_alcaldia.mean())
    max_crimes = int(counts_by_alcaldia.max())
else:
    avg_crimes_per_alcaldia = 0.0
    max_crimes = 0

c1.metric("Total Crimes", f"{total_crimes:,}")
c2.metric("Avg. Crimes per Alcaldía", f"{avg_crimes_per_alcaldia:.1f}")
c3.metric("Max Crimes per Alcaldía", f"{max_crimes}")

# Additional KPI: Most frequent crime (guard for empty DF)
if not filtered_df.empty and "delito" in filtered_df.columns:
    try:
        most_freq = filtered_df['delito'].mode()[0]
    except Exception:
        most_freq = "N/A"
else:
    most_freq = "N/A"
st.metric("Most Frequent Crime", f"{most_freq}")

# -----------------------------
# 4) Visualizations (Charts)
# -----------------------------
st.subheader("🔴 Crimes by Alcaldía")
if not filtered_df.empty and "alcaldia" in filtered_df.columns:
    df_group = filtered_df.groupby("alcaldia")["delito"].count().reset_index(name="count")
    fig = px.bar(df_group, x="alcaldia", y="count", color="alcaldia", title="Crimes by Alcaldía")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No data available to show Crimes by Alcaldía.")

# Additional Graph: Satisfaction by Crime Type
st.subheader("📊 Satisfaction by Crime Type")
if "satisfaccion" in filtered_df.columns and not filtered_df.empty:
    fig2 = px.box(
        filtered_df,
        x="delito",
        y="satisfaccion",
        color="delito",
        title="Satisfaction by Crime Type"
    )
    st.plotly_chart(fig2, use_container_width=True)
else:
    st.info("Column 'satisfaccion' not found or no data available for Satisfaction chart.")

# -----------------------------
# 5) Filtered Data Table
# -----------------------------
st.subheader("Filtered Data")
st.dataframe(filtered_df, use_container_width=True)

# -----------------------------
# 6) Mini Questions (Bonus)
# -----------------------------
with st.expander("Bonus: Answer these directly in Streamlit text inputs"):
    q1 = st.text_input("Q1) Which alcaldía has the highest total enrollment under your current filter?", key="q1")
    q2 = st.text_input("Q2) Which single crime type is the most frequent?", key="q2")
    q3 = st.text_area("Q3) Propose one actionable insight based on the chart/KPIs:", key="q3")
st.caption("Tip: Adjust filters and read the KPIs and chart to justify your answers.")

# -----------------------------
# 7) Activity TODOs
# -----------------------------
st.markdown("""
    ---
    ## Your TODOs for this activity
    1. **Bar Chart Grouping**: Modify the bar chart to color by **Alcaldía** instead of Department. Briefly explain the difference you observe.
    2. **New KPI**: Add a KPI that shows the **max** number of crimes in the filtered data.
    3. **Second Chart**: Create a new chart (bar or box) to compare **Satisfaction by Crime Type** or **Crimes by Alcaldía**.
    4. **Chart Type Toggle**: Add a chart type toggle to choose between Bar Chart and Line Chart. Based on the selection, update the main visualization.
""")

st.toast("App ready — complete the TODOs in the code and refresh!", icon="✅")

