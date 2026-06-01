from app.agents.base_agent import BaseAgent
from app.core.llm import llm_service
from app.core.logging import logger


class GeneralAgent(BaseAgent):

    def execute(self, task: str):

        logger.info(f"General agent processing: {task}")

        prompt = f"""
You are a helpful assistant.

Answer the user's question clearly and concisely.

Task:
{task}
"""

        response = llm_service.generate(prompt)

        return {
            "response": response
        }