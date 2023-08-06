import inspect
import os
import sys
from pathlib import Path

import pandas as pd

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

import streamlit as st

currentdir = os.path.dirname(
    os.path.abspath(inspect.getfile(inspect.currentframe()))
)

path = Path(currentdir).parent.parent

parentdir = os.path.dirname(str(path))
sys.path.insert(0, parentdir)

from preservationdatabase import exporter

import boto3
import logging

s3client = boto3.client("s3")
session = boto3.Session()
s3 = session.resource("s3")

members = exporter.get_all_members_api()

output = []

for member, data in members.items():
    output.append(f"{member} ({data})")

options = st.multiselect(
    "Please select some Crossref members",
    output,
)

from preservationdatabase import environment
from preservationdatabase import settings

os.environ["DJANGO_SETTINGS_MODULE"] = "settings"
environment.setup_environment(code_bucket=None, download_settings=False)

from preservationdatabase import constants

archives = [archive.name() for archive in constants.archives.values()]

member_info = []

grades = {}

for member in options:
    member_id = member.split(" ")[0]

    preservations = exporter.get_annotation(
        s3client=None,
        annotations_bucket=ANNOTATION_BUCKET,
        annotations_path=ANNOTATION_PATH,
        member_id=member_id,
        annotation_name="preservation.json",
    )

    grades[member] = preservations

    member_archives = []

    for archive in archives:
        member_info.append(
            pd.DataFrame(
                {
                    "Archive": [archive],
                    "Member": [member],
                    "Preserved Items": [int(preservations[archive])],
                }
            )
        )

if len(member_info) > 0:
    final_dataframe = pd.concat(
        member_info,
    )

    import altair as alt

    chart = (
        alt.Chart(final_dataframe)
        .mark_bar()
        .encode(
            x="Member:N",
            y="Preserved Items:Q",
            column="Archive:N",
            color="Member:N",
        )
        .interactive()
    )

    st.header("Absolute Preservation Numbers")
    st.altair_chart(chart, theme="streamlit", use_container_width=False)

    st.header("Percentage Preserved In Each Archive")

    chart_two = (
        alt.Chart(final_dataframe)
        .transform_joinaggregate(
            TotalPreserved="sum(Preserved Items)", groupby=["Member"]
        )
        .transform_calculate(
            PercentagePreserved="(datum['Preserved Items'] / "
            "datum.TotalPreserved) * 100"
        )
        .mark_bar()
        .encode(
            x="Member:N",
            y="PercentagePreserved:Q",
            column="Archive:N",
            color="Member:N",
        )
        .interactive()
    )

    st.altair_chart(chart_two, theme="streamlit", use_container_width=False)

    st.header("Member Grades and Information")

    for key, val in grades.items():
        st.subheader(key)

        percent_unpreserved = str(
            round(val["unpreserved-count"] / val["sample-count"] * 100, 2)
        )

        percent_in_one_archive = str(
            round(
                val["preserved-in-one-archive"] / val["sample-count"] * 100, 2
            )
        )

        percent_in_two_archives = str(
            round(
                val["preserved-in-two-archives"] / val["sample-count"] * 100, 2
            )
        )

        percent_in_three_or_more_archives = str(
            round(
                val["preserved-in-three-or-more-archives"]
                / val["sample-count"]
                * 100,
                2,
            )
        )

        st.write(
            f"This member had {val['sample-count']} samples in the '{val['about']['sample-file']}' directory. We excluded {val['excluded-non-journal']} works that were not journal articles in the sampling. We found {val['unpreserved-count']} unpreserved works ({percent_unpreserved}%), {val['preserved-in-one-archive']} works preserved in just one archive ({percent_in_one_archive}%), {val['preserved-in-two-archives']} works preserved in two archives ({percent_in_two_archives}%), and {val['preserved-in-three-or-more-archives']} works preserved in three or more archives ({percent_in_three_or_more_archives}%). As a result, this member was scored: '[{val['member-grade']}](/Grading_System)'."
        )

    st.header("Dataset")
    st.write(final_dataframe)
