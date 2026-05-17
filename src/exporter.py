class Exporter:
    def run(self, state: dict) -> dict:
        export_record = {
            "case_id": state["case_id"],
            "route": state["route"],
            "final_data": state["extracted_data"] if not state["fallback_triggered"] else None,
            "needs_manual_review": state.get("fallback_result", {}).get("needs_manual_review", False),
            "status": "exported_successfully" if not state["fallback_triggered"] else "exported_with_warning",
            "warnings": state["warnings"]
        }
        
        state["final_output"] = export_record
        
        # Оновлюємо глобальний статус стейту
        if state["fallback_triggered"]:
            state["status"] = "exported_with_warning"
        else:
            state["status"] = "exported_successfully"
            
        return {"step": "export", "status": state["status"]}