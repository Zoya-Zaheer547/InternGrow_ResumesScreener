import PyPDF2
import docx
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Ensure NLTK data is ready
try:
    stop_words = set(stopwords.words('english'))
except:
    nltk.download('stopwords')
    nltk.download('punkt')
    nltk.download('punkt_tab')
    stop_words = set(stopwords.words('english'))

# Predefined skill database
SKILL_DATABASE = [
    "python", "java", "c++", "c#", "javascript", "typescript", "react", "angular", "node.js",
    "html", "css", "sql", "postgresql", "mongodb", "aws", "docker", "kubernetes", "git",
    "machine learning", "deep learning", "nlp", "computer vision", "tensorflow", "pytorch",
    "scikit-learn", "pandas", "numpy", "data analysis", "excel", "power bi", "tableau",
    "communication", "leadership", "problem solving", "agile", "scrum"
]

def extract_text_from_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"
    return text

def extract_text_from_docx(docx_file):
    doc = docx.Document(docx_file)
    return "\n".join([p.text for p in doc.paragraphs])

def extract_skills(text):
    text_clean = re.sub(r'[^a-zA-Z0-9\s#+.]', ' ', text.lower())
    found_skills = set()
    
    # Skill matching
    for skill in SKILL_DATABASE:
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text_clean):
            found_skills.add(skill.title())
            
    return list(found_skills)

def calculate_similarity(resume_text, job_description):
    documents = [resume_text, job_description]
    count_vectorizer = TfidfVectorizer(stop_words='english')
    sparse_matrix = count_vectorizer.fit_transform(documents)
    match_percentage = cosine_similarity(sparse_matrix)[0][1] * 100
    return round(match_percentage, 2)