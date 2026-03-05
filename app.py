import streamlit as st
import pandas as pd
from utils import extract_text_from_pdf, rank_resumes

st.title("AI Resume Ranking System")

st.write("Upload resumes and rank them according to job description")

# JOB DESCRIPTION INPUT
job_description = st.text_area("Enter Job Description")

# FILE UPLOAD
uploaded_files = st.file_uploader(
    "Upload Resumes (PDF)",
    accept_multiple_files=True,
    type=["pdf"]
)

# BUTTON
if st.button("Rank Resumes"):

    if job_description == "":
        st.warning("Please enter job description")

    elif uploaded_files is None:
        st.warning("Please upload resumes")

    else:

        resume_texts = []
        resume_names = []

        for file in uploaded_files:
            text = extract_text_from_pdf(file)
            resume_texts.append(text)
            resume_names.append(file.name)

        scores = rank_resumes(job_description, resume_texts)

        data = pd.DataFrame({
            "Resume": resume_names,
            "Score": scores
        })

        data = data.sort_values(by="Score", ascending=False)

        st.subheader("Ranking Results")
        st.dataframe(data)

        st.bar_chart(data.set_index("Resume"))
