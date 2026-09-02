import pandas as pd
import plotly.express as px

def build_task4(apps: pd.DataFrame):
    d=apps.copy()
    d=d[d["Rating_Num"].ge(4)]
    d=d[~d["App"].astype(str).str.contains(r"\d",regex=True,na=False)]
    d=d[d["Category"].astype(str).str.upper().str.startswith(("T","P"))]
    d=d[d["Reviews_Num"].gt(1000)]
    d=d[d["Size_MB"].between(20,80,inclusive="both")]
    d["Month"]=d["Last Updated"].dt.to_period("M").dt.to_timestamp()
    g=d.groupby(["Month","Category"],as_index=False)["Installs_Num"].sum()
    return px.area(g,x="Month",y="Installs_Num",color="Category",
                   title="Task 4 — Cumulative Installs by Category"), g
