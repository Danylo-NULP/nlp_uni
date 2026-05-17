def run_crew_evaluation(test_cases, crew, baseline_caller=None):
    """
    Проганяє список тестів через Multi-agent crew.
    Опціонально робить виклик Baseline моделі для порівняння.
    """
    results = []
    
    for case in test_cases:
        task_id = case["id"]
        input_text = case["text"]
        
        print(f"--- Processing Task: {task_id} ---")
        
        # Запуск базової моделі (без crew workflow)
        baseline_answer = None
        if baseline_caller:
            baseline_prompt = f"Extract structured details (subjects, actions, visual attributes) from this image caption: '{input_text}'"
            baseline_answer = baseline_caller(baseline_prompt)
            
        # Запуск Multi-agent Crew
        crew_result = crew.process(task_id, input_text)
        
        results.append({
            "task_id": task_id,
            "input": input_text,
            "expected_behavior": case.get("expected_behavior", ""),
            "baseline_answer": baseline_answer,
            "crew_status": crew_result["status"],
            "fallback_triggered": crew_result["fallback_triggered"],
            "final_output": crew_result["final_output"]
        })
        
    return results