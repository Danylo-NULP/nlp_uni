import json

# Read-only Knowledge: Схеми для різних типів сцен
SCHEMAS = {
    "human_extraction": {
        "type": "object",
        "properties": {
            "subject": {"type": "string"},
            "action": {"type": "string"},
            "clothing": {"type": "array", "items": {"type": "string"}}
        },
        "required": ["subject", "action", "clothing"],
        "additionalProperties": False
    },
    "animal_extraction": {
        "type": "object",
        "properties": {
            "animal_type": {"type": "string"},
            "action": {"type": "string"},
            "color": {"type": "string"}
        },
        "required": ["animal_type", "action", "color"],
        "additionalProperties": False
    },
    "scenery_extraction": {
        "type": "object",
        "properties": {
            "main_objects": {"type": "array", "items": {"type": "string"}},
            "setting": {"type": "string"}
        },
        "required": ["main_objects", "setting"],
        "additionalProperties": False
    }
}

class Router:
    def __init__(self, llm_caller):
        self.llm = llm_caller

    def run(self, state: dict) -> dict:
        text = state["clean_text"]
        
        prompt = f"""Analyze the image caption and classify its primary focus.
Categories:
1. "human_extraction" (mainly about people)
2. "animal_extraction" (mainly about animals)
3. "scenery_extraction" (mainly about objects/nature, no main actors)

Caption: "{text}"

Return ONLY a valid JSON object:
{{"route": "<category_name>", "reason": "<brief explanation>"}}
"""
        response = self.llm(prompt)
        
        try:
            # Очищення можливого Markdown
            clean_resp = response.replace("```json", "").replace("```", "").strip()
            parsed = json.loads(clean_resp)
            route = parsed.get("route", "scenery_extraction")
            
            if route not in SCHEMAS:
                route = "scenery_extraction" # Default fallback route
                
            state["route"] = route
            state["schema"] = SCHEMAS[route]
            
            return {"step": "route", "status": "ok", "route": route, "reason": parsed.get("reason")}
        except Exception as e:
            state["route"] = "unknown"
            state["errors"].append(f"Routing failed: {str(e)}")
            return {"step": "route", "status": "error", "error": str(e)}