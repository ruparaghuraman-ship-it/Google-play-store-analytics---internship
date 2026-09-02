import streamlit as st
from src.data_cleaning import load_data
from src.task1 import build_task1, is_task1_window, task1_available_message

st.set_page_config(page_title="Google Play Store Analytics",layout="wide")
st.title("Google Play Store Analytics — Internship")
st.write("Training-project dataset with six task-specific analytics workflows.")

apps, reviews = load_data()
st.metric("Apps", f"{len(apps):,}")
st.metric("Reviews", f"{len(reviews):,}")

st.info("Task visualizations are exposed separately according to their required IST access windows and are not automatically placed in the main dashboard.")

# ── Task 1 ────────────────────────────────────────────────────────────────────
st.header("Task 1 — Filtered Bubble Chart")

if is_task1_window():
    fig, filtered = build_task1(apps, reviews)
    st.plotly_chart(fig, use_container_width=True)
    st.caption(f"{len(filtered)} apps matched the Task 1 filters.")
else:
    st.warning(task1_available_message())
