# app/synonyms.py
import re
SYNONYM_MAP = {
    # Programming Languages
    "js": "javascript",
    "ts": "typescript",
    "py": "python",
    "c++": "cpp",
    "c#": "csharp",
    "r lang": "r",
    
    # Frontend
    "react": "react.js",
    "vue": "vue.js",
    "angular": "angular.js",
    "html": "html5",
    "css": "css3",
    "sass": "scss",
    "bootstrap 5": "bootstrap",
    "mui": "material ui",
    "tailwind": "tailwind css",
    "jquery": "jquery.js",

    # Backend
    "node": "node.js",
    "express": "express.js",
    "flask framework": "flask",
    "django framework": "django",
    "springboot": "spring boot",
    "nest": "nestjs",

    # Databases
    "pg": "postgresql",
    "postgre": "postgresql",
    "mysql db": "mysql",
    "mongo": "mongodb",
    "redis cache": "redis",
    "elastic": "elasticsearch",

    # DevOps
    "ci/cd": "continuous integration",
    "jenkins pipeline": "jenkins",
    "gh actions": "github actions",
    "github": "git",
    "gitlab": "git",
    "svn": "subversion",
    "aws ec2": "aws",
    "s3": "aws s3",
    "ecr": "aws ecr",
    "azure devops": "azure",
    "gcp": "google cloud platform",
    "k8s": "kubernetes",
    "docker container": "docker",

    # Data Science
    "ml": "machine learning",
    "dl": "deep learning",
    "pytorch": "torch",
    "tensorflow 2": "tensorflow",
    "nlp": "natural language processing",
     "natural language processing": "natural language processing",
    "naturalLanguageProcessing": "natural language processing",
    "sklearn": "scikit-learn",
    "openai api": "gpt",
    "llm": "large language model",
    "rag": "retrieval augmented generation",
    "huggingface": "transformers",

    # BI + Tools
    "powerbi": "power bi",
    "tableau desktop": "tableau",
    "looker studio": "looker",
    "ms excel": "excel",
    "notion.so": "notion",
    "jira software": "jira",
    "asana tool": "asana",
    "airflow": "apache airflow",
    "gdocs": "google docs",

    # Soft Skills
    "problem solving": "analytical thinking",
    "team player": "teamwork",
    "punctual": "time management",
    "quick learner": "adaptability",
    "collaboration": "teamwork",
    "presentation skills": "public speaking",
    "emotional intelligence": "eq",
    "ownership": "accountability",

    # Certifications
    "aws certified developer": "aws certification",
    "google certified cloud engineer": "gcp certification",
    "microsoft azure certified": "azure certification",
    "scrum master": "agile scrum master",
    "pmp": "project management professional",
    "ocjp": "java certification",

    # Academic / Other
    "btech": "bachelor of technology",
    "be": "bachelor of engineering",
    "mtech": "master of technology",
    "bsc": "bachelor of science",
    "msc": "master of science"
}

def normalize_skill(text: str) -> str:
    # Break camelCase or glue words
    text = re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', text)
    text = text.replace("-", " ").replace("_", " ")
    text = text.lower().strip()

    # Try synonym mapping
    if text in SYNONYM_MAP:
        return SYNONYM_MAP[text]

    # Try partial match in map (e.g., "worked on NLP system" → "natural language processing")
    for key in SYNONYM_MAP:
        if key in text:
            return SYNONYM_MAP[key]
    
    return text