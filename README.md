# 🏥 HealthCoach AI – FHIR Practice Arena

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://healthcoach-ai-fhir-training-uzdeefhyupvfjkywurau6w.streamlit.app/)
[![Made with Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![Groq AI](https://img.shields.io/badge/Groq-LLM-purple.svg)](https://groq.com)

**HealthCoach AI** is an interactive, AI‑powered training platform for healthcare developers and interoperability professionals. It helps you master FHIR (Fast Healthcare Interoperability Resources) through a hands‑on practice problem and an intelligent AI coach that gives instant feedback on your code.

Built by **Gesner Deslandes**, Engineer‑in‑Chief at **GlobalInternet.py**.

🔗 **Live Demo:** [https://healthcoach-ai-fhir-training-uzdeefhyupvfjkywurau6w.streamlit.app/](https://healthcoach-ai-fhir-training-uzdeefhyupvfjkywurau6w.streamlit.app/)

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🎬 **Video Introduction** | A narrated walkthrough (male AI voice) explaining the entire platform. |
| 📝 **Practice Problem** | Calculate patient age from a FHIR Patient JSON resource. Users write code, run it, and get instant validation. |
| 🤖 **AI Coach** | Paste your code or describe your algorithm – the AI (Groq Llama 3.1) provides constructive feedback, efficiency tips, and FHIR best practices. |
| 🌐 **Multilingual UI** | Switch between **English**, **Français**, and **Español** – all text, prompts, and AI responses adapt. |
| 🛡️ **Global Security Shield** | Visual badge indicating end‑to‑end encryption. User data is anonymized and secured. |
| 💰 **Pricing & Contact** | Clear one‑time license fees and contact information in the sidebar. |

---

## 🧠 How It Works

1. **Practice Problem Tab** – You are given a FHIR Patient resource in JSON. Your task is to write a Python function that extracts the birth date and returns the age in years.  
   - Input example: `{"resourceType":"Patient","birthDate":"1990-03-15"}`  
   - Click **Run & Check Solution** – the app calculates the correct age using the `datetime` module.

2. **AI Coach Tab** – Paste your code (e.g., a nested‑loop O(n²) solution) or describe your approach.  
   - Click **Get AI Feedback** – the AI coach instantly replies with:  
     - Correctness check  
     - Efficiency analysis (e.g., suggests O(n log n) solution)  
     - Edge case handling (missing fields, invalid dates)  
     - FHIR best practices  

3. **Sidebar** – Change language, view the security badge, see pricing, and get in touch.

---

## 🛠️ Tech Stack

- **Frontend & Deployment**: [Streamlit](https://streamlit.io)
- **AI Model**: [Groq](https://groq.com) – Llama 3.1 8B (via Groq API)
- **Language**: Python 3.12
- **Data Handling**: Native JSON and `datetime` modules

---

## 📦 Installation (Local Development)

1. **Clone the repository**
   ```bash
   git clone https://github.com/Deslandes1/healthcoach-ai-fhir-training.git
   cd healthcoach-ai-fhir-training
