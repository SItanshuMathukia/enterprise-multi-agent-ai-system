import re

from app.agents.base_agent import BaseAgent
from app.core.llm import LLMService
from app.core.logging import logger
from app.schemas.research import ResearchResponse


class ResearchAgent(BaseAgent):

    def execute(self, task: str):

        logger.info(f"Researching task: {task}")

        prompt = f"""
You are a research assistant.

TASK:
{task}

Return ONLY valid JSON.

Format:

{{
  "question": "{task}",
  "answer": "your answer"
}}
"""

        response = LLMService.generate(prompt)

        raw_response = response.content.strip()

        try:

            cleaned_response = self.clean_json(raw_response)

            parsed = ResearchResponse.model_validate_json(cleaned_response)

            return parsed.model_dump()

        except Exception as e:

            logger.error(f"Research agent parsing failed: {e}")

            return {
                "question": task,
                "answer": raw_response
            }

    def clean_json(self, text: str):

        text = text.strip()

        text = re.sub(r"```json", "", text)
        text = re.sub(r"```", "", text)

        match = re.search(r"\{.*\}", text, re.DOTALL)

        if match:
            text = match.group(0)

        return text