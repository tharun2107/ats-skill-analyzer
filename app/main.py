from flask import Flask, request, jsonify
import fitz  # PyMuPDF
from app.skills_loader import load_skills
from app.extractor import SkillExtractor
from app.matcher import match_skills
from app.role_expectations import infer_expected_skills, group_skills

app = Flask(__name__)

# Load skills list and skill-to-group mapping
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

    resume_text = ""
    jd_text = ""
    job_role = ""

    if request.is_json:
        # JSON request (from curl or frontend JS fetch)
        data = request.get_json()
        resume_text = data.get("resume", "")
        jd_text = data.get("job_description", "")
        job_role = data.get("job_role", "").strip().lower()
    else:
        # Form-data request (file upload from frontend)
        if 'resume' in request.files:
            pdf_file = request.files['resume']
            resume_text = extract_text_from_pdf(pdf_file.read())  # ✅ ACTUAL PDF parsing
        else:
            resume_text = request.form.get("resume", "")  # fallback for raw text

        jd_text = request.form.get("job_description", "")
        job_role = request.form.get("job_role", "").strip().lower()

    print("JD TEXT (preview):", jd_text[:100])
    print("Resume TEXT (preview):", resume_text[:100])

    # 🔥 Extract section-wise skills
    resume_section_skills = extractor.extract_section_wise(resume_text)

    # Extract skills from JD
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
            section: group(skills) for section, skills in resume_section_skills.items()
        },
        "grouped_missing_skills": group(missing)
    })

if __name__ == '__main__':
    app.run(debug=True)
