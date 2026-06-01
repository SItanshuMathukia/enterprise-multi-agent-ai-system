import json
import re

from app.agents.base_agent import BaseAgent
from app.core.llm import llm_service
from app.core.logging import logger
from app.schemas.coding import CodingResponse


class CodingAgent(BaseAgent):

    def execute(self, task: str):

        logger.info(f"Coding agent processing: {task}")

        prompt = f"""
You are a senior software engineer.

Return ONLY valid JSON.

Task: {task}

You must:
- give IMPLEMENTATION level steps
- include file names
- include code hints where relevant
- include dependencies
- include commands

Output format:
{{
  "summary": "...",
  "steps": [
    {{
      "id": 1,
      "title": "...",
      "details": "..."
    }}
  ],
  "final_output": "..."
}}
"""

        response = llm_service.generate(prompt)

        raw_response = response.strip()

        try:

            cleaned_response = self.clean_json(raw_response)

            parsed = CodingResponse.model_validate_json(cleaned_response)

            return parsed.model_dump()

        except Exception as e:

            logger.error(f"Coding agent parsing failed: {e}")

            return {
                "summary": "Failed to parse structured coding response",
                "raw_output": raw_response
            }

    def clean_json(self, text: str):

        text = text.strip()

        text = re.sub(r"```json", "", text)
        text = re.sub(r"```", "", text)

        match = re.search(r"\{.*\}", text, re.DOTALL)

        if match:
            text = match.group(0)

        text = text.replace("\t", " ")

        text = re.sub(r"[\x00-\x1F]+", " ", text)

        return text