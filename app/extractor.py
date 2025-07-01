import spacy
from spacy.matcher import PhraseMatcher
from app.synonyms import normalize_skill

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
