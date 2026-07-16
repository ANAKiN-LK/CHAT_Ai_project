from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
class DocumentChunk(BaseModel):
    content: str = Field(..., description="เนื้อหาของ Chunk")
    metadata: Dict[str, Any] = Field(default={}, description="Metadata")
class SearchResult(BaseModel):
    content: str
    score: float
    metadata: Dict[str, Any] = {}