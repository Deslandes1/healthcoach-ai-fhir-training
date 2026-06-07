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

# Language texts
TEXTS = {
    "English": {
        "title": "🏥 HealthCoach AI – FHIR Practice Arena",
        "subtitle": "Master healthcare interoperability with AI coaching",
        "video_tab": "🎬 Video Introduction",
        "practice_tab": "📝 Practice Problem",
        "ai_tab": "🤖 AI Coach",
        "video_title": "Watch the full introduction video",
        "video_desc": "This video explains how to use the platform and how the AI coach helps you learn FHIR.",
        "problem_title": "FHIR Problem: Calculate Patient Age",
        "problem_statement": """You are given a FHIR Patient resource in JSON format. Your task is to write a function that extracts the patient's birth date and calculates their age in years as of today.

**Example FHIR Patient resource:**
```json
{
  "resourceType": "Patient",
  "birthDate": "1990-03-15",
  "name": [{"given": ["John"], "family": "Doe"}]
}
