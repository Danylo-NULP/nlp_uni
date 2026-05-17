import json
from .tools import AVAILABLE_TOOLS
from .tool_logger import ToolLogger

class ToolGroundedAgent:
    def __init__(self, llm_caller, logger: ToolLogger, max_steps=4):
        self.llm = llm_caller
        self.logger = logger
        self.max_steps = max_steps
        self.tools = AVAILABLE_TOOLS

    def build_system_prompt(self):
        tool_descriptions = """
1. extract_visual_attributes: Extracts colors and clothing from text. Input format: {"text": "<caption text>"}
2. validate_caption_length: Checks if text has >= 5 words. Input format: {"text": "<caption text>"}
3. check_animal_presence: Checks for animals in the text. Input format: {"text": "<caption text>"}
"""
        return f"""
You are an Image Caption Quality Agent. You analyze descriptions of photos and use tools to verify their content.
Available tools:
{tool_descriptions}

You must respond STRICTLY in JSON format with ONE of these two structures:

OPTION 1: To call a tool
{{
    "thought": "I need to check the length of the caption.",
    "tool_name": "validate_caption_length",
    "tool_input": {{"text": "A man running"}}
}}

OPTION 2: To give the final answer
{{
    "thought": "I have all the info. The caption is short and has no colors.",
    "final_answer": "This caption is invalid because it is too short and lacks visual details."
}}
"""

    def run(self, task_id: str, user_input: str):
        conversation_history = self.build_system_prompt() + f"\n\nUser Task: Analyze this caption: '{user_input}'"
        
        tool_call_count = 0
        
        for step in range(self.max_steps):
            # 1. Запитуємо LLM
            llm_response = self.llm(conversation_history)
            
            # 2. Парсимо JSON від агента
            try:
                # Очищення Markdown (якщо LLM додала бекстіки)
                cleaned_response = llm_response.replace("```json", "").replace("```", "").strip()
                agent_action = json.loads(cleaned_response)
            except json.JSONDecodeError:
                conversation_history += f"\n\nSystem Error: Your response was not valid JSON. You MUST return JSON only. Broken response: {llm_response}"
                continue

            # 3. Перевіряємо, чи це фінальна відповідь
            if "final_answer" in agent_action:
                return {
                    "task_id": task_id,
                    "tool_calls": tool_call_count,
                    "final_answer": agent_action["final_answer"],
                    "status": "success"
                }
                
            # 4. Викликаємо інструмент
            if "tool_name" in agent_action and "tool_input" in agent_action:
                tool_name = agent_action["tool_name"]
                tool_input = agent_action["tool_input"]
                tool_call_count += 1
                
                if tool_name not in self.tools:
                    error_msg = f"Tool '{tool_name}' not found."
                    self.logger.log_call(task_id, tool_name, tool_input, None, False, error_msg)
                    conversation_history += f"\n\nTool Result: Error - {error_msg}"
                    continue
                    
                # Виконання інструменту
                try:
                    tool_func = self.tools[tool_name]
                    tool_output = tool_func(tool_input)
                    # Успішне логування
                    self.logger.log_call(task_id, tool_name, tool_input, tool_output, True)
                    conversation_history += f"\n\nTool Result for '{tool_name}':\n{json.dumps(tool_output)}"
                except Exception as e:
                    # Логування помилки інструменту
                    self.logger.log_call(task_id, tool_name, tool_input, None, False, str(e))
                    conversation_history += f"\n\nTool Result for '{tool_name}': Error - {str(e)}"
            else:
                conversation_history += "\n\nSystem Error: Missing required fields in JSON."
                
        return {
            "task_id": task_id,
            "tool_calls": tool_call_count,
            "final_answer": "Agent reached maximum steps without a final answer.",
            "status": "timeout"
        }