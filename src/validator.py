import json
from jsonschema import validate
from jsonschema.exceptions import ValidationError

def validate_extraction(llm_output, schema):
    """
    Перевіряє вихід LLM на валідність JSON та відповідність схемі.
    Повертає: (is_valid: bool, parsed_json: dict, error_message: str)
    """
    # Крок 1: Parse JSON (з очищенням можливого Markdown від LLM)
    try:
        cleaned_output = llm_output.strip()
        # Прибираємо бекстіки (```json ... ```), які часто додають LLM
        if cleaned_output.startswith("```json"):
            cleaned_output = cleaned_output[7:]
        elif cleaned_output.startswith("```"):
            cleaned_output = cleaned_output[3:]
        if cleaned_output.endswith("```"):
            cleaned_output = cleaned_output[:-3]
            
        cleaned_output = cleaned_output.strip()
        parsed_json = json.loads(cleaned_output)
        
    except json.JSONDecodeError as e:
        return False, None, f"JSON Parse Error: {str(e)}"

    # Крок 2: Validate against Schema
    try:
        validate(instance=parsed_json, schema=schema)
    except ValidationError as e:
        return False, parsed_json, f"Schema Validation Error: {e.message}"

    return True, parsed_json, None