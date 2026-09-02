"""Task 1: filtered Plotly bubble chart.

The task is intentionally kept separate from the main dashboard and is gated to
5:00 PM–7:00 PM IST when rendered through the helper below.
"""

from datetime import datetime, time
from zoneinfo import ZoneInfo

import pandas as pd
import plotly.express as px

CATEGORIES = {
    "GAME",
    "BEAUTY",
    "BUSINESS",
    "COMICS",
    "COMMUNICATION",
    "DATING",
    "ENTERTAINMENT",
    "SOCIAL",
}

# Required display translations from the internship brief.
CATEGORY_LABELS = {
    "BEAUTY": "सुंदरता",       # Hindi
    "BUSINESS": "வணிகம்",      # Tamil
    "DATING": "Partnersuche",  # German
}

IST = ZoneInfo("Asia/Kolkata")
TASK_START = time(17, 0)
TASK_END = time(19, 0)


def is_task1_window(now: datetime | None = None) -> bool:
    """Return True only during 5:00 PM inclusive to 7:00 PM exclusive IST."""
    if now is None:
        now = datetime.now(IST)
    elif now.tzinfo is None:
        now = now.replace(tzinfo=IST)
    else:
        now = now.astimezone(IST)
    return TASK_START <= now.time() < TASK_END


def prepare_task1(apps: pd.DataFrame, reviews: pd.DataFrame) -> pd.DataFrame:
    """Apply every Task 1 filter and return chart-ready rows.

    Subjectivity is aggregated per app because the Play Store dataset is
    app-level while User Reviews contains multiple review records per app.
    """
    subjectivity = (
        reviews.groupby("App", as_index=False)["Sentiment_Subjectivity"]
        .mean()
        .rename(columns={"Sentiment_Subjectivity": "Mean_Subjectivity"})
    )

    d = apps.merge(subjectivity, on="App", how="left")
    d["Category"] = d["Category"].astype(str)
    d["App"] = d["App"].astype(str)

    d = d[
        d["Rating_Num"].gt(3.5)
        & d["Reviews_Num"].gt(500)
        & d["Installs_Num"].gt(50_000)
        & d["Category"].str.upper().isin(CATEGORIES)
        # The brief says the app name must not contain the letter "S";
        # treating it case-insensitively is the safer interpretation.
        & ~d["App"].str.contains("S", case=False, na=False)
        & d["Mean_Subjectivity"].gt(0.5)
        & d["Size_MB"].notna()
    ].copy()

    d["Category_Display"] = (
        d["Category"].str.upper().map(CATEGORY_LABELS).fillna(d["Category"])
    )
    return d


def build_task1(apps: pd.DataFrame, reviews: pd.DataFrame):
    """Build the Task 1 bubble chart and return (figure, filtered_data)."""
    d = prepare_task1(apps, reviews)

    fig = px.scatter(
        d,
        x="Size_MB",
        y="Rating_Num",
        size="Installs_Num",
        color="Category_Display",
        hover_name="App",
        hover_data={
            "Category_Display": True,
            "Size_MB": ":.2f",
            "Rating_Num": ":.2f",
            "Installs_Num": ":,",
            "Reviews_Num": ":,",
            "Mean_Subjectivity": ":.2f",
        },
        title="Task 1 — App Size vs Average Rating",
        labels={
            "Size_MB": "App Size (MB)",
            "Rating_Num": "Average Rating",
            "Installs_Num": "Number of Installs",
            "Category_Display": "Category",
            "Mean_Subjectivity": "Average Review Subjectivity",
        },
    )

    # The requirement explicitly calls for the Game category in pink.
    for trace in fig.data:
        if str(trace.name).upper() == "GAME":
            trace.marker.color = "pink"

    return fig, d


def task1_available_message(now: datetime | None = None) -> str:
    """Return the UI message for the required access window."""
    if is_task1_window(now):
        return "Task 1 is available (5:00 PM–7:00 PM IST)."
    return "Task 1 is hidden outside its required 5:00 PM–7:00 PM IST window."
