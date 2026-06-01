from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

class LLMService:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise ValueError("GROQ_API_KEY is missing in environment")

        self.client = Groq(api_key=api_key)
        self.model = "llama-3.3-70b-versatile"

        
    def generate(self, prompt: str, temperature: float = 0.2):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "Return ONLY valid JSON. No markdown. No backticks."},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature
        )

        return response.choices[0].message.content