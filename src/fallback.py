class FallbackHandler:
    def run(self, text, extracted_data, reviewer_output):
        """
        Safe failure handler.
        If extraction is rejected, we keep the partial extraction but flag it aggressively.
        """
        verdict = reviewer_output.get("verdict", "fallback_needed")
        issues = reviewer_output.get("issues", [])
        
        return {
            "status": "failed_and_caught",
            "reason": reviewer_output.get("recommended_action", f"Reviewer rejected with verdict: {verdict}"),
            "identified_issues": issues,
            "partial_output": extracted_data,
            "needs_manual_review": True
        }