import streamlit as st
import json
import os
from dotenv import load_dotenv
from openai import OpenAI
from utils.pdf_reader import extract_text_from_pdf

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(page_title="AI Resume Matcher", page_icon="🧠", layout="centered")
st.title("🧠 AI Resume & Job Description Matcher")
st.write("Upload your resume and paste a job description to get an ATS match score and improvement suggestions.")

def load_prompt(filename, **kwargs):
    with open(f"prompts/{filename}", "r") as f:
        template = f.read()
    return template.format(**kwargs)

def call_llm(prompt, model="gpt-4o-mini"):
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    return response.choices[0].message.content

resume_file = st.file_uploader("Upload your Resume (PDF)", type=["pdf"])
job_description = st.text_area("Paste the Job Description here", height=200)

if st.button("Analyze") and resume_file and job_description:
    with st.spinner("Extracting resume text..."):
        resume_text = extract_text_from_pdf(resume_file)

    with st.spinner("Extracting keywords from job description..."):
        kw_prompt = load_prompt("extract_keywords.txt", job_description=job_description)
        keywords_raw = call_llm(kw_prompt)
        try:
            keywords = json.loads(keywords_raw)
        except:
            keywords = [keywords_raw]

    st.subheader("📌 Key Skills from Job Description")
    st.write(", ".join(keywords))

    with st.spinner("Calculating match score..."):
        score_prompt = load_prompt("match_score.txt", keywords=json.dumps(keywords), resume_text=resume_text)
        score_raw = call_llm(score_prompt)
        try:
            score_data = json.loads(score_raw)
        except:
            score_data = {"score": "N/A", "matched_keywords": [], "missing_keywords": []}

    st.subheader("📊 Match Score")
    st.metric("ATS Match Score", f"{score_data.get('score', 'N/A')}/100")

    col1, col2 = st.columns(2)
    with col1:
        st.write("✅ Matched Keywords")
        st.write(score_data.get("matched_keywords", []))
    with col2:
        st.write("❌ Missing Keywords")
        st.write(score_data.get("missing_keywords", []))

    if score_data.get("missing_keywords"):
        with st.spinner("Generating improved bullet points..."):
            rewrite_prompt = load_prompt(
                "rewrite_bullets.txt",
                missing_keywords=", ".join(score_data.get("missing_keywords", [])),
                resume_text=resume_text
            )
            suggestions = call_llm(rewrite_prompt)

        st.subheader("✍️ Suggested Resume Bullet Points")
        st.write(suggestions)
