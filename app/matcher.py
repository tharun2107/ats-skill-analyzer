# matcher.py
from collections import Counter
from rapidfuzz import fuzz, process
from app.synonyms import normalize_skill
from app.skills_group import SECTION_WEIGHTS

def match_skills(jd_skills, resume_section_skills, threshold=85):
    matched = []
    missing = []
    score = 0.0
    total_weight = 0.0
    matched_skills_set = set()

    jd_skills_norm = [normalize_skill(s) for s in jd_skills]

    for jd_skill in jd_skills_norm:
        max_score = 0
        best_section = None

        for section, resume_skills in resume_section_skills.items():
            section_weight = SECTION_WEIGHTS.get(section, 1.0)
            resume_norm = [normalize_skill(s) for s in resume_skills]

            result = process.extractOne(jd_skill, resume_norm, scorer=fuzz.token_sort_ratio)
            if result:
                match, ratio, _ = result
                if ratio >= threshold and (ratio / 100.0) * section_weight > max_score:
                    max_score = (ratio / 100.0) * section_weight
                    best_section = section

        if max_score > 0:
            score += max_score
            matched.append(jd_skill)
            matched_skills_set.add(jd_skill)

        # ✅ Correct total weight based on best matched section
        total_weight += SECTION_WEIGHTS.get(best_section, 1.0) if best_section else 1.0

    missing = [s for s in jd_skills_norm if s not in matched_skills_set]

    final_score = round((score / total_weight) * 100, 2) if total_weight > 0 else 0.0
    return matched, missing, final_score
