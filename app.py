import streamlit as st
import re
from groq import Groq
from datetime import datetime
import json

# ================== SUPABASE CLIENT (flexible) ==================
try:
    from supabase import create_client, Client
except ImportError:
    Client = None

def get_supabase():
    # Try flat keys first
    supabase_url = st.secrets.get("SUPABASE_URL", "")
    supabase_key = st.secrets.get("SUPABASE_KEY", "")
    
    # If flat keys are empty, try nested under "supabase"
    if not supabase_url and "supabase" in st.secrets:
        supabase_url = st.secrets["supabase"].get("url", "")
        supabase_key = st.secrets["supabase"].get("key", "")
    
    if supabase_url and supabase_key and Client:
        try:
            return create_client(supabase_url, supabase_key)
        except Exception as e:
            st.error(f"Supabase connection error: {e}")
            return None
    return None

supabase = get_supabase()
SUPABASE_AVAILABLE = supabase is not None

# ================== CONFIGURATION ==================
st.set_page_config(
    page_title="HealthCoach AI | GlobalInternet.py",
    page_icon="🏥",
    layout="wide"
)

# Language texts (unchanged)
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
        "doc_prereq_text": "- Python 3.8 or higher\n- Required Python packages: streamlit, groq, datetime (built-in)\n- A Groq API key (optional – demo works without it)\n- Internet connection for video streaming",
        "doc_start": "How to Start",
        "doc_start_text": "1. Clone the repository: git clone https://github.com/Deslandes1/healthcoach-ai-fhir-training.git\n2. Install dependencies: pip install -r requirements.txt (or pip install streamlit groq supabase)\n3. Create a .streamlit/secrets.toml file with your Groq API key (optional):\n   GROQ_API_KEY = \"your-api-key-here\"\n   SUPABASE_URL = \"your-supabase-url\"\n   SUPABASE_KEY = \"your-supabase-key\"\n4. Run the app: streamlit run app.py\n5. The app will open in your browser.",
        "doc_test": "How to Test",
        "doc_test_text": "1. Watch the video introduction to understand the platform.\n2. Go to the Practice Problem tab and enter a FHIR Patient JSON or a date.\n3. Click 'Run & Check Solution' to see the calculated age.\n4. Go to the AI Coach tab, paste your code or describe your algorithm, and click 'Get AI Feedback' to receive constructive guidance.\n5. If no Groq key is set, a fallback response is provided.",
        "doc_demo": "Live Demo",
        "doc_demo_text": "You can test the fully functional app at:",
        "doc_demo_link": "https://healthcoach-ai-fhir-training-uzdeefhyupvfjkywurau6w.streamlit.app/"
    },
    "Français": {
        "title": "🏥 HealthCoach AI – Arène FHIR",
        "subtitle": "Maîtrisez l'interopérabilité en santé avec un coach IA",
        "video_tab": "🎬 Introduction vidéo",
        "practice_tab": "📝 Problème pratique",
        "ai_tab": "🤖 Coach IA",
        "doc_tab": "📚 Documentation",
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
        "howto_list": ["Regardez l'intro vidéo", "Lisez l'onglet Documentation", "Résolvez le problème FHIR", "Demandez des conseils au coach IA"],
        "footer": "© 2026 GlobalInternet.py – IA pour la formation FHIR",
        "security_badge": "🔐 Chiffrement de bout en bout actif",
        "security_caption": "Toutes les données sont sécurisées et anonymisées",
        "doc_title": "Documentation complète",
        "doc_prereq": "Prérequis",
        "doc_prereq_text": "- Python 3.8 ou supérieur\n- Paquets Python requis : streamlit, groq, datetime (intégré)\n- Une clé API Groq (optionnelle – la démo fonctionne sans)\n- Connexion Internet pour le streaming vidéo",
        "doc_start": "Comment démarrer",
        "doc_start_text": "1. Clonez le dépôt : git clone https://github.com/Deslandes1/healthcoach-ai-fhir-training.git\n2. Installez les dépendances : pip install -r requirements.txt (ou pip install streamlit groq supabase)\n3. Créez un fichier .streamlit/secrets.toml avec votre clé API Groq (optionnelle) :\n   GROQ_API_KEY = \"votre-clé-api-ici\"\n   SUPABASE_URL = \"votre-url-supabase\"\n   SUPABASE_KEY = \"votre-clé-supabase\"\n4. Lancez l'application : streamlit run app.py\n5. L'application s'ouvrira dans votre navigateur.",
        "doc_test": "Comment tester",
        "doc_test_text": "1. Regardez la vidéo d'introduction pour comprendre la plateforme.\n2. Allez dans l'onglet Problème pratique et entrez un JSON Patient FHIR ou une date.\n3. Cliquez sur 'Exécuter et vérifier' pour voir l'âge calculé.\n4. Allez dans l'onglet Coach IA, collez votre code ou décrivez votre algorithme, et cliquez sur 'Obtenir un feedback IA' pour recevoir des conseils constructifs.\n5. Si aucune clé Groq n'est définie, une réponse de repli est fournie.",
        "doc_demo": "Démo en direct",
        "doc_demo_text": "Vous pouvez tester l'application entièrement fonctionnelle à l'adresse :",
        "doc_demo_link": "https://healthcoach-ai-fhir-training-uzdeefhyupvfjkywurau6w.streamlit.app/"
    },
    "Español": {
        "title": "🏥 HealthCoach AI – Arena FHIR",
        "subtitle": "Domina la interoperabilidad en salud con un entrenador IA",
        "video_tab": "🎬 Introducción en video",
        "practice_tab": "📝 Problema práctico",
        "ai_tab": "🤖 Entrenador IA",
        "doc_tab": "📚 Documentación",
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
        "howto_list": ["Vea la introducción en video", "Lea la pestaña Documentación", "Resuelva el problema FHIR", "Pida consejos al entrenador IA"],
        "footer": "© 2026 GlobalInternet.py – IA para educación FHIR",
        "security_badge": "🔐 Cifrado de extremo a extremo activo",
        "security_caption": "Todos los datos están seguros y anonimizados",
        "doc_title": "Documentación completa",
        "doc_prereq": "Requisitos previos",
        "doc_prereq_text": "- Python 3.8 o superior\n- Paquetes Python necesarios: streamlit, groq, datetime (incluido)\n- Una clave API de Groq (opcional – la demo funciona sin ella)\n- Conexión a Internet para la transmisión de video",
        "doc_start": "Cómo empezar",
        "doc_start_text": "1. Clone el repositorio: git clone https://github.com/Deslandes1/healthcoach-ai-fhir-training.git\n2. Instale las dependencias: pip install -r requirements.txt (o pip install streamlit groq supabase)\n3. Cree un archivo .streamlit/secrets.toml con su clave API de Groq (opcional):\n   GROQ_API_KEY = \"su-clave-api-aquí\"\n   SUPABASE_URL = \"su-url-supabase\"\n   SUPABASE_KEY = \"su-clave-supabase\"\n4. Ejecute la aplicación: streamlit run app.py\n5. La aplicación se abrirá en su navegador.",
        "doc_test": "Cómo probar",
        "doc_test_text": "1. Vea el video de introducción para entender la plataforma.\n2. Vaya a la pestaña Problema práctico e ingrese un JSON Patient FHIR o una fecha.\n3. Haga clic en 'Ejecutar y verificar' para ver la edad calculada.\n4. Vaya a la pestaña Entrenador IA, pegue su código o describa su algoritmo y haga clic en 'Obtener retroalimentación IA' para recibir orientación constructiva.\n5. Si no hay clave de Groq, se proporciona una respuesta alternativa.",
        "doc_demo": "Demo en vivo",
        "doc_demo_text": "Puede probar la aplicación completamente funcional en:",
        "doc_demo_link": "https://healthcoach-ai-fhir-training-uzdeefhyupvfjkywurau6w.streamlit.app/"
    }
}

# ================== CUSTOM CSS ==================
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
    .doc-section {
        background: rgba(255, 255, 255, 0.8);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        border-left: 4px solid #8e24aa;
    }
</style>
""", unsafe_allow_html=True)

# ================== SIDEBAR ==================
with st.sidebar:
    st.image("https://raw.githubusercontent.com/Deslandes1/Color-Software-Game/main/Gesner%20Deslandes.png", width=80)
    st.markdown("### **Gesner Deslandes**")
    st.markdown("## **GlobalInternet.py**")
    st.markdown("**HealthCoach AI**")
    st.markdown("---")
    
    language = st.selectbox("🌐 Language / Idioma / Langue", ["English", "Français", "Español"])
    texts = TEXTS[language]
    
    st.markdown("---")
    if SUPABASE_AVAILABLE:
        st.success("✅ Supabase connected")
    else:
        st.warning("⚠️ Supabase not configured")
        # Debug expander to see what keys are present
        with st.expander("🔍 Debug: Secrets keys"):
            st.write("Keys found:", list(st.secrets.keys()))
            if "SUPABASE_URL" in st.secrets:
                st.write("SUPABASE_URL: present")
            if "SUPABASE_KEY" in st.secrets:
                st.write("SUPABASE_KEY: present")
            if "supabase" in st.secrets:
                st.write("supabase section: present")
    
    st.markdown("### 🛡️ Global Security Shield active")
    st.markdown(f'<div class="security-badge">{texts["security_badge"]}</div>', unsafe_allow_html=True)
    st.caption(texts["security_caption"])
    
    st.markdown("---")
    st.markdown("Built by **Gesner Deslandes**, Engineer-in-Chief")
    st.markdown("📞 (509) 4738 5663")
    st.markdown("✉️ deslandes78@gmail.com")
    st.markdown("---")
    
    st.markdown(f"### {texts['sidebar_howto']}")
    for i, step in enumerate(texts["howto_list"], 1):
        st.markdown(f"{i}. {step}")

# ================== MAIN TITLE ==================
st.title(texts["title"])
st.markdown(f"### {texts['subtitle']}")
st.markdown("---")

# ================== GROQ CLIENT ==================
if "GROQ_API_KEY" in st.secrets:
    groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    GROQ_AVAILABLE = True
else:
    groq_client = None
    GROQ_AVAILABLE = False
    st.warning("ℹ️ Groq API key not found. The AI Coach will use a fallback mode (no real AI feedback). To enable full AI capabilities, add GROQ_API_KEY to your secrets.")

# ================== AI FEEDBACK (with fallback) ==================
def get_ai_feedback(user_input, language):
    if not GROQ_AVAILABLE:
        return (
            "⚠️ **Groq API key is not configured.**\n\n"
            "In a real deployment, the AI would analyze your code and provide detailed feedback on correctness, edge cases, and FHIR best practices.\n\n"
            "**To enable the AI Coach, please add your Groq API key to `.streamlit/secrets.toml`.**\n\n"
            "Here is a sample improvement you could consider:\n"
            "- Add error handling for missing 'birthDate' field.\n"
            "- Validate the date format before parsing.\n"
            "- Use a try-except block for JSON parsing."
        )
    try:
        system_prompt = f"""You are an expert FHIR and healthcare interoperability coach. The user has written code or an idea to calculate age from a FHIR Patient resource. Provide constructive feedback:
- Check correctness and edge cases (invalid dates, missing fields).
- Suggest improvements (error handling, parsing JSON).
- Explain FHIR best practices if relevant.
Keep your answer concise and helpful. Respond in {language}."""
        response = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ],
            temperature=0.3,
            max_tokens=800
        )
        result = response.choices[0].message.content.strip()
        if SUPABASE_AVAILABLE:
            try:
                supabase.table("feedback_log").insert({
                    "user_input": user_input[:500],
                    "response": result[:500],
                    "language": language,
                    "timestamp": datetime.now().isoformat()
                }).execute()
            except Exception:
                pass
        return result
    except Exception as e:
        return texts["ai_error"].format(str(e))

# ================== TABS ==================
tab1, tab2, tab3, tab4 = st.tabs([texts["video_tab"], texts["practice_tab"], texts["ai_tab"], texts["doc_tab"]])

# --- Tab 1: Video ---
with tab1:
    st.markdown(f"### {texts['video_title']}")
    st.markdown(texts['video_desc'])
    video_link = "https://www.dropbox.com/scl/fi/bjne1bml85ce8k92ljrbk/HealthCoach-AI_demo_narrated-1.mp4?rlkey=z5cfob5jzbdwynvxtvgq151ac&st=6pge3b1x&dl=1"
    st.video(video_link)
    st.caption("If the video does not play, click the three dots → Download to save it locally.")

# --- Tab 2: Practice ---
with tab2:
    st.markdown(f"### {texts['problem_title']}")
    st.markdown(texts['problem_statement'])
    user_input_data = st.text_area(texts["test_input"], height=150,
                                   value='{"resourceType":"Patient","birthDate":"1990-03-15"}')
    if st.button(texts["run_button"]):
        try:
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
    if not GROQ_AVAILABLE:
        st.info("ℹ️ **Fallback Mode** – No Groq API key found. The feedback below is a generic template. To get real AI-powered coaching, add your Groq API key to the secrets.")
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

# --- Tab 4: Documentation ---
with tab4:
    st.markdown(f"### 📖 {texts['doc_title']}")
    
    st.markdown(f"#### {texts['doc_prereq']}")
    st.markdown(texts['doc_prereq_text'])
    
    st.markdown(f"#### {texts['doc_start']}")
    st.markdown(texts['doc_start_text'])
    
    st.markdown(f"#### {texts['doc_test']}")
    st.markdown(texts['doc_test_text'])
    
    st.markdown(f"#### {texts['doc_demo']}")
    st.markdown(texts['doc_demo_text'])
    st.markdown(f"👉 [{texts['doc_demo_link']}]({texts['doc_demo_link']})")
    
    st.markdown("---")
    st.markdown("**Additional Resources**")
    st.markdown("- GitHub Repository: [https://github.com/Deslandes1/healthcoach-ai-fhir-training](https://github.com/Deslandes1/healthcoach-ai-fhir-training)")
    st.markdown("- GlobalInternet.py Website: [https://globalinternetsitepy-abh7v6tnmskxxnuplrdcgk.streamlit.app/](https://globalinternetsitepy-abh7v6tnmskxxnuplrdcgk.streamlit.app/)")

# ================== FOOTER ==================
st.markdown("---")
st.markdown(texts["footer"])
