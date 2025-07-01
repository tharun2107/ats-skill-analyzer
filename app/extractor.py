import spacy
from spacy.matcher import PhraseMatcher

class SkillExtractor:
    def __init__(self, skills_list):
        self.nlp = spacy.load("en_core_web_sm")
        self.matcher = PhraseMatcher(self.nlp.vocab, attr="LOWER")
        patterns = [self.nlp.make_doc(skill) for skill in skills_list]
        self.matcher.add("SKILLS", patterns)

    def extract(self, text):
        doc = self.nlp(text)
        matches = self.matcher(doc)
        skills_found = set([doc[start:end].text.lower() for match_id, start, end in matches])
        return list(skills_found)