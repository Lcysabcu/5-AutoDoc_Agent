import nest_asyncio
nest_asyncio.apply()

from documentation_flow import CreateDocumentationFlow

def run_doc_flow(repo_url: str) -> list[str]:
    """
    运行文档生成流程
    
    参数:
        repo_url (str): GitHub 仓库 URL
        
    返回:
        list[str]: 生成的文档文件路径列表
    """
    print(f"🎯 启动文档生成流程...")
    print(f"📦 目标仓库: {repo_url}")
    
    flow = CreateDocumentationFlow()
    result = flow.kickoff(inputs={"project_url": repo_url})
    
    print(f"✅ 文档生成流程完成!")
    return result

if __name__ == "__main__":
    print("🤖 文档生成工具")
    print("=" * 50)
    repo_url = input("请输入 GitHub 仓库 URL: ")
    
    if not repo_url.strip():
        print("❌ 请输入有效的仓库 URL")
    else:
        try:
            generated_docs = run_doc_flow(repo_url)
            print(f"\n🎉 成功生成 {len(generated_docs)} 个文档文件:")
            for doc_path in generated_docs:
                print(f"   📄 {doc_path}")
        except Exception as e:
            print(f"❌ 文档生成失败: {e}")