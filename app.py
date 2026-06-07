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
        "howto_list": ["Watch the video intro", "Solve the FHIR practice problem", "Ask AI Coach for feedback", "Prepare for interoperability roles"],
        "footer": "© 2026 GlobalInternet.py – AI for FHIR Education",
        "security_badge": "🔐 End‑to‑end encryption active",
        "security_caption": "All data is secured and anonymized",
        "price_title": "Our Services",
        "price_list": [
            "Full source code – $499 USD",
            "Source + customization – $1,499 USD",
            "Enterprise plan – $2,999 USD"
        ]
    },
    "Français": {
        "title": "🏥 HealthCoach AI – Arène FHIR",
        "subtitle": "Maîtrisez l'interopérabilité en santé avec un coach IA",
        "video_tab": "🎬 Introduction vidéo",
        "practice_tab": "📝 Problème pratique",
        "ai_tab": "🤖 Coach IA",
        "video_title": "Regardez la vidéo d'introduction complète",
        "video_desc": "Cette vidéo explique comment utiliser la plateforme et comment le coach IA vous aide à apprendre FHIR.",
        "problem_title": "Problème FHIR : Calculer l'âge d'un patient",
        "problem_statement": """
On vous donne une ressource Patient FHIR au format JSON. Écrivez une fonction qui extrait la date de naissance et calcule l'âge en années à aujourd'hui.

**Exemple de ressource Patient FHIR (JSON) :**
{
  "resourceType": "Patient",
  "birthDate": "1990-03-15",
  "name": [{"given": ["Jean"], "family": "Dupont"}]
}

**Sortie attendue :** Âge en années (ex. 36).

Écrivez votre solution en Python. Utilisez le module `datetime`.
""",
        "test_input": "Entrez le JSON FHIR ou la date de naissance (AAAA-MM-JJ) :",
        "run_button": "Exécuter et vérifier",
        "result_correct": "✅ Correct ! L'âge est **{}** ans.",
        "result_wrong": "❌ Votre code a retourné {}, mais le bon âge est {}. Utilisez le Coach IA.",
        "hint_placeholder": "Collez votre code ou décrivez votre idée...",
        "hint_button": "Obtenir un feedback IA",
        "ai_thinking": "L'IA analyse votre approche...",
        "ai_error": "Erreur IA : {}",
        "sidebar_howto": "Comment utiliser",
        "howto_list": ["Regardez l'intro vidéo", "Résolvez le problème FHIR", "Demandez des conseils au coach IA", "Préparez-vous aux rôles d'interopérabilité"],
        "footer": "© 2026 GlobalInternet.py – IA pour la formation FHIR",
        "security_badge": "🔐 Chiffrement de bout en bout actif",
        "security_caption": "Toutes les données sont sécurisées et anonymisées",
        "price_title": "Nos services",
        "price_list": [
            "Code source complet – 499 USD",
            "Code + personnalisation – 1 499 USD",
            "Formule Entreprise – 2 999 USD"
        ]
    },
    "Español": {
        "title": "🏥 HealthCoach AI – Arena FHIR",
        "subtitle": "Domina la interoperabilidad en salud con un entrenador IA",
        "video_tab": "🎬 Introducción en video",
        "practice_tab": "📝 Problema práctico",
        "ai_tab": "🤖 Entrenador IA",
        "video_title": "Vea el video de introducción completo",
        "video_desc": "Este video explica cómo usar la plataforma y cómo el entrenador IA te ayuda a aprender FHIR.",
        "problem_title": "Problema FHIR: Calcular edad del paciente",
        "problem_statement": """
Se le proporciona un recurso Patient FHIR en formato JSON. Escriba una función que extraiga la fecha de nacimiento y calcule la edad en años hasta hoy.

**Ejemplo de recurso Patient FHIR (JSON):**
{
  "resourceType": "Patient",
  "birthDate": "1990-03-15",
  "name": [{"given": ["Juan"], "family": "Pérez"}]
}

**Salida esperada:** Edad en años (ej. 36).

Escriba su solución en Python. Use el módulo `datetime`.
""",
        "test_input": "Ingrese el JSON FHIR o la fecha de nacimiento (AAAA-MM-DD):",
        "run_button": "Ejecutar y verificar",
        "result_correct": "✅ ¡Correcto! La edad es **{}** años.",
        "result_wrong": "❌ Su código devolvió {}, pero la edad correcta es {}. Use el Entrenador IA.",
        "hint_placeholder": "Pegue su código o describa su idea algorítmica...",
        "hint_button": "Obtener retroalimentación IA",
        "ai_thinking": "La IA está analizando su enfoque...",
        "ai_error": "Error IA: {}",
        "sidebar_howto": "Cómo usar",
        "howto_list": ["Vea la introducción en video", "Resuelva el problema FHIR", "Pida consejos al entrenador IA", "¡Participe en roles de interoperabilidad!"],
        "footer": "© 2026 GlobalInternet.py – IA para educación FHIR",
        "security_badge": "🔐 Cifrado de extremo a extremo activo",
        "security_caption": "Todos los datos están seguros y anonimizados",
        "price_title": "Nuestros servicios",
        "price_list": [
            "Código fuente completo – $499 USD",
            "Código + personalización – $1,499 USD",
            "Plan Empresarial – $2,999 USD"
        ]
    }
}

# ================== CUSTOM CSS (light purple) ==================
st.markdown("""
<style>
    .stApp { background: linear-gradient(135deg, #f3e5f5 0%, #e1bee7 100%); }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #ce93d8 0%, #ab47bc 100%);
        border-right: 2px solid #6a1b9a;
    }
    [data-testid="stSidebar"] .stMarkdown, 
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] .stCaption { color: #1a1a2e !important; }
    [data-testid="stSidebar"] .stSelectbox label {
        color: #1a1a2e !important;
        font-weight: bold !important;
        font-size: 1rem !important;
    }
    [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] span {
        color: #1a1a2e !important;
        font-weight: bold !important;
    }
    div[data-baseweb="select"] ul { background-color: #e1bee7 !important; }
    div[data-baseweb="select"] ul li {
        color: #1a1a2e !important;
        font-weight: bold !important;
        background-color: #e1bee7 !important;
    }
    div[data-baseweb="select"] ul li:hover { background-color: #ba68c8 !important; }
    h1, h2, h3 { color: #4a148c !important; }
    p, li, .stMarkdown { color: #1a1a2e !important; }
    .stButton>button {
        background-color: #8e24aa !important;
        color: white !important;
        border-radius: 30px !important;
        font-weight: bold !important;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #ab47bc !important;
        transform: scale(1.02);
    }
    .security-badge {
        background: #f3e5f5;
        border: 1px solid #6a1b9a;
        border-radius: 30px;
        padding: 8px 15px;
        margin: 10px 0;
        text-align: center;
        color: #4a148c;
        font-weight: bold;
    }
    .feature-card {
        background: rgba(255, 255, 255, 0.7);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# ================== SIDEBAR ==================
with st.sidebar:
    st.image("https://raw.githubusercontent.com/Deslandes1/Color-Software-Game/main/Gesner%20Deslandes.png", width=80)
    st.markdown("## **GlobalInternet.py**")
    st.markdown("**HealthCoach AI**")
    st.markdown("---")
    
    language = st.selectbox("🌐 Language / Idioma / Langue", ["English", "Français", "Español"])
    texts = TEXTS[language]
    
    st.markdown("---")
    st.markdown("### 🛡️ Global Security Shield active")
    st.markdown(f'<div class="security-badge">{texts["security_badge"]}</div>', unsafe_allow_html=True)
    st.caption(texts["security_caption"])
    
    st.markdown("---")
    st.markdown("Built by **Gesner Deslandes**, Engineer-in-Chief")
    st.markdown("📞 (509) 4738 5663")
    st.markdown("✉️ deslandes78@gmail.com")
    st.markdown("---")
    
    st.markdown(f"### 💰 {texts['price_title']}")
    for item in texts["price_list"]:
        st.markdown(f"- {item}")
    st.markdown("---")
    
    st.markdown(f"### {texts['sidebar_howto']}")
    for i, step in enumerate(texts["howto_list"], 1):
        st.markdown(f"{i}. {step}")

# ================== MAIN TITLE ==================
st.title(texts["title"])
st.markdown(f"### {texts['subtitle']}")
st.markdown("---")

# ================== GROQ CLIENT ==================
if "GROQ_API_KEY" not in st.secrets:
    st.error("⚠️ Missing Groq API key. Add `GROQ_API_KEY` to your Streamlit secrets.")
    st.stop()
groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# ================== AI FEEDBACK ==================
def get_ai_feedback(user_input, language):
    system_prompt = f"""You are an expert FHIR and healthcare interoperability coach. The user has written code or an idea to calculate age from a FHIR Patient resource. Provide constructive feedback:
- Check correctness and edge cases (invalid dates, missing fields).
- Suggest improvements (error handling, parsing JSON).
- Explain FHIR best practices if relevant.
Keep your answer concise and helpful. Respond in {language}."""
    try:
        response = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ],
            temperature=0.3,
            max_tokens=800
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return texts["ai_error"].format(str(e))

# ================== TABS ==================
tab1, tab2, tab3 = st.tabs([texts["video_tab"], texts["practice_tab"], texts["ai_tab"]])

# --- Tab 1: Video Introduction (with your new narrated video) ---
with tab1:
    st.markdown(f"### {texts['video_title']}")
    st.markdown(texts['video_desc'])
    # Your narrated HealthCoach AI video link (dl=1 for direct streaming)
    video_link = "https://www.dropbox.com/scl/fi/bjne1bml85ce8k92ljrbk/HealthCoach-AI_demo_narrated-1.mp4?rlkey=z5cfob5jzbdwynvxtvgq151ac&st=6pge3b1x&dl=1"
    st.video(video_link)
    st.caption("If the video does not play, click the three dots → Download to save it locally.")

# --- Tab 2: Practice Problem ---
with tab2:
    st.markdown(f"### {texts['problem_title']}")
    st.markdown(texts['problem_statement'])
    user_input_data = st.text_area(texts["test_input"], height=150,
                                   value='{"resourceType":"Patient","birthDate":"1990-03-15"}')
    if st.button(texts["run_button"]):
        try:
            import json
            data = json.loads(user_input_data)
            birth_date_str = data.get("birthDate")
            if not birth_date_str:
                st.error("No birthDate field found in JSON.")
            else:
                birth_date = datetime.strptime(birth_date_str, "%Y-%m-%d")
                today = datetime.today()
                age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
                st.success(texts["result_correct"].format(age))
        except json.JSONDecodeError:
            # assume direct birth date string
            try:
                birth_date = datetime.strptime(user_input_data.strip(), "%Y-%m-%d")
                today = datetime.today()
                age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
                st.success(texts["result_correct"].format(age))
            except Exception as e:
                st.error(f"Invalid input. Provide JSON or YYYY-MM-DD. Error: {e}")
        except Exception as e:
            st.error(f"Error: {e}")

# --- Tab 3: AI Coach ---
with tab3:
    st.markdown(f"### 🤖 {texts['ai_tab']}")
    user_code = st.text_area(texts["hint_placeholder"], height=250,
                             placeholder='Example: def calculate_age(fhir_json):\n    import json, datetime\n    data = json.loads(fhir_json)\n    birth = datetime.datetime.strptime(data["birthDate"], "%Y-%m-%d")\n    ...')
    if st.button(texts["hint_button"]):
        if not user_code.strip():
            st.warning("Please describe your approach or paste your code.")
        else:
            with st.spinner(texts["ai_thinking"]):
                feedback = get_ai_feedback(user_code, language)
            st.markdown("### 💡 AI Feedback")
            st.markdown(feedback)

# ================== FOOTER ==================
st.markdown("---")
st.markdown(texts["footer"])
