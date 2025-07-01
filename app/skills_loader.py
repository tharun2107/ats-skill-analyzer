import pandas as pd

def load_skills(path="skills_dataset.xlsx"):
    df = pd.read_excel(path)
    skills = df['Skills'].dropna().str.lower().str.strip().unique().tolist()
    return skills