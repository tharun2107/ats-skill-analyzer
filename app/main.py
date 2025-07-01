from flask import Flask, request, jsonify
from app.skills_loader import load_skills
from app.extractor import SkillExtractor
from app.matcher import match_skills

app = Flask(__name__)

skills_list = load_skills()
extractor = SkillExtractor(skills_list)

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    resume_text = data.get('resume', '')
    jd_text = data.get('job_description', '')

    resume_skills = extractor.extract(resume_text)
    jd_skills = extractor.extract(jd_text)

    result = match_skills(jd_skills, resume_skills)
    result.update({
        "jd_skills": jd_skills,
        "resume_skills": resume_skills
    })

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)