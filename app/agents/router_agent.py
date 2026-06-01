from app.agents.base_agent import BaseAgent
from app.core.llm import llm_service
from app.schemas.router import RouterResponse
from app.utils.json_cleaner import clean_llm_response
from app.core.logging import logger


class RouterAgent(BaseAgent):

    def execute(self, task: str):

        logger.info(f"Routing task: {task}")

        prompt = f"""
You are an intelligent task router.

Classify the task into ONE of:
- coding
- research
- review
- planning
- travel
- general

Return STRICT JSON ONLY:

{{
  "route": "coding | research | review | planning | travel",
  "confidence": 0.0,
  "reasoning": "short reason"
}}

Rules:
- ALWAYS include all 3 fields
- confidence must be between 0 and 1
- reasoning must be 1 short sentence
- output must be valid JSON ONLY (no markdown, no text)

Task: {task}
"""

        try:
            response = llm_service.generate(prompt)

            cleaned_response = clean_llm_response(response)

            parsed = RouterResponse.model_validate_json(cleaned_response)

            return parsed.model_dump()

        except Exception as e:
            logger.error(f"Router failed, fallback used: {str(e)}")

            # SAFE FALLBACK (never crash workflow)
            return {
                "route": "research",
                "confidence": 0.5,
                "reasoning": "fallback due to parsing error"
            }