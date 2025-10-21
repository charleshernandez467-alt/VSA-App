"""
Streamlit Mini-Dashboard Activity
---------------------------------
Instructions (summarized):
1) Read the assignment sheet from CANVAS.
2) Run: streamlit run streamlit_activity_app.py
3) Complete each TODO step in this file and re-run.
"""
import streamlit as st
import pandas as pd
import plotly.express as px
st.set_page_config(page_title="Mini-Dashboard Activity", layout="wide")

# -----------------------------
# 0) Title & Intro
# -----------------------------
st.title("🎯 Mini-Dashboard: KPIs + Filters + Chart")
st.markdown(
"""
**Goal:** Build a tiny, interactive dashboard using Streamlit + pandas +
Plotly.
**Dataset:** Synthetic "Course Enrollments" across Departments.
"""
)

# -----------------------------
# 1) Data (pre-loaded)
# -----------------------------
df = pd.DataFrame({
    "Department": [
        "Finance","Finance","Finance",
        "Marketing","Marketing","Marketing",
        "Engineering","Engineering","Engineering"
    ],
    "Course": [
        "Intro Analytics", "Risk Models", "Financial Viz",
        "Marketing Basics", "Segmentation", "Campaigns",
        "Intro Robotics", "ML for Sensors", "Control Systems"
    ],
    "Students": [55, 38, 44, 60, 35, 42, 48, 51, 39],
    "Satisfaction": [4.2, 3.9, 4.1, 4.5, 4.0, 3.8, 4.3, 4.4, 4.1], # 1–5
    "Semester": ["A","A","B","A","B","B","A","A","B"]
})

# -----------------------------
# 2) Sidebar filters
# -----------------------------
st.sidebar.header("Filters")
dept = st.sidebar.multiselect(
    "Department", options=sorted(df["Department"].unique()), default=None, key="dept_filter"
)
sem = st.sidebar.multiselect(
    "Semester", options=sorted(df["Semester"].unique()), default=None, key="sem_filter"
)

# Radio button para tipo de gráfico
chart_type = st.sidebar.radio(
    "Chart type:",
    ["Bar Chart", "Line Chart"],
    key="chart_type_toggle"
)

fdf = df.copy()
if dept:
    fdf = fdf[fdf["Department"].isin(dept)]
if sem:
    fdf = fdf[fdf["Semester"].isin(sem)]

# -----------------------------
# 3) KPIs (top row)
# -----------------------------
c1, c2, c3, c4 = st.columns(4)
total_students = int(fdf["Students"].sum())
avg_class = float(fdf["Students"].mean()) if not fdf.empty else 0.0
avg_sat = float(fdf["Satisfaction"].mean()) if not fdf.empty else 0.0
num_courses = int(fdf["Course"].nunique())
max_sat = float(fdf["Satisfaction"].max()) if not fdf.empty else 0.0

c1.metric("Total Students", f"{total_students:,}")
c2.metric("Avg. Students / Course", f"{avg_class:.1f}")
c3.metric("Avg. Satisfaction", f"{avg_sat:.2f} / 5")
c4.metric("Courses", f"{num_courses}")

# KPI: Max Satisfaction
st.metric("🌟 Max Satisfaction", f"{max_sat:.2f}")

# -----------------------------
# 4) Table + Chart (second row)
# -----------------------------
tcol, gcol = st.columns([1,2])
with tcol:
    st.subheader("Filtered Data")
    st.dataframe(fdf, use_container_width=True, hide_index=True)

with gcol:
    st.subheader("Students by Course")
    # Gráfico principal: color por Semester y según radio button
    if chart_type == "Bar Chart":
        fig = px.bar(
            fdf,
            x="Course", y="Students",
            color="Semester", # ahora color por Semester
            title="Students per Course (filtered)",
            text="Students"
        )
    else:
        fig = px.line(
            fdf,
            x="Course", y="Students",
            color="Semester",
            title="Students per Course (filtered)",
            markers=True
        )
    fig.update_layout(xaxis_tickangle=-30)
    st.plotly_chart(fig, use_container_width=True, key="chart1")

# Segundo gráfico: Comparar Satisfaction por Department
fig2 = px.box(
    fdf,
    x="Department",
    y="Satisfaction",
    color="Department",
    title="Satisfaction by Department"
)
st.plotly_chart(fig2, use_container_width=True, key="chart2")

# -----------------------------
# 5) mini-questions
# -----------------------------
with st.expander(" Bonus: answer these directly in Streamlit text inputs"):
    q1 = st.text_input("Q1) Which department has the highest total enrollment under your current filter?", key="q1")
    q2 = st.text_input("Q2) Which single course is the most popular?", key="q2")
    q3 = st.text_area("Q3) Propose one actionable insight based on the chart/KPIs:", key="q3")
st.caption("Tip: adjust filters and read the KPIs + chart to justify your answers.")

# -----------------------------
# 6) TODOs for activity
# -----------------------------
st.markdown(
"""
---
## Your TODOs for this activity
1. **Chart grouping:** Modify the bar chart to color by **Semester** instead of
Department. Briefly explain the difference you observe.
2. **New KPI:** Add a KPI that shows the **max** satisfaction score in the
filtered data.
3. **Second chart:** Create a new chart (bar or box) to compare **Satisfaction
by Department** or **Students by Semester**.
4. **radio button:** Add a chart type toggle:Create a radio button in the
sidebar where students can choose between Bar Chart and Line Chart.
Based on the selection, update the main visualization
(px.bar or px.line) for Students per Course.
"""
)
st.toast("App ready — complete the TODOs in the code and refresh!", icon="✅")
