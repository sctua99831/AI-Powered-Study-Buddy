# app.py
import streamlit as st
import google.generativeai as genai
import os
import io
from datetime import datetime

# -------------------------
# Page Configuration
# -------------------------
st.set_page_config(page_title="AI-Powered Study Buddy", page_icon="📘", layout="centered")
st.title("📘 AI-Powered Study Buddy")
st.write("""
Welcome to your personal AI-powered learning companion!  
Explain any topic, summarize study notes, or generate quizzes and flashcards instantly using Google Gemini AI.
""")

# -------------------------
# Load Gemini API Key
# -------------------------
GEMINI_API_KEY = (
    st.secrets.get("GEMINI_API_KEY", None)
    if "GEMINI_API_KEY" in st.secrets
    else os.environ.get("GEMINI_API_KEY")
)

if not GEMINI_API_KEY:
    st.warning("⚠️ Gemini API key not found. Please add it in Streamlit Secrets as GEMINI_API_KEY.")
    st.stop()

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# -------------------------
# Sidebar Navigation
# -------------------------
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Choose a function:",
    ["🧠 Concept Explanation", "📝 Summarize Notes", "🎯 Quiz & Flashcards"]
)

# -------------------------
# 1️⃣ Concept Explanation
# -------------------------
if page == "🧠 Concept Explanation":
    st.header("🧠 Explain Any Concept")
    topic = st.text_input("Enter a topic or concept you want to understand:", placeholder="e.g., Quantum Computing, Photosynthesis, Blockchain")

    if st.button("Explain Simply"):
        if not topic.strip():
            st.warning("Please enter a topic first.")
        else:
            with st.spinner("Generating a simple explanation using Gemini..."):
                try:
                    prompt = (
                        f"Explain the topic '{topic}' in very simple, student-friendly terms. "
                        "Use analogies or examples if useful, and keep it clear and easy to understand."
                    )
                    response = model.generate_content(prompt)
                    st.success("✅ Explanation Ready!")
                    st.subheader("Explanation:")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"Failed to generate explanation: {e}")

# -------------------------
# 2️⃣ Summarize Notes
# -------------------------
elif page == "📝 Summarize Notes":
    st.header("📝 Summarize Study Notes")
    notes = st.text_area("Paste your study notes or text:", placeholder="Paste your long notes or paragraphs here...", height=200)

    if st.button("Summarize Notes"):
        if not notes.strip():
            st.warning("Please paste some notes to summarize.")
        else:
            with st.spinner("Summarizing your notes..."):
                try:
                    prompt = (
                        "Summarize the following notes into concise, bullet-point study material. "
                        "Highlight key definitions, concepts, and examples:\n\n"
                        f"{notes}"
                    )
                    response = model.generate_content(prompt)
                    summary = response.text
                    st.success("✅ Summary Generated!")
                    st.subheader("Summary:")
                    st.write(summary)

                    # Download option
                    b = io.BytesIO(summary.encode("utf-8"))
                    st.download_button("💾 Download Summary", b, file_name=f"summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")

                except Exception as e:
                    st.error(f"Summarization failed: {e}")

# -------------------------
# 3️⃣ Quiz & Flashcards
# -------------------------
elif page == "🎯 Quiz & Flashcards":
    st.header("🎯 Quiz & Flashcards Generator")
    study_material = st.text_area("Paste study notes or text:", placeholder="Paste your summarized notes or study content here...", height=200)

    if st.button("Generate Quiz & Flashcards"):
        if not study_material.strip():
            st.warning("Please paste some study material first.")
        else:
            with st.spinner("Generating quiz and flashcards using Gemini..."):
                try:
                    prompt = (
                        "From the following study material, create:\n"
                        "1) 5 multiple-choice questions with 4 options each, marking the correct answer.\n"
                        "2) 5 flashcards (Q: ... A: ... format).\n\n"
                        f"Study Material:\n{study_material}"
                    )
                    response = model.generate_content(prompt)
                    quiz = response.text
                    st.success("✅ Quiz & Flashcards Ready!")
                    st.subheader("Quiz & Flashcards:")
                    st.write(quiz)

                    # Download option
                    b2 = io.BytesIO(quiz.encode("utf-8"))
                    st.download_button("💾 Download Quiz & Flashcards", b2, file_name=f"quiz_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")

                except Exception as e:
                    st.error(f"Quiz generation failed: {e}")

# -------------------------
# Footer
# -------------------------
st.markdown("---")
