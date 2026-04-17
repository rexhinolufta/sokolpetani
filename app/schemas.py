from pydantic import BaseModel, Field
from typing import Optional, Dict, Any


class ChatRequest(BaseModel):
    user_id: str = Field(..., description="User ID")
    message: str = Field(..., description="Message from user")
    use_memory: bool = True


class ChatResponse(BaseModel):
    reply: str
    tool_used: Optional[str] = None
    tool_result: Optional[Dict[str, Any]] = None


class VoiceOutRequest(BaseModel):
    text: str


class HealthResponse(BaseModel):
    status: str = "ok"
    service: str = "FusionBrain"
