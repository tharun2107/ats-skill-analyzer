# skill_groups.py
import pandas as pd
from collections import defaultdict

GROUPED_SKILLS_PATH = "grouped_skills_dataset.csv"

def load_grouped_skills():
    df = pd.read_csv(GROUPED_SKILLS_PATH)
    grouped = defaultdict(list)
    for _, row in df.iterrows():
        group = row['Group'].strip().lower()
        skill = row['Skill'].strip().lower()
        grouped[group].append(skill)
    return grouped

# Example weights (can be extended)
GROUP_WEIGHTS = {
    "frontend": 1.2,
    "backend": 1.3,
    "cloud": 1.4,
    "devops": 1.5,
    "soft skills": 0.8,
    "ai_ml": 1.6,
    "database": 1.1,
    "other": 1.0
}

SECTION_WEIGHTS = {
    "experience": 1.5,
    "projects": 1.4,
    "education": 1.0,
    "certifications": 1.3,
    "achievements": 1.2,
    "default": 1.0
}

# Skill to group mapping for fallbacks
SKILL_GROUP_MAP = {
    'html': 'frontend',
    'css': 'frontend',
    'css3': 'frontend',
    'javascript': 'frontend',
    'react.js': 'frontend',
    'tailwind css': 'frontend',
    'figma': 'frontend',

    'node.js': 'backend',
    'express.js': 'backend',
    'django': 'backend',

    'mongodb': 'database',
    'postgresql': 'database',
    'elasticsearch': 'database',

    'aws': 'cloud',
    'aws ec2': 'cloud',
    'aws ecr': 'cloud',

    'docker': 'devops',
    'jenkins': 'devops',
    'terraform': 'devops',
    'kubernetes': 'devops',
    'github actions': 'devops',
    'ci/cd': 'devops',

    'gpt': 'ai_ml',
    'huggingface': 'ai_ml',
    'huggingface transformers': 'ai_ml',
    'natural language processing': 'ai_ml',
    'nlp': 'ai_ml',
    'rag': 'ai_ml',

    'communication': 'soft skills',
    'leadership': 'soft skills',
    'teamwork': 'soft skills',
    'problem solving': 'soft skills',
    'analytical thinking': 'soft skills'
}