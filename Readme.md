🚀 GitHub CodeSense - 源码解析与 AI 问答助手 (企业级架构版)

一款基于 FastAPI 和 Vue 3 构建的智能化 GitHub 源码阅读辅助工具。通过结合大语言模型 (LLM)，本项目能够自动拉取 GitHub 仓库信息，提取架构逻辑，并提供一个基于该仓库上下文的专属 AI 代码导师。

✨ 核心特性

🏗 自动化架构解析：输入仓库链接，一键生成项目简介、技术栈分析、模块划分及源码阅读指南。

🤖 沉浸式 AI 导师：基于项目上下文的实时问答，解答代码逻辑、入口文件、设计模式等疑难问题。

🏢 企业级后端架构：采用 FastAPI，基于 12-Factor 原则，实现配置分离、路由与业务逻辑解耦 (Controller-Service 模式)、Pydantic 强类型校验及全异步 I/O。

⚡️ 现代化前端交互：基于 Vue 3 Composition API 构建，分离 API 服务层与 UI 状态，Tailwind CSS 驱动响应式界面。

📂 目录结构

本项目严格遵循前后端分离及高内聚低耦合的规范：

project_root/
├── .env                        # [需手动创建] 环境变量与配置文件 (存放API Key等)
├── .gitignore                  # Git 忽略配置
├── requirements.txt            # Python 后端依赖
├── main.py                     # FastAPI 应用程序入口
├── app/                        # 后端核心业务模块
│   ├── config.py               # 全局配置管理中心 (基于 pydantic-settings)
│   ├── schemas.py              # DTO 数据模型 (请求与响应的强类型定义)
│   ├── api/
│   │   └── routers.py          # 路由层 (API 接口定义)
│   └── services/
│       ├── github_service.py   # GitHub 数据抓取与解析逻辑
│       └── ai_service.py       # 大模型 (Gemini) 调用与 Prompt 组装
└── frontend/                   # 前端资源
    └── index.html              # Vue 3 前端页面 (演示用单文件架构)


🛠️ 快速启动

1. 环境准备

请确保本地已安装 Python 3.9+。

克隆项目后，建议创建并激活一个虚拟环境：

python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate


2. 安装后端依赖

pip install -r requirements.txt


3. 配置环境变量

在项目根目录下创建一个 .env 文件，并填入以下基础配置（参考 .gitignore，此文件不会被提交）：

# .env 
PROJECT_NAME="GitHub CodeSense Enterprise API"
VERSION="2.0.0"
CORS_ORIGINS="*"

# Gemini API 配置
GEMINI_API_KEY="在这里填入你的_GEMINI_API_KEY"
GEMINI_MODEL_URL="[https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent](https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent)"
AI_API_TIMEOUT=30.0

# GitHub 配置
GITHUB_API_TIMEOUT=15.0


4. 启动后端服务

在项目根目录下，运行以下命令启动 FastAPI 服务（开启热重载）：

python main.py
# 或者使用 uvicorn 命令直接启动：
# uvicorn main:app --host 0.0.0.0 --port 3001 --reload


服务启动后，可访问 http://localhost:3001/docs 查看由 Swagger UI 自动生成的交互式 API 文档。

5. 启动前端页面

本企业级 Demo 的前端通过 CDN 引入了 Vue 3 和 Tailwind CSS，并封装在 frontend/index.html 中。
你可以直接在浏览器中双击打开该 HTML 文件，或者使用简单的本地服务器来托管它：

# 使用 Python 自带的简易服务器 (在 frontend 目录下运行)
cd frontend
python -m http.server 8080


然后在浏览器中访问 http://localhost:8080 即可开始使用！

📄 许可证

本项目基于 MIT License 授权。