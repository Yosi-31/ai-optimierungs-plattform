import streamlit as st
import pandas as pd
import requests

# -------------------------
# GRUNDKONFIGURATION
# -------------------------
st.set_page_config(
    page_title="AI Analyse & Optimierung",
    layout="wide"
)

st.title("🚀 AI Analyse & Optimierungs Plattform")

# -------------------------
# AI KONFIG
# -------------------------
HF_TOKEN = st.secrets.get("HF_TOKEN", "")
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"}

def ask_ai(prompt):
    response = requests.post(
        API_URL,
        headers=HEADERS,
        json={"inputs": prompt}
    )
    return response.json()[0]["generated_text"]

# -------------------------
# MODUS
# -------------------------
modus = st.radio(
    "Modus wählen",
    [
        "🟢 Anfänger – verständlich & geführt",
        "🔵 Pro – tief & analytisch"
    ]
)

# -------------------------
# UPLOAD
# -------------------------
uploaded_file = st.file_uploader(
    "Datei hochladen (CSV, Excel, TXT)",
    type=["csv", "xlsx", "txt"]
)

content = ""

if uploaded_file:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
        st.subheader("📊 Datenvorschau")
        st.dataframe(df)
        content = df.head(25).to_string()

    elif uploaded_file.name.endswith(".xlsx"):
        df = pd.read_excel(uploaded_file)
        st.subheader("📊 Datenvorschau")
        st.dataframe(df)
        content = df.head(25).to_string()

    else:
        content = uploaded_file.read().decode("utf-8")
        st.subheader("📄 Textvorschau")
        st.text_area("", content, height=300)

# -------------------------
# PROMPTS
# -------------------------
def build_prompt(modus, content):
    if "Anfänger" in modus:
        return f"""
Du bist ein professioneller Coach.

Aufgaben:
1. Kurze Zusammenfassung
2. Was ist gut?
3. Was kann verbessert werden?
4. Konkrete, einfache Optimierungsschritte

Erkläre klar, strukturiert und ohne unnötige Fachbegriffe.

Inhalt:
{content}
"""
    else:
        return f"""
Du bist ein erfahrener Analyst und Optimierungs-Experte.

Analysiere:
- Schwächen
- Risiken
- Ineffizienzen
- Optimierungspotenziale
- Konkrete Maßnahmen

Sei direkt, präzise und fachlich.

Inhalt:
{content}
"""

# -------------------------
# ANALYSE BUTTON
# -------------------------
if content and st.button("🤖 Analyse & Optimierung starten"):
    prompt = build_prompt(modus, content)
    with st.spinner("AI analysiert …"):
        result = ask_ai(prompt)

    st.subheader("🧠 AI Feedback")
    st.write(result)

# -------------------------
# FACHLICHER CHAT
# -------------------------
st.divider()
st.subheader("💬 Fachlicher Dialog")

frage = st.text_input("Stelle eine fachliche Frage zum Upload")

if frage and content:
    chat_prompt = f"""
Kontext:
{content}

Frage:
{frage}
"""
    antwort = ask_ai(chat_prompt)
    st.write(antwort)
