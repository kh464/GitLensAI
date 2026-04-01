from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    """
    全局配置管理中心
    Pydantic 会自动从环境变量或 .env 文件中读取同名变量
    """
    PROJECT_NAME: str = "GitHub CodeSense API"
    VERSION: str = "1.0.0"
    
    # 跨域配置
    CORS_ORIGINS: str = "*"

    # AI 模型配置
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL_URL: str = ""
    AI_API_TIMEOUT: float = 30.0
    
    # GitHub 配置
    GITHUB_API_TIMEOUT: float = 15.0

    @property
    def cors_origins_list(self) -> List[str]:
        # 将逗号分隔的字符串转换为列表
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

# 实例化全局配置对象
settings = Settings()