# התקנת הספריות הדרושות (רק בפעם הראשונה)
# !pip install streamlit google-generativeai pypdf

import streamlit as st
import google.generativeai as genai
import PyPDF2
import io

# הגדרת כותרת ועיצוב
st.set_page_config(page_title="AI Tutor", layout="wide", page_icon="🎓")

st.title("🎓 AI Study Partner")
st.write("העלה סיכום או מאמר, וה-AI יהפוך אותו למבחן וכרטיסיות!")

# תפריט צד להגדרות
with st.sidebar:
    api_key = st.text_input("הכנס Google API Key", type="password")
    st.info("קבל מפתח בחינם מ-Google AI Studio")

# פונקציה לקריאת PDF
def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# הפונקציה הראשית
def main():
    uploaded_file = st.file_uploader("בחר קובץ PDF", type="pdf")

    if uploaded_file and api_key:
        # קריאת הקובץ
        with st.spinner("קורא את הקובץ..."):
            text = extract_text_from_pdf(uploaded_file)
            st.success("הקובץ נקרא בהצלחה!")

        # הגדרת ה-AI
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')

        # יצירת כרטיסיות
        if st.button("צור כרטיסיות לימוד 🗂️"):
            with st.spinner("ה-AI חושב..."):
                prompt = f"""
                תפקידך הוא מורה פרטי. קרא את הטקסט הבא וצור ממנו 5 כרטיסיות לימוד.
                לכל כרטיסיה תן: 'שאלה' ו-'תשובה'.
                הטקסט: {text[:4000]}
                """
                response = model.generate_content(prompt)
                st.markdown("### כרטיסיות לימוד:")
                st.write(response.text)

        # יצירת מבחן
        if st.button("צור מבחן אמריקאי 📝"):
            with st.spinner("מכין שאלות..."):
                prompt = f"""
                צור מבחן אמריקאי קצר (3 שאלות) על בסיס הטקסט.
                לכל שאלה הצג 4 אפשרויות ואת התשובה הנכונה בסוף.
                הטקסט: {text[:4000]}
                """
                response = model.generate_content(prompt)
                st.markdown("### מבחן ידע:")
                st.write(response.text)

    elif not api_key:
        st.warning("אנא הכנס את המפתח (API Key) בצד ימין כדי להתחיל.")

# הרצת האפליקציה
if __name__ == "__main__":
    main()
