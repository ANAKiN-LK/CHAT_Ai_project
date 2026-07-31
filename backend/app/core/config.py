import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
class Settings(BaseSettings):

    APP_NAME: str = "Chat-AI"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
   
    VLLM_BASE_URL: str = "http://localhost:8001/v1"
    VLLM_API_KEY: str = "EMPTY"
    VLLM_MODEL_NAME: str = "Qwen/Qwen2.5-14B-Instruct-AWQ"

    EMBEDDING_URL: str = "http://localhost:8081"
    EMBEDDING_API_KEY: str = "dummy_token"
    
    QDRANT_URL: str = "http://localhost:6333"
    QDRANT_API_KEY: str = "ca0a9feebc24ee1915d7bc1b585627efb9bb30ffebfd34ea8a352522d250614b"
    QDRANT_COLLECTION: str = "Chat-AI"
    
    model_config = SettingsConfigDict(
        env_file=os.path.join(BASE_DIR, ".env"),
        env_file_encoding="utf-8",
        extra="ignore" 
    )

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()