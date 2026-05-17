import json

class Executor:
    def __init__(self, llm_caller):
        self.llm = llm_caller

    def run(self, state: dict) -> dict:
        if state["route"] == "unknown" or not state["schema"]:
            return {"step": "execute", "status": "skipped", "reason": "No valid route/schema"}

        text = state["clean_text"]
        schema = state["schema"]
        
        prompt = f"""Extract structured information from the caption according to this JSON schema:
{json.dumps(schema, indent=2)}

Caption: "{text}"

CRITICAL RULES:
1. Return ONLY valid JSON.
2. Do NOT invent details (no hallucinations). Use null if missing.
"""
        response = self.llm(prompt)
        
        try:
            clean_resp = response.replace("```json", "").replace("```", "").strip()
            extracted_data = json.loads(clean_resp)
            state["extracted_data"] = extracted_data
            return {"step": "execute", "status": "ok", "method": "llm_extraction"}
        except Exception as e:
            state["errors"].append(f"Execution failed: {str(e)}")
            return {"step": "execute", "status": "error", "error": str(e)}