class Fallback:
    def run(self, state: dict) -> dict:
        # Fallback спрацьовує, якщо є помилки виконання, невідомий маршрут або провалена валідація
        if state["status"] == "validated_successfully" and not state["errors"]:
            return {"step": "fallback", "status": "skipped"}

        state["fallback_triggered"] = True
        
        # Стратегія Safe Failure: зберігаємо те, що є, але маркуємо для ручної перевірки
        fallback_record = {
            "action_taken": "safe_failure",
            "reason": state.get("validation_issues", ["Unknown execution error"]),
            "needs_manual_review": True
        }
        
        state["fallback_result"] = fallback_record
        state["status"] = "fallback_applied"
        state["warnings"].append("Case routed to manual review due to validation/execution issues.")
        
        return {"step": "fallback", "status": "executed", "details": fallback_record}