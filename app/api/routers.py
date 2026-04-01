from fastapi import APIRouter, HTTPException, status
from app.schemas import AnalyzeRequest, AnalyzeResponse, ChatRequest, ChatResponse
from app.services.github_service import GitHubService
from app.services.ai_service import AIService

router = APIRouter()

@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_github_repo(request: AnalyzeRequest):
    """分析 GitHub 仓库并生成架构文档"""
    repo_details = GitHubService.parse_url(request.github_url)
    if not repo_details:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="提供的 GitHub 链接无效")
    
    repo_info = await GitHubService.fetch_repo_context(repo_details["owner"], repo_details["repo"])
    
    prompt = (
        "你是一个资深的软件架构师。请根据以下我提供的 GitHub 开源项目的基础信息、目录结构以及 README 内容，"
        "为我编写一份针对新手的项目解析文档。\n"
        "要求包含以下几个章节（必须用 Markdown 格式输出）：\n"
        "1. **项目一句话简介**\n2. **核心技术栈分析**\n3. **系统架构与模块划分**\n4. **新手阅读源码建议**\n\n"
        f"以下是项目信息:\n{repo_info['context']}"
    )
    system_instruction = "你是一个擅长提炼代码架构和指导新手阅读源码的高级工程师。"
    
    docs = await AIService.generate_content(prompt, system_instruction)
    
    return AnalyzeResponse(
        repo_name=repo_info["name"],
        repo_info=repo_info["context"],
        docs=docs
    )

@router.post("/chat", response_model=ChatResponse)
async def chat_with_agent(request: ChatRequest):
    """基于仓库上下文的实时问答"""
    chat_history = "\n".join([f"{'提问' if m.role == 'user' else '回答'}: {m.content}" for m in request.messages])
    
    prompt = (
        "用户正在就以下 GitHub 项目向你提问。\n"
        f"【项目背景信息】:\n{request.repo_info}\n\n"
        f"【历史对话】:\n{chat_history}\n\n"
        "请针对用户最新的提问给出专业、清晰、富有启发性的解答。推测或建议文件路径。"
    )
    system_instruction = "你是一个耐心的代码开源项目导师。用中文回答，态度友好，解释通俗易懂。"
    
    reply = await AIService.generate_content(prompt, system_instruction)
    return ChatResponse(reply=reply)