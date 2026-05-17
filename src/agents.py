import json
import re

def clean_json_response(raw_text):
    """Очищає відповідь локальної LLM від Markdown та іншого сміття."""
    raw_text = raw_text.strip()
    if "```json" in raw_text:
        raw_text = raw_text.split("```json")[1].split("```")[0]
    elif "```" in raw_text:
        raw_text = raw_text.split("```")[1].split("```")[0]
    
    # Спроба знайти JSON-подібний блок, якщо немає бекстіків
    match = re.search(r'\{.*\}', raw_text, re.DOTALL)
    if match:
        raw_text = match.group(0)
        
    try:
        return json.loads(raw_text)
    except json.JSONDecodeError:
        return {"error": "Invalid JSON", "raw_output": raw_text}

class Triager:
    def __init__(self, llm_caller):
        self.llm = llm_caller

    def run(self, text):
        prompt = f"""You are a Triager for an Image Caption Analysis Crew.
Determine the main focus of the image caption to route it to the correct extraction schema.

Focus categories:
- "human_focus": mainly about people.
- "animal_focus": mainly about animals.
- "scenery_focus": mainly about inanimate objects, buildings, or nature.

Caption: "{text}"

Return ONLY a JSON object with:
- "task_type": "caption_routing"
- "route": <the chosen focus category>
- "expected_fields": array of strings (For human: ["subject", "action", "clothing"]. For animal: ["animal_type", "action", "color"]. For scenery: ["main_objects", "setting"])
- "difficulty": "easy", "medium", or "hard"
"""
        response = self.llm(prompt)
        return clean_json_response(response)

class Extractor:
    def __init__(self, llm_caller):
        self.llm = llm_caller

    def run(self, text, triage_info):
        route = triage_info.get('route', 'human_focus')
        fields = triage_info.get('expected_fields', [])
        
        prompt = f"""You are an Extractor for an Image Caption Analysis Crew.
Extract structured data from the caption based on the provided route.

Caption: "{text}"
Route: {route}
Fields to extract: {fields}

CRITICAL RULES:
1. Return ONLY valid JSON.
2. Keys must exactly match the "Fields to extract".
3. Do NOT hallucinate. Use null if a field is not present in the text.
4. Add a "confidence_note" field explaining your extraction.
"""
        response = self.llm(prompt)
        return clean_json_response(response)