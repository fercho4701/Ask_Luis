import json

class PromptService:

    def build_prompt(self, context, question):
        context_json = json.dumps(
            context,
            ensure_ascii=False,
            indent=2
        )

        return f"""
Información profesional de Luis:

{context_json}

Pregunta del reclutador:
{question}
"""