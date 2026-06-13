# 🧠 AI Resume & Job Description Matcher

An AI-powered tool that compares your resume against a job description, calculates an ATS match score, identifies missing keywords, and suggests improved resume bullet points — built using prompt engineering and OpenAI's API.

## 🚀 Features
- Extracts key skills/requirements from any job description using LLM prompts
- Calculates an ATS-style match score between resume and JD
- Highlights matched vs missing keywords
- Generates improved, keyword-optimized resume bullet points
- Simple, interactive Streamlit UI

## 🛠️ Tech Stack
- Python
- OpenAI API (GPT-4o-mini)
- Streamlit
- pdfplumber
- Prompt Engineering (structured JSON prompts, few-shot style instructions)

## 🧩 Prompt Engineering Approach
This project separates prompts into modular `.txt` templates under `/prompts`:
- `extract_keywords.txt` — extracts structured skill data from job descriptions
- `match_score.txt` — performs semantic comparison and scoring, returns strict JSON
- `rewrite_bullets.txt` — generates tailored resume improvements based on gaps

Each prompt enforces output format (JSON/lists) to ensure reliable parsing — a key prompt engineering technique for production LLM apps.

## ⚙️ Setup

1. Clone the repo
```bash
git clone https://github.com/yourusername/resume-matcher-ai.git
cd resume-matcher-ai
```

2. Create virtual environment & install dependencies
```bash
python -m venv venv
source venv/bin/activate   # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

3. Add your API key
```bash
cp .env.example .env
# then add your OpenAI API key inside .env
```

4. Run the app
```bash
streamlit run app/main.py
```

## 📈 Future Improvements
- Support for .docx resumes
- Cover letter generator
- Multi-LLM support (Claude, Gemini)
- Export optimized resume as PDF
