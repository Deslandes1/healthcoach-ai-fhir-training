import streamlit as st
import re
from groq import Groq
from datetime import datetime

# ================== CONFIGURATION ==================
st.set_page_config(
    page_title="HealthCoach AI | GlobalInternet.py",
    page_icon="🏥",
    layout="wide"
)

# Language texts (pricing removed)
TEXTS = {
    "English": {
        "title": "🏥 HealthCoach AI – FHIR Practice Arena",
        "subtitle": "Master healthcare interoperability with AI coaching",
        "video_tab": "🎬 Video Introduction",
        "practice_tab": "📝 Practice Problem",
        "ai_tab": "🤖 AI Coach",
        "doc_tab": "📚 Documentation",
        "video_title": "Watch the full introduction video",
        "video_desc": "This video explains how to use the platform and how the AI coach helps you learn FHIR.",
        "problem_title": "FHIR Problem: Calculate Patient Age",
        "problem_statement": """
You are given a FHIR Patient resource in JSON format. Your task is to write a function that extracts the patient's birth date and calculates their age in years as of today.

**Example FHIR Patient resource (JSON):**
{
  "resourceType": "Patient",
  "birthDate": "1990-03-15",
  "name": [{"given": ["John"], "family": "Doe"}]
}

**Expected output:** Age in whole years (e.g., 36).

Write your solution in Python. Use the `datetime` module.
""",
        "test_input": "Enter FHIR Patient JSON or paste birth date (YYYY-MM-DD):",
        "run_button": "Run & Check Solution",
        "result_correct": "✅ Correct! Age is **{}** years.",
        "result_wrong": "❌ Your code returned {}, but the correct age is {}. Debug with AI Coach.",
        "hint_placeholder": "Paste your code or describe your algorithm idea...",
        "hint_button": "Get AI Feedback",
        "ai_thinking": "AI is analyzing your approach...",
        "ai_error": "AI error: {}",
        "sidebar_howto": "How to use",
        "howto_list": ["Watch the video intro", "Read the Documentation tab", "Solve the FHIR practice problem", "Ask AI Coach for feedback"],
        "footer": "© 2026 GlobalInternet.py – AI for FHIR Education",
        "security_badge": "🔐 End‑to‑end encryption active",
        "security_caption": "All data is secured and anonymized",
        "doc_title": "Complete Documentation",
        "doc_prereq": "Prerequisites",
        "doc_prereq_text": """
- Python 3.8 or higher
- Required Python packages: streamlit, groq, datetime (built-in)
- A Groq API key (sign up at groq.com)
- Internet connection for video streaming
""",
        "doc_start": "How to Start",
        "doc_start_text": """
1. Clone the repository: `git clone https://github.com/Deslandes1/healthcoach-ai-fhir-training.git`
2. Install dependencies: `pip install -r requirements.txt` (or `pip install streamlit groq`)
3. Create a `.streamlit/secrets.toml` file with your Groq API key:
