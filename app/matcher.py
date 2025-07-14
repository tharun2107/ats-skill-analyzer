# # matcher.py
# from collections import Counter
# from rapidfuzz import fuzz, process
# from app.synonyms import normalize_skill
# from app.skills_group import SECTION_WEIGHTS

# def match_skills(jd_skills, resume_section_skills, threshold=85):
#     matched = []
#     missing = []
#     score = 0.0
#     total_weight = 0.0
#     matched_skills_set = set()

#     jd_skills_norm = [normalize_skill(s) for s in jd_skills]

#     for jd_skill in jd_skills_norm:
#         max_score = 0
#         best_section = None

#         for section, resume_skills in resume_section_skills.items():
#             section_weight = SECTION_WEIGHTS.get(section, 1.0)
#             resume_norm = [normalize_skill(s) for s in resume_skills]

#             result = process.extractOne(jd_skill, resume_norm, scorer=fuzz.token_sort_ratio)
#             if result:
#                 match, ratio, _ = result
#                 if ratio >= threshold and (ratio / 100.0) * section_weight > max_score:
#                     max_score = (ratio / 100.0) * section_weight
#                     best_section = section

#         if max_score > 0:
#             score += max_score
#             matched.append(jd_skill)
#             matched_skills_set.add(jd_skill)

#         # ✅ Correct total weight based on best matched section
#         total_weight += SECTION_WEIGHTS.get(best_section, 1.0) if best_section else 1.0

#     missing = [s for s in jd_skills_norm if s not in matched_skills_set]

#     final_score = round((score / total_weight) * 100, 2) if total_weight > 0 else 0.0
#     return matched, missing, final_score

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
                if ratio >= threshold:
                    quality = (ratio / 100.0) ** 1.3  # diminishing returns
                    weighted_score = quality * section_weight
                    if weighted_score > max_score:
                        max_score = weighted_score
                        best_section = section

        if max_score > 0:
            score += max_score
            matched.append(jd_skill)
            matched_skills_set.add(jd_skill)

        total_weight += SECTION_WEIGHTS.get(best_section, 1.0) if best_section else 1.0

    missing = [s for s in jd_skills_norm if s not in matched_skills_set]

    # ✅ Bonus: add score for good certs & achievements (even if not in JD)
    for bonus_section in ["certifications", "achievements"]:
        items = resume_section_skills.get(bonus_section, [])
        bonus_weight = SECTION_WEIGHTS.get(bonus_section, 1.0)
        bonus = 0.05 * len(items) * bonus_weight  # 5% per item * weight
        score += bonus

    # ✅ Final score calculation (capped to max 95%)
    final_score = round((score / total_weight) * 100, 2) if total_weight > 0 else 0.0
    final_score = min(final_score, 95.0)
    return matched, missing, final_score
