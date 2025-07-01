import pandas as pd
from app.synonyms import SYNONYM_MAP

def load_skills(path="skills_dataset.xlsx"):
    df = pd.read_excel(path)
    skills = set(df['Skills'].dropna().str.lower().str.strip().unique().tolist())
    # Expand with all synonyms and canonical forms
    skills.update(SYNONYM_MAP.keys())
    skills.update(SYNONYM_MAP.values())
    return list(skills)