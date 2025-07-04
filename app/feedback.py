# feedback.py
def generate_feedback_summary(score, matched_skills, missing_skills, job_role=""):
    role = job_role.title() if job_role else "this role"

    # Score-based intro
    if score >= 85:
        feedback = f"You are an excellent fit for the {role}. "
    elif score >= 60:
        feedback = f"You are a good fit for the {role}. "
    elif score >= 40:
        feedback = f"You are a moderate fit for the {role}. "
    else:
        feedback = f"You currently have limited alignment with the {role} requirements. "

    # Matched skills
    if matched_skills:
        skills_str = ", ".join(matched_skills[:5])
        feedback += f"You already demonstrate strengths in {skills_str}. "

    # Missing skills
    if missing_skills:
        if score >= 60:
            feedback += "Improving your proficiency in "
        else:
            feedback += "To become a stronger candidate, focus on learning "
        feedback += ", ".join(missing_skills[:5]) + ". "

    # Final note
    if score < 60:
        feedback += "Keep working on these areas to improve your alignment."
    else:
        feedback += "You're very close — polish a few more skills and you're there!"

    return feedback
