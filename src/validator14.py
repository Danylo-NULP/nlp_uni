from jsonschema import validate, ValidationError

class Validator:
    def run(self, state: dict) -> dict:
        if not state.get("extracted_data"):
            state["status"] = "validation_failed"
            return {"step": "validate", "status": "error", "issues": ["No data to validate"]}

        data = state["extracted_data"]
        schema = state["schema"]
        issues = []

        # 1. Перевірка схеми
        try:
            validate(instance=data, schema=schema)
        except ValidationError as e:
            issues.append(f"Schema violation: {e.message}")

        # 2. Проста перевірка на null у required полях (додатково)
        for req_field in schema.get("required", []):
            if data.get(req_field) is None and req_field != "clothing": # clothing може бути порожнім масивом
                issues.append(f"Required field '{req_field}' is null.")

        if issues:
            state["validation_issues"] = issues
            state["status"] = "validation_failed"
            return {"step": "validate", "status": "warning", "issues": issues}
        
        state["status"] = "validated_successfully"
        return {"step": "validate", "status": "ok"}