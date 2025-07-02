# extractor.py
import spacy
from spacy.matcher import PhraseMatcher
from app.synonyms import normalize_skill

SECTION_HEADERS = ["experience", "projects", "education", "certifications", "skills", "summary"]

class SkillExtractor:
    def __init__(self, skills_list):
        self.nlp = spacy.load("en_core_web_sm")
        self.matcher = PhraseMatcher(self.nlp.vocab, attr="LOWER")
        patterns = [self.nlp.make_doc(skill) for skill in skills_list]
        self.matcher.add("SKILLS", patterns)

    def extract(self, text):
        doc = self.nlp(text)
        matches = self.matcher(doc)
        skills_found = set()
        for _, start, end in matches:
            raw = doc[start:end].text.lower().strip()
            normalized = normalize_skill(raw)
            skills_found.add(normalized)
        return list(skills_found)

    def extract_section_wise(self, resume_text):
        # Simple split by headers
        sections = {}
        current_section = "default"
        lines = resume_text.splitlines()

        for line in lines:
            line_clean = line.strip().lower().strip(":")
            if line_clean in SECTION_HEADERS:
                current_section = line_clean
                sections[current_section] = []
            else:
                sections.setdefault(current_section, []).append(line)

        result = {}
        for section, lines in sections.items():
            text = " ".join(lines)
            result[section] = self.extract(text)
        return result
