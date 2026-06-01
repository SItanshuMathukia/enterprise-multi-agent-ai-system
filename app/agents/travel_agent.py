from app.agents.base_agent import BaseAgent
from app.core.llm import llm_service
from app.schemas.travel import TravelResponse
from app.utils.json_cleaner import clean_llm_response
from app.core.logging import logger


class TravelAgent(BaseAgent):

    def execute(self, task: str):

        logger.info(f"Travel agent processing: {task}")

        prompt = f"""
You are a travel booking assistant.

Return ONLY valid JSON.

IMPORTANT:
Return EXACTLY this structure:

{{
  "summary": "...",
  "steps": [
    {{
      "id": 1,
      "title": "...",
      "details": "..."
    }}
  ],
  "booking_flow": "..."
}}

Rules:
- No markdown
- No explanation
- No extra text
- Always valid JSON

Task:
{task}
"""

        response = llm_service.generate(prompt)

        cleaned_response = clean_llm_response(response)

        try:
            parsed = TravelResponse.model_validate_json(cleaned_response)
            return parsed.model_dump()

        except Exception as e:

            logger.error(f"Travel parsing failed: {e}")

            return {
                "summary": "Failed to parse travel response",
                "steps": [],
                "booking_flow": cleaned_response
            }