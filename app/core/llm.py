from app.services.llm_service import LLMService

llm_service = LLMService()

class LLM:
    def invoke(self, prompt, **kwargs):
        response = llm_service.generate(prompt, **kwargs)

        # ALWAYS normalize output
        if hasattr(response, "content"):
            return response.content

        return str(response)
    
llm = LLM()