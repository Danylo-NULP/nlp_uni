from .flow_state import create_initial_state
from .router import Router
from .executor import Executor
from .validator14 import Validator
from .fallback14 import Fallback
from .exporter import Exporter
from .flow_logger import FlowLogger

class DocumentProcessingFlow:
    def __init__(self, llm_caller):
        self.router = Router(llm_caller)
        self.executor = Executor(llm_caller)
        self.validator = Validator()
        self.fallback = Fallback()
        self.exporter = Exporter()
        self.logger = FlowLogger()

    def process(self, case_id: str, raw_text: str) -> dict:
        steps_log = []
        
        # 1. INGEST
        state = create_initial_state(case_id, raw_text)
        if not raw_text.strip():
            state["errors"].append("Input text is empty.")
            state["status"] = "failed"
            steps_log.append({"step": "ingest", "status": "error", "error": "Empty input"})
        else:
            state["clean_text"] = raw_text.strip().replace("\n", " ")
            state["status"] = "ingested"
            steps_log.append({"step": "ingest", "status": "ok"})

        # 2. ROUTE
        if not state["errors"]:
            steps_log.append(self.router.run(state))

        # 3. EXECUTE
        if not state["errors"]:
            steps_log.append(self.executor.run(state))

        # 4. VALIDATE
        if not state["errors"]:
            steps_log.append(self.validator.run(state))

        # 5. FALLBACK
        steps_log.append(self.fallback.run(state))

        # 6. EXPORT
        steps_log.append(self.exporter.run(state))

        # ЛОГУВАННЯ
        self.logger.log_flow_run(state, steps_log)

        return state["final_output"]