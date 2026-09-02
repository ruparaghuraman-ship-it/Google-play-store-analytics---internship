import pandas as pd
import plotly.express as px

def build_task5(apps: pd.DataFrame):
    d=apps.copy()
    d=d[d["Rating_Num"].ge(4)&d["Size_MB"].lt(10)]
    d=d[d["Last Updated"].dt.month.eq(1)]
    top=d.groupby("Category",as_index=False).agg(
        Installs=("Installs_Num","sum"),
        Average_Rating=("Rating_Num","mean"),
        Total_Reviews=("Reviews_Num","sum")
    ).nlargest(10,"Installs")
    long=top.melt(id_vars="Category",
                  value_vars=["Average_Rating","Total_Reviews"],
                  var_name="Metric",value_name="Value")
    return px.bar(long,x="Category",y="Value",color="Metric",barmode="group",
                  title="Task 5 — Rating and Reviews for Top Categories"), top
