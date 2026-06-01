from app.agents.base_agent import BaseAgent
from app.core.llm import llm_service
from app.schemas.review import ReviewResponse
from app.utils.json_cleaner import clean_llm_response
from app.core.logging import logger


class ReviewAgent(BaseAgent):

    def execute(self, task: str):

        logger.info(f"Reviewing task: {task}")

        prompt = f"""
        You are a principal software engineer.

        Review the architecture and implementation plan.

        Focus on:
        - weaknesses
        - scalability issues
        - security concerns
        - missing features
        - architecture improvements

        Return ONLY valid JSON.

        Example:
        {{
            "review": "your review here"
        }}

        Task:
        {task}
        """

        response = llm_service.generate(prompt)

        cleaned_response = clean_llm_response(response)

        parsed = ReviewResponse.model_validate_json(cleaned_response)

        return parsed.model_dump()