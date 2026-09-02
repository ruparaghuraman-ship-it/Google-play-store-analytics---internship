import pandas as pd
import plotly.graph_objects as go

def build_task6(apps: pd.DataFrame):
    d=apps.copy()
    d=d[d["Installs_Num"].lt(10000)&d["Revenue"].lt(10000)]
    android=pd.to_numeric(d["Android Ver"].astype(str).str.extract(
        r"([0-9]+(?:\.[0-9]+)?)")[0],errors="coerce")
    d=d[android.gt(4)&d["Size_MB"].gt(15)&
        d["Content Rating"].eq("Everyone")&
        d["App"].astype(str).str.len().le(30)]
    top=d.groupby("Category")["Installs_Num"].sum().nlargest(3).index
    d=d[d["Category"].isin(top)]
    g=d.groupby("Type",as_index=False).agg(
        Average_Installs=("Installs_Num","mean"),Revenue=("Revenue","sum"))
    fig=go.Figure()
    fig.add_bar(x=g["Type"],y=g["Average_Installs"],name="Average Installs")
    fig.add_scatter(x=g["Type"],y=g["Revenue"],name="Revenue",
                    mode="lines+markers",yaxis="y2")
    fig.update_layout(title="Task 6 — Average Installs vs Revenue",
                      yaxis_title="Average Installs",
                      yaxis2=dict(title="Revenue ($)",overlaying="y",side="right"))
    return fig,d
