import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.api.routers import router

# 初始化日志配置
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# 通过配置中心 (settings) 读取 App 基础信息
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="企业级 GitHub 源码解析服务"
)

# 动态注入 CORS 跨域配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载路由模块，统一添加 /api/v1 前缀
app.include_router(router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn
    # 使用字符串 "main:app" 形式启动，配合 reload=True 开启热重载，方便本地开发
    uvicorn.run("main:app", host="0.0.0.0", port=3001, reload=True)