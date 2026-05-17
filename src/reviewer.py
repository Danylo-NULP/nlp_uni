from .agents import clean_json_response

class Reviewer:
    def __init__(self, llm_caller):
        self.llm = llm_caller

    def run(self, text, extracted_data):
        import json
        
        prompt = f"""You are a strict Reviewer for an Image Caption Analysis Crew.
Compare the Extracted JSON against the Original Caption.

Original Caption: "{text}"
Extracted JSON: {json.dumps(extracted_data, ensure_ascii=False)}

Check for:
1. Hallucinations (did the Extractor invent colors, clothing, or actions not explicitly in the text?).
2. Missing obvious fields.
3. Consistency.

Return ONLY a JSON object with:
- "verdict": strictly one of ["accept", "repair_needed", "fallback_needed", "manual_review"]
- "issues": array of objects {{"field": "...", "problem": "..."}} (leave empty [] if accepted)
- "recommended_action": short string advising what to do next
"""
        response = self.llm(prompt)
        return clean_json_response(response)