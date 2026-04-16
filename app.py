import streamlit as st
from streamlit_option_menu import option_menu
from resume_parser import extract_text_from_pdf
from skill_matcher import extract_skills, calculate_match
import pandas as pd
import matplotlib.pyplot as plt

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="AI Resume Screener", layout="wide")

# ---------------- UI STYLE ----------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #141e30, #243b55);
    color: white;
}
</style>
""", unsafe_allow_html=True)

# ---------------- LOGIN SYSTEM ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "1234":
            st.session_state.logged_in = True
            st.success("Login successful!")
            st.rerun()
        else:
            st.error("Invalid credentials")

    st.stop()

# ---------------- NAVIGATION MENU ----------------
selected = option_menu(
    menu_title=None,
    options=["Home", "Analyzer", "Dashboard", "About"],
    icons=["house", "search", "bar-chart", "info-circle"],
    orientation="horizontal"
)

# ---------------- HOME ----------------
if selected == "Home":
    st.title("🚀 AI Resume Screening Tool")

    st.markdown("""
    ### Welcome!

    This tool helps you:
    - 📄 Analyze resumes  
    - 🎯 Match job descriptions  
    - 📊 Get match score  
    - 📈 View analytics dashboard  
    """)

# ---------------- ANALYZER ----------------
elif selected == "Analyzer":

    st.title("📊 Resume Analyzer")

    uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
    job_description = st.text_area("Enter Job Description")

    if st.button("Analyze Resume"):
        if uploaded_file and job_description:

            with st.spinner("Analyzing..."):
                resume_text = extract_text_from_pdf(uploaded_file)

                if not resume_text.strip():
                    st.error("Could not extract text")
                else:
                    resume_skills = extract_skills(resume_text)
                    job_skills = extract_skills(job_description)

                    score, matched, missing = calculate_match(resume_skills, job_skills)

                    # Save data for dashboard
                    st.session_state.matched = matched
                    st.session_state.missing = missing

            # Display Results
            st.metric("Match Score", f"{score}%")
            st.progress(int(score))

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("✅ Matched Skills")
                st.markdown(" ".join([f"`{s}`" for s in matched]))

            with col2:
                st.subheader("❌ Missing Skills")
                st.markdown(" ".join([f"`{s}`" for s in missing]))

        else:
            st.warning("⚠️ Please upload resume and enter job description")

# ---------------- DASHBOARD ----------------
elif selected == "Dashboard":

    st.title("📊 Analytics Dashboard")

    if "matched" in st.session_state and "missing" in st.session_state:

        data = {
            "Category": ["Matched", "Missing"],
            "Count": [
                len(st.session_state.matched),
                len(st.session_state.missing)
            ]
        }

        df = pd.DataFrame(data)

        st.subheader("Skill Analysis")

        col1, col2, col3 = st.columns([1,2,1])

        with col2:
            fig, ax = plt.subplots(figsize=(2,2))
            ax.pie(
                df["Count"],
                labels=df["Category"],
                autopct='%1.0f%%',
                startangle=90,
                textprops={'fontsize': 7}
            )

            ax.axis('equal')
            st.pyplot(fig)


    else:
        st.warning("⚠️ Run analysis first to see dashboard")

# ---------------- ABOUT ----------------
elif selected == "About":

    st.title("📁 About Project")

    st.write("""
    This AI Resume Screening Tool:

    - Extracts text from PDF resumes  
    - Uses NLP (spaCy) for skill extraction  
    - Matches job descriptions  
    - Calculates match score  
    - Displays analytics dashboard  

    ### Tech Stack:
    - Python  
    - Streamlit  
    - spaCy   
    """)