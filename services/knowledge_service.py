import json

class KnowledgeService:

    def load_json(self, file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)

    def load_all(self):
        return {
            "profile": self.load_json("data/profile.json"),
            "experience": self.load_json("data/experience.json"),
            "education": self.load_json("data/education.json"),
            "projects": self.load_json("data/projects.json"),
            "contact": self.load_json("data/contact.json")
        }