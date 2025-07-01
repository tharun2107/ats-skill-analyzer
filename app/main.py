from flask import Flask, request, jsonify
from app.skills_loader import load_skills
from app.extractor import SkillExtractor
from app.matcher import match_skills
from app.synonyms import normalize_skill  # Optional, used in extractor

app = Flask(__name__)

# Load skills list from Excel once at startup
skills_list = load_skills()

# Initialize the extractor with the skills list
extractor = SkillExtractor(skills_list)

@app.route('/analyze', methods=['POST'])
def analyze():
    print("🔥 This is the latest version of main.py")  # Debug print

    data = request.get_json()
    resume_text = data.get('resume', '')
    jd_text = data.get('job_description', '')

    # Extract skills from resume and job description
    resume_skills = extractor.extract(resume_text)
    jd_skills = extractor.extract(jd_text)

    # Match and score
    matched, missing, score = match_skills(jd_skills, resume_skills)

    return jsonify({
        'matched_skills': matched,
        'missing_skills': missing,
        'score': score,
        'jd_skills': jd_skills,
        'resume_skills': resume_skills
    })

if __name__ == '__main__':
    app.run(debug=True)
