import PyPDF2
from openai import OpenAI
from sklearn.metrics.pairwise import cosine_similarity
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def extract_text_from_pdf(uploaded_file):
    text = ""
    pdf = PyPDF2.PdfReader(uploaded_file)

    for page in pdf.pages:
        if page.extract_text():
            text += page.extract_text()

    return text


def get_embedding(text):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )

    return response.data[0].embedding


def rank_resumes(job_desc, resumes):

    job_embedding = get_embedding(job_desc)

    resume_embeddings = []

    for resume in resumes:
        resume_embeddings.append(get_embedding(resume))

    scores = cosine_similarity(
        [job_embedding],
        resume_embeddings
    )[0]

    return scores