import spacy
from spacy.matcher import PhraseMatcher

# Load NLP model
nlp = spacy.load("en_core_web_sm")

# Skill database
SKILL_DB = [

    # IT / Data
    "python", "sql", "data analysis", "excel", "power bi",
    "machine learning", "tableau", "data visualization", "statistics",
    "django", "flask", "mongodb", "rest api", "git",
    "data structures", "problem solving", "docker", "cloud computing",

    # Web
    "html", "css", "react", "bootstrap", "javascript",

    # B.Com / Finance
    "accounting", "tally", "gst", "taxation",
    "financial reporting", "auditing", "bookkeeping",
    "financial analysis", "budgeting", "banking",

    # Marketing
    "digital marketing", "seo", "social media marketing",
    "content creation", "market research",
    "google ads", "analytics", "branding", "creativity",

    # HR
    "recruitment", "employee management", "hr policies",
    "payroll", "interviewing", "conflict resolution",
    "training", "organizational skills",

    # Common
    "communication", "teamwork"
]

# Create PhraseMatcher (done once for performance)
matcher = PhraseMatcher(nlp.vocab)
patterns = [nlp(skill) for skill in SKILL_DB]
matcher.add("SKILLS", patterns)


# -------- SKILL EXTRACTION (NLP BASED) --------
def extract_skills(text):
    doc = nlp(text.lower())

    matches = matcher(doc)

    extracted_skills = set()

    for match_id, start, end in matches:
        span = doc[start:end]
        extracted_skills.add(span.text)

    return list(extracted_skills)


# -------- MATCH CALCULATION --------
def calculate_match(resume_skills, job_skills):
    resume_skills = [s.lower().strip() for s in resume_skills]
    job_skills = [s.lower().strip() for s in job_skills]

    matched = list(set(resume_skills) & set(job_skills))
    missing = list(set(job_skills) - set(resume_skills))

    score = (len(matched) / len(job_skills)) * 100 if job_skills else 0

    return round(score, 2), matched, missing