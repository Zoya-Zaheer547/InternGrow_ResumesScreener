import streamlit as st
import pandas as pd
from utils import extract_text_from_pdf, extract_text_from_docx, extract_skills, calculate_similarity

# Page Config
st.set_page_config(
    page_title="AI Resume Screener Pro", 
    page_icon="⚡", 
    layout="wide"
)

# Custom Aesthetic CSS
st.markdown("""
<style>
    /* Main Background Gradient */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #0f172a 100%);
        color: #f8fafc;
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: rgba(15, 23, 42, 0.8) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Glassmorphism Title Box */
    .main-title {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 25px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        text-align: center;
    }
    
    .main-title h1 {
        background: linear-gradient(90deg, #60a5fa, #a78bfa, #f472b6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 2.8rem;
        margin-bottom: 8px;
    }
    
    .main-title p {
        color: #94a3b8;
        font-size: 1.1rem;
    }

    /* Primary Buttons Styling */
    .stButton>button {
        background: linear-gradient(90deg, #6366f1 0%, #8b5cf6 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 12px 28px !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        box-shadow: 0 4px 14px 0 rgba(99, 102, 241, 0.39) !important;
        transition: all 0.3s ease !important;
        width: 100%;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px 0 rgba(99, 102, 241, 0.6) !important;
    }

    /* Tables Styling */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
</style>
""", unsafe_allow_html=True)

# Main Title Section
st.markdown("""
<div class="main-title">
    <h1>⚡ Intelligent AI Resume Screener</h1>
    <p>Upload candidate resumes and match them intelligently against Job Descriptions using Natural Language Processing.</p>
</div>
""", unsafe_allow_html=True)

# Sidebar Input
st.sidebar.markdown("### 📋 Job Description")
job_desc = st.sidebar.text_area("Paste Job Description here:", height=320, placeholder="Target role requirements, technical skills, and responsibilities...")

# Upload Section
st.markdown("### 📂 Upload Candidate Resumes")
uploaded_files = st.file_uploader(
    "Support formats: PDF, DOCX", 
    type=["pdf", "docx"], 
    accept_multiple_files=True
)

st.write("")

if st.button("🚀 Run AI Screening & Rank Candidates"):
    if not job_desc.strip():
        st.warning("⚠️ Please paste a Job Description in the sidebar first!")
    elif not uploaded_files:
        st.warning("⚠️ Please upload at least one candidate resume!")
    else:
        results = []
        job_skills = extract_skills(job_desc)

        for file in uploaded_files:
            file_type = file.name.split('.')[-1].lower()
            if file_type == "pdf":
                resume_text = extract_text_from_pdf(file)
            else:
                resume_text = extract_text_from_docx(file)
            
            candidate_skills = extract_skills(resume_text)
            match_score = calculate_similarity(resume_text, job_desc)
            
            matched_skills = list(set(candidate_skills).intersection(set(job_skills)))
            missing_skills = list(set(job_skills) - set(candidate_skills))

            results.append({
                "Candidate Name": file.name.rsplit('.', 1)[0].replace('_', ' ').replace('-', ' ').title(),
                "Match Score (%)": match_score,
                "Extracted Skills": ", ".join(candidate_skills) if candidate_skills else "None Detected",
                "Matched Skills": ", ".join(matched_skills) if matched_skills else "None",
                "Missing Skills": ", ".join(missing_skills) if missing_skills else "None"
            })

        df = pd.DataFrame(results)
        df = df.sort_values(by="Match Score (%)", ascending=False).reset_index(drop=True)
        df.index += 1

        st.markdown("---")
        st.markdown("### 📊 Candidate Ranking Dashboard")
        st.dataframe(df, use_container_width=True)

        csv = df.to_csv(index_label="Rank").encode('utf-8')
        st.download_button(
            label="📥 Export Analysis as CSV",
            data=csv,
            file_name='resume_screening_results.csv',
            mime='text/csv'
        )