from pathlib import Path
from typing import Optional
from mcp.server.fastmcp import FastMCP
from main import run_doc_flow

# 创建 FastMCP 实例
mcp = FastMCP("doc-writer")

@mcp.tool()
def write_documentation(repo_url: str) -> str:
    """
    为给定的 GitHub 仓库 URL 生成文档。
    生成完成时通知用户。

    参数:
        repo_url (str): GitHub 仓库的 URL
    
    返回:
        str: 文档成功生成时返回消息。
    """
    try:
        if not repo_url.startswith(("http://", "https://")):
            raise ValueError("无效的仓库 URL 格式")
        
        print(f"开始为仓库 {repo_url} 生成文档...")
        run_doc_flow(repo_url)
        return f"✅ 成功为仓库 {repo_url} 生成中文文档\n\n文档文件已保存到 docs/ 目录，您可以使用 list_docs() 查看文件列表。"
    
    except Exception as e:
        return f"❌ 为仓库 {repo_url} 生成文档失败，原因：{e}"

@mcp.tool()
def list_docs() -> str:
    """
    列出成功生成的文档文件。

    参数: 无
    
    返回: 
        str: 返回生成的文档文件的格式化字符串列表。
    """
    docs_dir = Path("docs")
    if not docs_dir.exists():
        return "⚠️ 未找到文档文件，请先使用 write_documentation() 生成文档。"
    
    doc_files = list(docs_dir.glob("*.mdx"))
    if not doc_files:
        return "📁 docs 目录为空，没有找到 .mdx 文档文件。"
    
    output_lines = ["📚 已生成的文档文件:"]
    for i, doc_file in enumerate(doc_files, 1):
        output_lines.append(f"{i}. docs/{doc_file.name}")
    
    output_lines.append(f"\n总计: {len(doc_files)} 个文档文件")
    output_lines.append("\n使用 view_content('docs/文件名.mdx') 查看具体内容")
    return "\n".join(output_lines)

@mcp.tool()
def view_content(file_path: str) -> str:
    """
    显示生成的文档文件内容。
    
    参数:
        file_path (str): 文档文件的相对路径（例如：'docs/overview.mdx'）
    
    返回:
        str: 文件内容或错误消息。
    """
    try:
        if not file_path.startswith("docs/") or "../" in file_path:
            raise ValueError("无效的文件路径")
            
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"文件 {file_path} 不存在")
        if not path.is_file():
            raise ValueError(f"路径 {file_path} 不是文件")
        if path.suffix not in {".mdx", ".md"}:
            raise ValueError("只能查看文档文件 (.mdx/.md)")
            
        content = path.read_text(encoding="utf-8")
        file_size = len(content)
        
        return f"📄 文件: {file_path}\n📏 大小: {file_size} 字符\n\n{content}"
        
    except Exception as e:
        return f"❌ 查看文档失败：{str(e)}"

@mcp.tool()
def get_help() -> str:
    """
    获取文档生成工具的使用帮助。

    参数: 无
    
    返回:
        str: 工具使用说明。
    """
    help_text = """
📖 文档生成工具使用指南

可用命令：

1. write_documentation(repo_url)
   - 为指定的 GitHub 仓库生成中文文档
   - 示例: write_documentation("https://github.com/username/repo")

2. list_docs()
   - 列出所有已生成的文档文件
   - 示例: list_docs()

3. view_content(file_path)
   - 查看指定文档文件的内容
   - 示例: view_content("docs/项目概述.mdx")

4. get_help()
   - 显示此帮助信息

工作流程：
1. 使用 write_documentation() 生成文档
2. 使用 list_docs() 查看生成的文件
3. 使用 view_content() 阅读具体文档内容

注意：确保 Ollama 服务正在运行且已安装 deepseek-r1 模型。
"""
    return help_text

# 运行服务器
if __name__ == "__main__":
    print("🚀 启动文档生成 MCP 服务器...")
    print("📡 服务器运行在 http://127.0.0.1:8000/sse")
    print("💡 使用 get_help() 查看可用命令")
    mcp.run(transport='sse')