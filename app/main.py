# from flask import Flask, request, jsonify
# from app.skills_loader import load_skills
# from app.extractor import SkillExtractor
# from app.matcher import match_skills
# from app.synonyms import normalize_skill  # Optional, used in extractor
# from app.role_expectations import infer_expected_skills, group_skills # Optional, used for role inference
# app = Flask(__name__)

# # ✅ Load skills list AND skill-to-group mapping from CSV
# skills_list, skill_to_group = load_skills()

# # ✅ Initialize the extractor
# extractor = SkillExtractor(skills_list)

# # ✅ Grouping helper
# def group_skills(skill_list):
#     grouped = {}
#     for skill in skill_list:
#         group = skill_to_group.get(skill.lower(), "Other")
#         grouped.setdefault(group, []).append(skill)
#     return grouped


# @app.route('/analyze', methods=['POST'])
# def analyze():
#     print("🔥 This is the latest version of main.py")  # Debug print

#     data = request.get_json()
#     resume_text = data.get('resume', '')
#     jd_text = data.get('job_description', '')
#     job_role = data.get('job_role', '').strip().lower()

#     resume_skills = extractor.extract(resume_text)
#     jd_skills_extracted = extractor.extract(jd_text)

#     # If JD skills are empty but job_role is known, infer from role
#     inferred_skills = infer_expected_skills(job_role)
#     if not jd_skills_extracted and inferred_skills:
#         jd_skills = inferred_skills
#     else:
#         jd_skills = jd_skills_extracted

#     matched, missing, score = match_skills(jd_skills, resume_skills)

#     return jsonify({
#         "jd_skills": jd_skills,
#         "resume_skills": resume_skills,
#         "matched_skills": matched,
#         "missing_skills": missing,
#         "score": score,
#         "grouped_jd_skills": group_skills(jd_skills),
#         "grouped_resume_skills": group_skills(resume_skills),
#         "grouped_missing_skills": group_skills(missing),
#         "expected_coverage": group_skills(inferred_skills) if inferred_skills else {}
#     })


# if __name__ == '__main__':
#     app.run(debug=True)

# main.py 1
# from flask import Flask, request, jsonify
# from app.skills_loader import load_skills
# from app.extractor import SkillExtractor
# from app.matcher import match_skills
# from app.role_expectations import infer_expected_skills, group_skills

# app = Flask(__name__)

# skills_list, skill_to_group = load_skills()
# extractor = SkillExtractor(skills_list)

# def group_skills_by_map(skill_list):
#     grouped = {}
#     for skill in skill_list:
#         group = skill_to_group.get(skill.lower(), "Other")
#         grouped.setdefault(group, []).append(skill)
#     return grouped

# @app.route('/analyze', methods=['POST'])
# def analyze():
#     data = request.get_json()
#     resume_text = data.get('resume', '')
#     jd_text = data.get('job_description', '')
#     job_role = data.get('job_role', '').strip().lower()

#     jd_skills_extracted = extractor.extract(jd_text)
#     inferred_skills = infer_expected_skills(job_role)
#     jd_skills = inferred_skills if not jd_skills_extracted and inferred_skills else jd_skills_extracted

#     resume_section_skills = extractor.extract_section_wise(resume_text)

#     matched, missing, score = match_skills(jd_skills, resume_section_skills)

#     return jsonify({
#         "jd_skills": jd_skills,
#         "resume_skills_by_section": resume_section_skills,
#         "matched_skills": matched,
#         "missing_skills": missing,
#         "score": score
#     })

# if __name__ == '__main__':
#     app.run(debug=True)
# working version

# from flask import Flask, request, jsonify
# from app.skills_loader import load_skills
# from app.extractor import SkillExtractor
# from app.matcher import match_skills
# from app.role_expectations import infer_expected_skills
# from app.feedback import generate_feedback_summary  # ✅ already present

# app = Flask(__name__)

# # Load skills and skill-to-group map
# skills_list, skill_to_group = load_skills()
# extractor = SkillExtractor(skills_list)

# def group_skills_by_map(skill_list):
#     grouped = {}
#     for skill in skill_list:
#         group = skill_to_group.get(skill.lower(), "Other")
#         grouped.setdefault(group, []).append(skill)
#     return grouped

# @app.route('/analyze', methods=['POST'])
# def analyze():
#     print("🔥 This is the latest version of main.py")
#     data = request.get_json()
#     resume_text = data.get('resume', '')
#     jd_text = data.get('job_description', '')
#     job_role = data.get('job_role', '').strip().lower()

#     # Extract JD skills from text or fallback to inferred
#     jd_skills_extracted = extractor.extract(jd_text)
#     inferred_skills = infer_expected_skills(job_role)
#     jd_skills = inferred_skills if not jd_skills_extracted and inferred_skills else jd_skills_extracted

#     # Extract resume skills by section (including certifications and achievements)
#     resume_section_skills = extractor.extract_section_wise(resume_text)

#     # Match and compute score
#     matched, missing, score = match_skills(jd_skills, resume_section_skills)

#     # Generate feedback summary
#     feedback = generate_feedback_summary(score, matched, missing, job_role)

#     return jsonify({
#         "jd_skills": jd_skills,
#         "resume_skills_by_section": resume_section_skills,
#         "matched_skills": matched,
#         "missing_skills": missing,
#         "score": score,
#         "feedback_summary": feedback,
#         "grouped_jd_skills": group_skills_by_map(jd_skills),
#         "grouped_missing_skills": group_skills_by_map(missing)
#     })

# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, request, jsonify
import fitz  # PyMuPDF
from app.skills_loader import load_skills
from app.extractor import SkillExtractor
from app.matcher import match_skills
from app.role_expectations import infer_expected_skills, group_skills
from app.resume_splitter import split_resume_sections  # your section logic

app = Flask(__name__)

skills_list, skill_to_group = load_skills()
extractor = SkillExtractor(skills_list)

def extract_text_from_pdf(pdf_bytes):
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

@app.route('/analyze', methods=['POST'])
def analyze():
    print("🔥 ML Service Called")
    
    # Check if PDF file is sent
    resume_text = ""
    if 'resume' in request.files:
        pdf_file = request.files['resume']
        resume_text = extract_text_from_pdf(pdf_file.read())
    else:
        resume_text = request.form.get('resume', '')

    jd_text = request.form.get('job_description', '')
    job_role = request.form.get('job_role', '').strip().lower()

    resume_sections = split_resume_sections(resume_text)
    resume_section_skills = {
        section: extractor.extract(text)
        for section, text in resume_sections.items()
    }

    jd_skills_extracted = extractor.extract(jd_text)
    inferred_skills = infer_expected_skills(job_role)
    jd_skills = inferred_skills if not jd_skills_extracted and inferred_skills else jd_skills_extracted

    matched, missing, score = match_skills(jd_skills, resume_section_skills)

    def group(skills): return group_skills(skills, skill_to_group)

    return jsonify({
        "jd_skills": jd_skills,
        "matched_skills": matched,
        "missing_skills": missing,
        "score": score,
        "resume_skills_by_section": resume_section_skills,
        "grouped_jd_skills": group(jd_skills),
        "grouped_resume_skills": {
            k: group(v) for k, v in resume_section_skills.items()
        },
        "grouped_missing_skills": group(missing)
    })

if __name__ == '__main__':
    app.run(debug=True)
