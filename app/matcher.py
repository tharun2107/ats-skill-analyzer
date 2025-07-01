def match_skills(jd_skills, resume_skills):
    jd_set = set([skill.lower() for skill in jd_skills])
    resume_set = set([skill.lower() for skill in resume_skills])

    matched = sorted(list(jd_set & resume_set))
    missing = sorted(list(jd_set - resume_set))

    score = round((len(matched) / len(jd_set)) * 100, 2) if jd_set else 0

    return matched, missing, score
