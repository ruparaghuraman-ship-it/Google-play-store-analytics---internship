import pandas as pd
import plotly.express as px

CATEGORIES = {
    "GAME","BEAUTY","BUSINESS","COMICS",
    "COMMUNICATION","DATING","ENTERTAINMENT","SOCIAL"
}

def build_task1(apps: pd.DataFrame, reviews: pd.DataFrame):
    r = reviews.groupby("App", as_index=False)["Sentiment_Subjectivity"].mean()
    r = r.rename(columns={"Sentiment_Subjectivity":"Mean_Subjectivity"})
    d = apps.merge(r, on="App", how="left")
    d = d[
        d["Rating_Num"].gt(3.5)
        & d["Reviews_Num"].gt(500)
        & d["Installs_Num"].gt(50000)
        & d["Category"].astype(str).str.upper().isin(CATEGORIES)
        & ~d["App"].astype(str).str.contains("S", case=False, na=False)
        & d["Mean_Subjectivity"].gt(0.5)
    ].copy()
    fig = px.scatter(
        d, x="Size_MB", y="Rating_Num", size="Installs_Num",
        color="Category", hover_name="App",
        title="Task 1 — App Size vs Average Rating",
        labels={"Size_MB":"App Size (MB)","Rating_Num":"Average Rating",
                "Installs_Num":"Number of Installs"}
    )
    for trace in fig.data:
        if str(trace.name).upper() == "GAME":
            trace.marker.color = "pink"
    return fig, d
