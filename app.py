from __future__ import annotations

from pathlib import PurePosixPath

import pandas as pd
import streamlit as st

from storage_utils import build_zip, format_bytes, get_file_category


st.set_page_config(
    page_title="iCloud File Organizer",
    page_icon="☁️",
    layout="wide",
)

st.title("iCloud File Organizer")
st.caption("Review files you export from iCloud Drive and download a selection to your device.")

st.info(
    "This app does not connect to iCloud or change anything in your Apple account. "
    "First download files from iCloud.com, then upload them here. Downloads are saved "
    "through your browser. Files uploaded to a hosted app are processed on that host, "
    "so avoid uploading sensitive files."
)

uploaded_files = st.file_uploader(
    "Upload files exported from iCloud Drive",
    accept_multiple_files=True,
    help="Choose files you previously downloaded from iCloud Drive.",
)

if not uploaded_files:
    st.markdown(
        "### Getting started\n"
        "1. Open [iCloud.com](https://www.icloud.com/) and download files from iCloud Drive.\n"
        "2. Upload those files above to review their names, types, and sizes.\n"
        "3. Select files and download them individually or together as a ZIP."
    )
    st.stop()

records = []
for index, uploaded_file in enumerate(uploaded_files):
    file_bytes = uploaded_file.getvalue()
    records.append(
        {
            "id": str(index),
            "name": PurePosixPath(uploaded_file.name.replace("\\", "/")).name,
            "category": get_file_category(uploaded_file.name),
            "size": len(file_bytes),
            "data": file_bytes,
        }
    )

total_size = sum(record["size"] for record in records)
metric_columns = st.columns(2)
metric_columns[0].metric("Files uploaded", len(records))
metric_columns[1].metric("Total size", format_bytes(total_size))

categories = sorted({record["category"] for record in records})
selected_categories = st.multiselect(
    "Filter by file type",
    options=categories,
    default=categories,
)
search = st.text_input("Search file names").strip().casefold()

filtered_records = [
    record
    for record in records
    if record["category"] in selected_categories
    and search in record["name"].casefold()
]

st.subheader("Files")
if filtered_records:
    st.dataframe(
        pd.DataFrame(
            [
                {
                    "File name": record["name"],
                    "Type": record["category"],
                    "Size": format_bytes(record["size"]),
                }
                for record in filtered_records
            ]
        ),
        hide_index=True,
        use_container_width=True,
    )

    labels = {
        f'{record["id"]} · {record["name"]}': record for record in filtered_records
    }
    selected_labels = st.multiselect(
        "Choose files to download",
        options=list(labels),
    )

    if selected_labels:
        selected_records = [labels[label] for label in selected_labels]
        zip_data = build_zip(
            (record["name"], record["data"]) for record in selected_records
        )
        st.download_button(
            "Download selection as ZIP",
            data=zip_data,
            file_name="icloud-files.zip",
            mime="application/zip",
            use_container_width=True,
        )

    single_label = st.selectbox(
        "Or download one file",
        options=[""] + list(labels),
        format_func=lambda label: "Choose a file..." if not label else label,
    )
    if single_label:
        record = labels[single_label]
        st.download_button(
            "Download selected file",
            data=record["data"],
            file_name=record["name"],
            mime="application/octet-stream",
            key="download_single_file",
        )
else:
    st.warning("No uploaded files match the current filters.")

st.caption(
    "This is a temporary organizer, not an iCloud sync or storage-cleanup tool. "
    "It does not delete files from iCloud, and uploaded files are not retained by "
    "this app after the session ends."
)
