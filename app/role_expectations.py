# # app/role_expectations.py
# ROLE_EXPECTATIONS = {
#     "frontend developer": [
#         "html", "css", "javascript", "react", "vue", "tailwind css", "figma", "responsive design"
#     ],
#     "backend developer": [
#         "node.js", "express.js", "django", "postgresql", "mongodb", "api design"
#     ],
#     "data scientist": [
#         "python", "pandas", "numpy", "scikit-learn", "tensorflow", "matplotlib", "data visualization"
#     ],
#     "cloud engineer": [
#         "aws", "terraform", "jenkins", "docker", "kubernetes", "ec2", "ecr", "prometheus"
#     ],
#     "ai engineer": [
#         "machine learning", "deep learning", "transformers", "gpt", "huggingface", "nlp", "rag"
#     ],
#     "full stack developer": [
#         "html", "css", "javascript", "react", "node.js", "express.js", "mongodb", "docker"
#     ],
#     "software tester": [
#         "manual testing", "automation testing", "selenium", "jira", "test cases"
#     ]
# }

# def infer_expected_skills(role_title: str):
#     return ROLE_EXPECTATIONS.get(role_title.lower(), [])

# def group_skills(skills_list):
#     from app.synonyms import normalize_skill
#     groups = {
#         "Frontend": {"html", "css", "javascript", "react", "vue", "figma", "tailwind css"},
#         "Backend": {"node.js", "express.js", "django", "api", "java"},
#         "Database": {"postgresql", "mongodb", "mysql"},
#         "DevOps": {"jenkins", "docker", "kubernetes", "terraform"},
#         "Cloud": {"aws", "azure", "gcp", "ec2", "ecr"},
#         "AI_ML": {"machine learning", "nlp", "gpt", "rag", "huggingface", "transformers"},
#         "Soft Skills": {"communication", "leadership", "teamwork", "problem solving"},
#         "Other": set()
#     }

#     result = {k: [] for k in groups}
#     result["Other"] = []

#     for skill in skills_list:
#         norm = normalize_skill(skill)
#         found = False
#         for group, keywords in groups.items():
#             if norm in keywords:
#                 result[group].append(norm)
#                 found = True
#                 break
#         if not found:
#             result["Other"].append(norm)

#     return {k: v for k, v in result.items() if v}

# app/role_expectations.py

ROLE_EXPECTATIONS = {
    "frontend developer": [
        "html", "css", "javascript", "react", "vue", "tailwind css", "figma", "responsive design"
    ],
    "backend developer": [
        "node.js", "express.js", "django", "postgresql", "mongodb", "api design"
    ],
    "data scientist": [
        "python", "pandas", "numpy", "scikit-learn", "tensorflow", "matplotlib", "data visualization"
    ],
    "cloud engineer": [
        "aws", "terraform", "jenkins", "docker", "kubernetes", "ec2", "ecr", "prometheus"
    ],
    "ai engineer": [
        "machine learning", "deep learning", "transformers", "gpt", "huggingface", "nlp", "rag"
    ],
    "full stack developer": [
        "html", "css", "javascript", "react", "node.js", "express.js", "mongodb", "docker"
    ],
    "software tester": [
        "manual testing", "automation testing", "selenium", "jira", "test cases"
    ]
}

def infer_expected_skills(role_title: str):
    return ROLE_EXPECTATIONS.get(role_title.lower(), [])

def group_skills(skills_list, skill_to_group):
    """
    Groups skills into predefined categories based on the CSV mapping (skill_to_group).
    Falls back to 'Other' if group is not found.
    """
    from app.synonyms import normalize_skill
    result = {}

    for skill in skills_list:
        norm = normalize_skill(skill)
        group = skill_to_group.get(norm.lower(), "Other")
        result.setdefault(group, []).append(norm)

    return result
