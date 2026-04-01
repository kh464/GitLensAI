from pydantic import BaseModel, Field
from typing import List

class AnalyzeRequest(BaseModel):
    github_url: str = Field(..., description="GitHub 项目的完整 HTTPS 链接")

class AnalyzeResponse(BaseModel):
    repo_name: str
    repo_info: str
    docs: str

class ChatMessage(BaseModel):
    role: str = Field(..., pattern="^(user|ai)$")
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    repo_info: str

class ChatResponse(BaseModel):
    reply: str