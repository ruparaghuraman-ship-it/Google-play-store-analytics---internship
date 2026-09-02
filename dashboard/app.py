import streamlit as st
from src.data_cleaning import load_data

st.set_page_config(page_title="Google Play Store Analytics",layout="wide")
st.title("Google Play Store Analytics — Internship")
st.write("Training-project dataset with six task-specific analytics workflows.")

apps, reviews = load_data()
st.metric("Apps", f"{len(apps):,}")
st.metric("Reviews", f"{len(reviews):,}")

st.info("Task visualizations are exposed separately according to their required IST access windows and are not automatically placed in the main dashboard.")
