import json
from src.llm_extract import build_extraction_prompt
from src.validator import validate_extraction

def build_repair_prompt(broken_output, error_msg, schema):
    """Формує промпт для виправлення помилки."""
    return f"""
Your previous response failed JSON Validation. Please fix it.

Error message from validator:
{error_msg}

Your broken output:
{broken_output}

Expected JSON Schema:
{json.dumps(schema, indent=2)}

CRITICAL RULES:
1. Fix the JSON so it strictly passes the schema and parsing rules.
2. Return ONLY valid JSON, no markdown formatting (no ```), no explanations.
"""

def run_extraction_with_repair(text, schema, llm_call_func, max_repairs=2):
    """
    Виконує extraction та запускає repair loop у разі помилки.
    llm_call_func: функція, яка приймає prompt і повертає текст від LLM.
    """
    # Ітерація 0: Базовий extraction
    prompt = build_extraction_prompt(text, schema)
    llm_output = llm_call_func(prompt)
    
    is_valid, parsed_json, error_msg = validate_extraction(llm_output, schema)
    
    repairs_used = 0
    repair_history = []

    # Цикл виправлення (Repair Loop)
    while not is_valid and repairs_used < max_repairs:
        repairs_used += 1
        repair_prompt = build_repair_prompt(llm_output, error_msg, schema)
        llm_output = llm_call_func(repair_prompt)
        
        is_valid, parsed_json, new_error_msg = validate_extraction(llm_output, schema)
        
        repair_history.append({
            "attempt": repairs_used,
            "previous_error": error_msg,
            "new_output": llm_output,
            "success": is_valid
        })
        
        error_msg = new_error_msg

    return {
        "final_json": parsed_json,
        "is_valid": is_valid,
        "repairs_used": repairs_used,
        "final_error": error_msg,
        "raw_output": llm_output,
        "repair_history": repair_history
    }