import streamlit as st
import pandas as pd
import plotly.express as px

from utils import extract_text_from_pdf, rank_resumes

st.set_page_config(page_title="AI Resume Ranker", layout="wide")

st.title("🤖 AI Resume Ranking System")

job_description = st.text_area("Paste Job Description")

uploaded_files = st.file_uploader(
    "Upload Resumes (PDF)",
    accept_multiple_files=True
)

if st.button("Rank Resumes"):

    if job_description and uploaded_files:

        resume_texts = []
        names = []

        for file in uploaded_files:
            text = extract_text_from_pdf(file)
            resume_texts.append(text)
            names.append(file.name)

        scores = rank_resumes(job_description, resume_texts)

        df = pd.DataFrame({
            "Resume": names,
            "Match Score": scores
        })

        df = df.sort_values(by="Match Score", ascending=False)

        st.subheader("🏆 Resume Ranking")

        st.dataframe(df)

        # chart
        fig = px.bar(
            df,
            x="Resume",
            y="Match Score",
            color="Match Score",
            title="Resume Matching Score"
        )

        st.plotly_chart(fig, use_container_width=True)
