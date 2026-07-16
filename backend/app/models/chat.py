from pydantic import BaseModel, Field
from typing import Optional
class ChatRequest(BaseModel):
    question: str = Field(..., description="คำถามจากผู้ใช้", min_length=1)
    user_id: str = Field(default="guest", description="User ID")
    session_id: Optional[str] = Field(default=None, description="Session ID")
class ChatResponse(BaseModel):
    answer: str = Field(..., description="คำตอบจาก AI")
    is_from_knowledge_base: bool = Field(default=False, description="คำตอบมาจากฐานความรู้หรือไม่")
    sources: list[str] = Field(default=[], description="แหล่งอ้างอิง")
    status: str = Field(default="success")
class HealthResponse(BaseModel):
    status: str
    app_name: str
    version: str
    services: dict