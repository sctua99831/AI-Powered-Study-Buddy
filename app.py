import streamlit as st
import google.generativeai as genai
import os
from datetime import datetime
import io

# ----------------------------
# Page Configuration
# ----------------------------
st.set_page_config(page_title="AI-Powered Study Buddy", page_icon="🎓", layout="centered")
st.title("🎓 AI-Powered Study Buddy")
st.write("""
Your personal AI study companion!  
You can:
- 💡 Explain complex topics in simple terms.  
- 📚 Summarize your study notes.  
- 🧠 Generate quizzes and flashcards from notes.
""")

# ----------------------------
# Gemini API Setup
# ----------------------------
if "GEMINI_API_KEY" in st.secrets:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
else:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    st.error("🚨 Gemini API key not found! Please add it in Streamlit secrets or as an environment variable.")
    st.stop()

genai.configure(api_key=GEMINI_API_KEY)

# ----------------------------
# Task Selection
# ----------------------------
task = st.sidebar.selectbox(
    "Choose a task:",
    ["Explain Topic", "Summarize Notes", "Generate Quiz & Flashcards"]
)

# ----------------------------
# 1️⃣ Explain Topic
# ----------------------------
if task == "Explain Topic":
    st.header("💡 Explain Topic in Simple Terms")
    topic = st.text_input("Enter a topic you want explained:")
    detail_level = st.radio("Choose explanation level:", ["Beginner", "Intermediate", "Advanced"])

    if st.button("Explain"):
        if not topic:
            st.warning("Please enter a topic.")
        else:
            with st.spinner("Generating explanation..."):
                try:
                    model = genai.GenerativeModel("gemini-2.0-flash")
                    prompt = f"""
You are a helpful study assistant. Explain the topic "{topic}" in simple terms for a {detail_level.lower()} learner.
Make the explanation clear, structured, and engaging.
Add examples or analogies when helpful.
"""
                    response = model.generate_content(prompt)
                    explanation = response.text.strip()

                    st.success("✅ Explanation Ready!")
                    st.subheader("Simplified Explanation")
                    st.write(explanation)

                except Exception as e:
                    st.error(f"Explanation failed: {e}")

# ----------------------------
# 2️⃣ Summarize Notes
# ----------------------------
elif task == "Summarize Notes":
    st.header("📚 Summarize Study Notes")
    notes = st.text_area("Paste your study notes below:", height=300)

    if st.button("Summarize"):
        if not notes.strip():
            st.warning("Please paste your notes first.")
        else:
            with st.spinner("Summarizing notes..."):
                try:
                    model = genai.GenerativeModel("gemini-2.0-flash")
                    prompt = f"""
You are an academic summarizer. Summarize the following notes into concise, well-organized bullet points.
Highlight key concepts, definitions, and examples where relevant.

Notes:
{notes}
"""
                    response = model.generate_content(prompt)
                    summary = response.text.strip()

                    st.success("✅ Summary Ready!")
                    st.subheader("Summary")
                    st.write(summary)

                    # Download option
                    st.download_button(
                        "⬇️ Download Summary (.txt)",
                        data=summary.encode("utf-8"),
                        file_name=f"summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                        mime="text/plain"
                    )

                except Exception as e:
                    st.error(f"Summarization failed: {e}")

# ----------------------------
# 3️⃣ Generate Quiz & Flashcards
# ----------------------------
elif task == "Generate Quiz & Flashcards":
    st.header("🧠 Generate Quiz & Flashcards")
    content = st.text_area("Paste study notes or text content below:", height=300)

    if st.button("Generate"):
        if not content.strip():
            st.warning("Please paste some text to create quiz and flashcards.")
        else:
            with st.spinner("Generating quiz & flashcards..."):
                try:
                    model = genai.GenerativeModel("gemini-2.0-flash")
                    prompt = f"""
You are a quiz and flashcard generator.

From the following text, create:
1. **5 Multiple Choice Questions (MCQs)** with 4 options each — clearly mark the correct answer.
2. **5 Flashcards** in the format:
   Q: ...
   A: ...

Keep questions conceptual and suitable for students.

Text:
{content}
"""
                    response = model.generate_content(prompt)
                    quiz_flashcards = response.text.strip()

                    st.success("✅ Quiz & Flashcards Ready!")
                    st.subheader("Quiz & Flashcards")
                    st.write(quiz_flashcards)

                    # Download option
                    st.download_button(
                        "⬇️ Download Quiz & Flashcards (.txt)",
                        data=quiz_flashcards.encode("utf-8"),
                        file_name=f"quiz_flashcards_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                        mime="text/plain"
                    )

                except Exception as e:
                    st.error(f"Quiz generation failed: {e}")

# ----------------------------
# Footer
# ----------------------------
st.markdown("---")


