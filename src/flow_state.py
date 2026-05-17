def create_initial_state(case_id: str, raw_text: str) -> dict:
    """
    Ініціалізує порожній об'єкт стану для нового прогону Flow.
    """
    return {
        "case_id": case_id,
        "raw_text": raw_text,
        "clean_text": None,
        "route": None,
        "schema": None,
        "extracted_data": None,
        "validation_issues": [],
        "fallback_triggered": False,
        "fallback_result": None,
        "final_output": None,
        "status": "initialized",
        "errors": [],
        "warnings": []
    }