from urllib.parse import urlparse
from typing import Optional
import httpx
from fastapi import HTTPException
from app.config import settings

class GitHubService:
    """处理所有与 GitHub API 相关的业务逻辑"""
    
    @staticmethod
    def parse_url(url: str) -> Optional[dict]:
        try:
            parsed = urlparse(url)
            if parsed.hostname != "github.com":
                return None
            parts = [p for p in parsed.path.split("/") if p]
            if len(parts) >= 2:
                return {"owner": parts[0], "repo": parts[1].replace(".git", "")}
            return None
        except Exception:
            return None

    @classmethod
    async def fetch_repo_context(cls, owner: str, repo: str) -> dict:
        # 使用配置文件中的超时时间
        async with httpx.AsyncClient(timeout=settings.GITHUB_API_TIMEOUT) as client:
            # 1. 获取基本信息
            repo_res = await client.get(f"https://api.github.com/repos/{owner}/{repo}")
            if repo_res.status_code != 200:
                raise HTTPException(status_code=repo_res.status_code, detail="无法获取 GitHub 仓库信息")
            repo_data = repo_res.json()
            
            default_branch = repo_data.get("default_branch", "main")
            
            # 2. 获取 README
            readme_url = f"https://raw.githubusercontent.com/{owner}/{repo}/{default_branch}/README.md"
            readme_text = "未找到 README"
            try:
                readme_res = await client.get(readme_url)
                if readme_res.status_code == 200:
                    readme_text = readme_res.text
            except httpx.RequestError:
                pass

            # 3. 获取目录结构
            tree_text = ""
            try:
                tree_res = await client.get(f"https://api.github.com/repos/{owner}/{repo}/git/trees/{default_branch}")
                if tree_res.status_code == 200:
                    tree_data = tree_res.json()
                    items = [f"{'📁' if i['type'] == 'tree' else '📄'} {i['path']}" for i in tree_data.get("tree", [])]
                    tree_text = "\n".join(items[:30])
            except httpx.RequestError:
                pass

            context = (
                f"项目名称: {repo_data.get('full_name')}\n"
                f"描述: {repo_data.get('description', '无')}\n"
                f"主语言: {repo_data.get('language', '未知')}\n"
                f"顶层目录:\n{tree_text}\n\n"
                f"README 片段:\n{readme_text[:3000]}"
            )
            return {"name": repo_data.get("name"), "context": context}