import json
from datetime import datetime
import os

class CrewWorkflow:
    def __init__(self, triager, extractor, reviewer, fallback, log_path="docs/crew_logs_lab13.jsonl"):
        self.triager = triager
        self.extractor = extractor
        self.reviewer = reviewer
        self.fallback = fallback
        self.log_path = log_path
        
        # Створюємо папку, якщо її немає
        os.makedirs(os.path.dirname(self.log_path) if os.path.dirname(self.log_path) else '.', exist_ok=True)

    def process(self, case_id, text):
        # 1. Triager визначає тип
        triage_out = self.triager.run(text)
        
        # 2. Extractor витягує дані
        extract_out = self.extractor.run(text, triage_out)
        
        # 3. Reviewer перевіряє
        review_out = self.reviewer.run(text, extract_out)
        
        # 4. Delegation & Fallback Logic
        fallback_triggered = False
        fallback_out = None
        final_out = extract_out
        status = "accepted_by_reviewer"

        # Якщо Reviewer каже щось інше крім 'accept' або якщо Extractor зламався
        verdict = review_out.get("verdict", "fallback_needed")
        if verdict != "accept" or "error" in extract_out:
            fallback_triggered = True
            fallback_out = self.fallback.run(text, extract_out, review_out)
            final_out = fallback_out
            status = "fallback_applied"

        # Формування логу
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "case_id": case_id,
            "input": text,
            "triager_output": triage_out,
            "extractor_output": extract_out,
            "reviewer_output": review_out,
            "fallback_triggered": fallback_triggered,
            "fallback_output": fallback_out,
            "final_output": final_out,
            "status": status
        }
        
        self._log(log_entry)
        return log_entry

    def _log(self, entry):
        with open(self.log_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')