
from collections import Counter
from rapidfuzz import fuzz, process  # pip install rapidfuzz
from .synonyms import normalize_skill  # Import your normalization function
def compute_weights(jd_skills, jd_text):
    # Assign weight 1 to every skill
    return {skill: 1 for skill in jd_skills}
def match_skills(jd_skills, resume_skills, jd_text=None, threshold=85):
    weights = compute_weights(jd_skills, jd_text or "")

    # Normalize all skills for better matching
    resume_skills_norm = [normalize_skill(s) for s in resume_skills]
    jd_skills_norm = [normalize_skill(s) for s in jd_skills]

    matched = []
    missing = []
    score = 0.0
    total_weight = sum(weights.get(skill, 1) for skill in jd_skills)

    for orig_skill, norm_skill in zip(jd_skills, jd_skills_norm):
        weight = weights.get(orig_skill, 1)
        # Fuzzy match using normalized skills
        result = process.extractOne(norm_skill, resume_skills_norm, scorer=fuzz.token_sort_ratio)
        if result:
            match, ratio, _ = result  # Unpack all three values
            if ratio >= threshold:
                quality = ratio / 100.0
                score += weight * quality
                matched.append(orig_skill)
            else:
                missing.append(orig_skill)
        else:
            missing.append(orig_skill)

    final_score = round((score / total_weight) * 100, 2) if total_weight > 0 else 0.0
    return matched, missing, final_score