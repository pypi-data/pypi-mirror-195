SAMPLES_BUCKET = "samples-crossref-research"
SAMPLES_PATH = "members-works/sample-2023-01-21/works/"

ANNOTATION_BUCKET = "outputs.research.crossref.org"
ANNOTATION_PATH = "annotations"
ANNOTATION_FILENAME = "preservation.json"

REPORT_BUCKET = "outputs.research.crossref.org"
REPORT_PATH = "reports"
REPORT_FILENAME = "preservation.json"

CODE_BUCKET = "airflow-crossref-research-annotation"

PARALLEL_JOBS = 5

member_tier_names = [
    "<USD 1 million",
    "USD 1 million - USD 5 million",
    "USD 5 million - USD 10 million",
    "USD 10 million - USD 25 million",
    "USD 25 million - USD 50 million",
    "USD 50 million - USD 100 million",
    "USD 100 million - USD 200 million",
    "USD 200 million - USD 500 million",
    ">USD 500 million",
]


def get_report(s3client, report_bucket, report_path, report_name):
    key = f"{report_path}/{report_name}"

    data = (
        s3client.get_object(Bucket=report_bucket, Key=key)["Body"]
        .read()
        .decode("utf-8")
    )

    from io import StringIO
    import logging
    import json

    with StringIO(data) as json_file:
        output = json.loads(json_file.read())
        return output


import boto3
import logging

s3client = boto3.client("s3")
session = boto3.Session()
s3 = session.resource("s3")

import streamlit as st
import numpy as np


import matplotlib.pyplot as plt
import matplotlib.colors as mcolors


report = get_report(
    s3client=s3client,
    report_bucket=REPORT_BUCKET,
    report_path=REPORT_PATH,
    report_name="preservation.json",
)

# Pie chart, where the slices will be ordered and plotted counter-clockwise:
labels = (
    f"Gold (75% in 3 or more archives) [{report['gold-totals']} members]",
    f"Silver (50% in 2 archives) [{report['silver-totals']} members]",
    f"Bronze (25% in 1 archive) [{report['bronze-totals']} members]",
    f"Unclassified (no archival status) [{report['unclassified-totals']} members]",
)
sizes = [
    report["gold-totals"],
    report["silver-totals"],
    report["bronze-totals"],
    report["unclassified-totals"],
]

colors = [
    mcolors.CSS4_COLORS["gold"],
    mcolors.CSS4_COLORS["silver"],
    mcolors.CSS4_COLORS["tan"],
    mcolors.CSS4_COLORS["lightcyan"],
]

import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Create subplots: use 'domain' type for Pie subplot
fig = make_subplots(
    rows=1, cols=2, specs=[[{"type": "domain"}, {"type": "domain"}]]
)
fig.add_trace(
    go.Pie(
        labels=labels,
        values=sizes,
        name="Preservation Status",
        marker_colors=colors,
    ),
    1,
    1,
)

# Use `hole` to create a donut-like pie chart
fig.update_traces(hole=0.4, hoverinfo="label+percent+name")

# now build the types of preservation status

import pandas as pd

gold_data = pd.DataFrame(
    {
        "Member Classes": member_tier_names,
        "Number of Members": [i for i in report["gold-members"].values()],
    }
)

silver_data = pd.DataFrame(
    {
        "Member Classes": member_tier_names,
        "Number of Members": [i for i in report["silver-members"].values()],
    }
)

bronze_data = pd.DataFrame(
    {
        "Member Classes": member_tier_names,
        "Number of Members": [i for i in report["bronze-members"].values()],
    }
)

unclassified_data = pd.DataFrame(
    {
        "Member Classes": member_tier_names,
        "Number of Members": [
            i for i in report["unclassified-members"].values()
        ],
    }
)

data_set = [gold_data, silver_data, bronze_data, unclassified_data]
class_labels = ["Gold", "Silver", "Bronze", "Unclassified"]

st.set_page_config(
    page_title="Overall Report",
    page_icon="👋",
)


st.title("Crossref Labs Preservation Report")
st.header("All Members Preservation Grades")

st.plotly_chart(fig, use_container_width=False)


for label, data in zip(class_labels, data_set):
    st.header(f"{label} Members Preservation Grades")
    st.bar_chart(data, x="Member Classes", y="Number of Members")
