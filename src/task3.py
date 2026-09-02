import pandas as pd
import plotly.graph_objects as go

def build_task3(apps: pd.DataFrame):
    d=apps.copy()
    d=d[~d["App"].astype(str).str.upper().str.startswith(("X","Y","Z"))]
    d=d[d["Category"].astype(str).str.upper().str.startswith(("E","C","B"))]
    d=d[d["Reviews_Num"].gt(500)]
    d=d[~d["App"].astype(str).str.contains("S",case=False,na=False)]
    d["Month"]=d["Last Updated"].dt.to_period("M").dt.to_timestamp()
    g=d.groupby(["Month","Category"],as_index=False)["Installs_Num"].sum()
    g=g.sort_values(["Category","Month"])
    g["MoM_Growth"]=g.groupby("Category")["Installs_Num"].pct_change()
    return g
