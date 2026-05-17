import json
import os
from datetime import datetime

class FlowLogger:
    def __init__(self, log_path="docs/flow_logs_lab14.jsonl"):
        self.log_path = log_path
        os.makedirs(os.path.dirname(self.log_path) if os.path.dirname(self.log_path) else '.', exist_ok=True)

    def log_flow_run(self, state: dict, steps_log: list):
        """
        Зберігає повний запис про проходження Flow для одного кейсу.
        """
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "case_id": state.get("case_id"),
            "input": state.get("raw_text"),
            "steps": steps_log,
            "route": state.get("route"),
            "validation_issues": state.get("validation_issues"),
            "fallback_triggered": state.get("fallback_triggered"),
            "export_output": state.get("final_output"),
            "final_status": state.get("status"),
            "errors": state.get("errors"),
            "warnings": state.get("warnings")
        }
        
        with open(self.log_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')