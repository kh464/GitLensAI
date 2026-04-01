import logging
import httpx
from fastapi import HTTPException, status
from app.config import settings

logger = logging.getLogger("AIService")

class AIService:
    """处理所有与大模型相关的业务逻辑"""
    
    @classmethod
    async def generate_content(cls, prompt: str, system_instruction: str = "") -> str:
        if not settings.GEMINI_API_KEY:
            logger.warning("未配置 GEMINI_API_KEY")
            return "后端未配置大模型 API Key，请联系管理员在 .env 中配置。"

        # 动态读取 URL 和 Key，代码中不再写死任何模型信息
        url = f"{settings.GEMINI_MODEL_URL}?key={settings.GEMINI_API_KEY}"
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "systemInstruction": {"parts": [{"text": system_instruction}]}
        }

        async with httpx.AsyncClient(timeout=settings.AI_API_TIMEOUT) as client:
            try:
                response = await client.post(url, json=payload)
                response.raise_for_status()
                data = response.json()
                return data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "未能生成有效回复")
            except httpx.HTTPError as e:
                logger.error(f"调用 AI API 失败: {str(e)}")
                raise HTTPException(
                    status_code=status.HTTP_502_BAD_GATEWAY, 
                    detail="AI 服务暂时不可用，请稍后重试。"
                )