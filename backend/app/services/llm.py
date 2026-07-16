from langchain_openai import ChatOpenAI
from app.core.config import settings

class LLMService:
    _instance: ChatOpenAI = None
    
    @classmethod
    def get_llm(cls) -> ChatOpenAI:
        if cls._instance is None:
            cls._instance = ChatOpenAI(
                base_url=settings.VLLM_BASE_URL,
                api_key=settings.VLLM_API_KEY,
                model=settings.VLLM_MODEL_NAME,
                temperature=0.7,
                streaming=True
            )
        return cls._instance
def get_llm() -> ChatOpenAI:
    return LLMService.get_llm()