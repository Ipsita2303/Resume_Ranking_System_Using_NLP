import os
from openai import OpenAI
import numpy as np
import PyPDF2

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text


def get_embedding(text):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding


def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)
    return np.dot(a,b) / (np.linalg.norm(a) * np.linalg.norm(b))


def rank_resumes(job_description, resume_texts):
    job_embedding = get_embedding(job_description)

    scores = []

    for text in resume_texts:
        resume_embedding = get_embedding(text)
        score = cosine_similarity(job_embedding, resume_embedding)
        scores.append(score)

    return scores
