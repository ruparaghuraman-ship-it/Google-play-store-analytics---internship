import pandas as pd
import plotly.express as px

EXCLUDED_PREFIXES = ("A","C","G","S")

def build_task2(apps: pd.DataFrame):
    d = apps.copy()
    d = d[d["Installs_Num"].gt(1_000_000)]
    d = d[~d["Category"].astype(str).str.upper().str.startswith(EXCLUDED_PREFIXES)]
    top5 = d.groupby("Category", as_index=False)["Installs_Num"].sum().nlargest(5,"Installs_Num")
    # The source dataset has no country column. This function therefore prepares
    # the category-level top-five data without inventing geographic observations.
    return top5
