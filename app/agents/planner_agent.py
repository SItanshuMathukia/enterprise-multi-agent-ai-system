from app.agents.base_agent import BaseAgent
from app.core.llm import llm_service
from app.schemas.planner import PlanResponse
from app.utils.json_cleaner import clean_llm_response
from app.core.logging import logger
from app.core.llm import llm


class PlannerAgent(BaseAgent):

    def execute(self, task: str):

        logger.info(f"Planning task: {task}")

        prompt = f"""
        You are a senior software architect.

        Create a step-by-step implementation plan.

        Return ONLY valid JSON.

        Example:
        {{
            "steps": [
                {{
                    "id": 1,
                    "title": "Setup project"
                }}
            ]
        }}

        Task:
        {task}
        """

        response = llm_service.generate(prompt)

        cleaned_response = clean_llm_response(response)

        parsed = PlanResponse.model_validate_json(cleaned_response)

        return parsed.model_dump()